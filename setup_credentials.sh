#!/bin/bash


function usage {
  echo "Usage: $0 subscription_id ovh_application_key ovh_application_secret ovh_consumer_key [options]"
  echo "Options:"
  echo "  -g: Set the secret in the GitHub repository"
  echo "  -h: Display this help message"
  exit 1
}

SUBSCRIPTION_ID=$1
OVH_APPLICATION_KEY=$2
OVH_APPLICATION_SECRET=$3
OVH_CONSUMER_KEY=$4
shift 4

SECRET_FILE="act.secrets"
GH_SECRET=false
GH_ENV="treediculous"
OPTSTRING="gh"
GIT_TOKEN=$(gh auth token)

while getopts ${OPTSTRING} opt; do
  case ${opt} in
    g)
      echo "Setting secret in GitHub repository"
      GH_SECRET=true
      ;;
    h)
      usage
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      usage
      ;;
  esac
done

if [ -z "$SUBSCRIPTION_ID" ]; then
  usage
fi

# get credentials
credentials=$(az ad sp create-for-rbac --name "mlapp-romain" --role contributor --scopes "/subscriptions/$SUBSCRIPTION_ID" --sdk-auth)

# Format credentials to remove escape characters and remove first and last character
formatted_credentials=$(echo $credentials | jq -c @json | tr -d "\\" | sed -r 's/^.{1}//' | sed 's/.$//')

function add_secret_to_github {
  secret_name=$1
  secret_value=$2
  gh secret set "$secret_name" --body "$secret_value" --env "$GH_ENV"
}

function add_secret_to_file {
  secret_name=$1
  secret_value=$2
  echo "$secret_name=$secret_value" >> $SECRET_FILE
}

if [ "$GH_SECRET" = true ]; then
  add_secret_to_github "AZURE_CREDENTIALS" "$formatted_credentials"
  add_secret_to_github "AZURE_SUBSCRIPTION_ID" "$SUBSCRIPTION_ID"
  add_secret_to_github "GIT_TOKEN" "$GIT_TOKEN"
  add_secret_to_github "OVH_APPLICATION_KEY" "$OVH_APPLICATION_KEY"
  add_secret_to_github "OVH_APPLICATION_SECRET" "$OVH_APPLICATION_SECRET"
  add_secret_to_github "OVH_CONSUMER_KEY" "$OVH_CONSUMER_KEY"
fi

echo "" > $SECRET_FILE
add_secret_to_file "AZURE_CREDENTIALS" "$formatted_credentials"
add_secret_to_file "AZURE_SUBSCRIPTION_ID" "$SUBSCRIPTION_ID"
add_secret_to_file "GIT_TOKEN" "$GIT_TOKEN"
add_secret_to_file "OVH_APPLICATION_KEY" "$OVH_APPLICATION_KEY"
add_secret_to_file "OVH_APPLICATION_SECRET" "$OVH_APPLICATION_SECRET"
add_secret_to_file "OVH_CONSUMER_KEY" "$OVH_CONSUMER_KEY"
echo "Secrets saved in $SECRET_FILE"