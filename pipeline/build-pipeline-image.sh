#!/bin/bash

PUSH=false

DOCKER_REGISTRY="ghcr.io"
DOCKER_REPOSITORY="patacoing"
DOCKER_IMAGE="treediculous"
DOCKER_IMAGE_TAG="pipeline"
DOCKERFILE_NAME="Dockerfile"

IMAGE_NAME=$DOCKER_REGISTRY/$DOCKER_REPOSITORY/$DOCKER_IMAGE:$DOCKER_IMAGE_TAG

while getopts "p" option
do
  case $option in
    p) PUSH=true;;
  esac
done

cd ../

docker build -f pipeline/$DOCKERFILE_NAME -t treediculous-pipepline:latest --no-cache . --platform linux/amd64

if $PUSH; then
  exit 0
fi

docker tag treediculous-pipepline:latest $IMAGE_NAME
docker push $IMAGE_NAME