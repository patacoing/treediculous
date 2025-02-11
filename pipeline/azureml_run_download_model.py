import argparse
from pathlib import Path
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml import MLClient


parser = argparse.ArgumentParser("train")
parser.add_argument("--subscription_id", type=str)
parser.add_argument("--resource_group_name", type=str)
parser.add_argument("--workspace_name", type=str)
parser.add_argument("--location", type=str)
parser.add_argument("--version", type=str, default="1")
parser.add_argument("--download_path", type=str, default="./")

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name
location = args.location
version = args.version
download_path = args.download_path


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

base_path = Path(__file__).resolve().parent

model_name = 'treediculous'

ml_client.models.download(name=model_name, version=version, download_path=base_path / download_path)