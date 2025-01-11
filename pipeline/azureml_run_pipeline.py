import argparse
from pathlib import Path
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml import MLClient, Input, Output, load_component
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import Model, Workspace, Environment
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import AmlCompute
import uuid
import json


parser = argparse.ArgumentParser("pipeline")
parser.add_argument("--subscription_id", type=str)
parser.add_argument("--resource_group_name", type=str)
parser.add_argument("--workspace_name", type=str)
parser.add_argument("--location", type=str)

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name
location = args.location

try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    print(ex)
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    credential = InteractiveBrowserCredential()


# Get a handle to workspace
ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group_name,
    workspace_name=workspace_name,
)

environment = Environment(
    name="treediculous_environment",
    image="ghcr.io/patacoing/treediculous:pipeline",
    description="Environment for treediculous pipeline",
)

ml_client.environments.create_or_update(environment)

# Retrieve an already attached Azure Machine Learning Compute.
cluster_name = "simple-cpu-low"

cluster_basic = AmlCompute(
    name=cluster_name,
    type="amlcompute",
    size="Standard_D4s_v3",
    location=location,  # az account list-locations -o table
    min_instances=0,
    max_instances=1,
    idle_time_before_scale_down=60,
)
ml_client.begin_create_or_update(cluster_basic).result()


@pipeline(default_compute=cluster_name)
def azureml_pipeline(
    images_input_data: Input,
    labels_input_data: Input,
):
    preprocessing_step = load_component(source="preprocessing/command.yml")
    preprocessing_data = preprocessing_step(images_input=images_input_data)

    splitting_step = load_component(source="splitting/command.yml")
    splitting_data = splitting_step(
        labels_input=labels_input_data,
        images_input=preprocessing_data.outputs.images_output,
    )

    train_step = load_component(source="training/command.yml")
    train_data = train_step(
        train_labels_input=splitting_data.outputs.train_labels_output,
        train_images_input=splitting_data.outputs.train_images_output,
        test_labels_input=splitting_data.outputs.test_labels_output,
        test_images_input=splitting_data.outputs.test_images_output,
    )

    return {
        "output": train_data.outputs.model_output,
    }


IMAGES_DATASET_NAME = "treediculous-images"
LABELS_DATASET_NAME = "treediculous-labels"
IMAGES_DATASET_VERSION = 1
LABELS_DATASET_VERSION = 1


pipeline_job = azureml_pipeline(
    images_input_data=Input(
        path=f"azureml:{IMAGES_DATASET_NAME}:{IMAGES_DATASET_VERSION}",
        type=AssetTypes.URI_FOLDER,
    ),
    labels_input_data=Input(
        path=f"azureml:{LABELS_DATASET_NAME}:{LABELS_DATASET_VERSION}",
        type=AssetTypes.URI_FOLDER,
    ),
)


azure_blob = "azureml://datastores/workspaceblobstore/paths/"
experiment_id = str(uuid.uuid4())
custom_output_path = azure_blob + "treediculous/" + experiment_id + "/"
pipeline_job.outputs.output = Output(
    type=AssetTypes.URI_FOLDER, mode="rw_mount", path=custom_output_path
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="treediculous_pipeline",
)

ml_client.jobs.stream(pipeline_job.name)

model_name = "treediculous"
try:
    model_version = str(len(list(ml_client.models.list(model_name))) + 1)
except:
    model_version = "1"

file_model = Model(
    version=model_version,
    path=custom_output_path + f"{model_name}.keras",
    type=AssetTypes.CUSTOM_MODEL,
    name=model_name,
    description="Model created from azureML.",
)
saved_model = ml_client.models.create_or_update(file_model)

print(
    f"Model with name {saved_model.name} was registered to workspace, the model version is {saved_model.version}."
)

output_data = {
    "model_version": saved_model.version,
    "model_name": saved_model.name,
    "experiment_id": experiment_id,
}


app_path = Path(__file__).parent.resolve().parent / "api/app/model"
app_path.mkdir(exist_ok=True)

with open(app_path / "model_version", "w") as f:
    f.write(str(output_data["model_version"]))

print(json.dumps(output_data))