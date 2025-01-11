# Treediculous

## Description

This project aims to classify Xmas trees. The dataset is composed of images
of Xmas trees retrieved from the internet, reddit, facebook groups, ...
With treediculous, you'll be able to get a **real** opinion on your Xmas tree.

The website is available at https://treediculous.fr

## Disclaimer

The resulting predictions are not meant to be taken seriously. The fact that defining
a Xmas tree as `ugly` or `nice` is purely subjective and depends on the annotator.

## Labels

- ugly
- nice

## Annotation rules

- if the tree is too much decorated → ugly
- if the tree is too simple → ugly
- if the color of the tree is extravagant → ugly
- if the tree is ugly → ugly
- if the shape of the tree is strange → ugly
- if the tree is too small → ugly

## Annotation tool

label-studio


## Tech stack

- API : FastAPI
- Frontend : React
- Deployment : Docker, Azure, Github Actions, Terraform
- MLOps : AzureML

## Docker images

Docker images are available at https://github.com/patacoing/treediculous/pkgs/container/treediculous

- API : treediculous:api-*version*

It contains the FastAPI app and the model to classify the trees.

- Frontend : treediculous:web-*version*

It contains the React app to display the predictions as well as Caddy.

- ML Pipeline environment : treediculous:pipeline

It contains the environment to run the ML pipeline in azure

## Structure

- api : FastAPI app to infer the model
- webapp : React app to call the backend
- model : azureml pipeline, model training

## TODO:

Need to seperate containers in 2 container groups:
- Caddy
- API + Frontend
because when we deploy a container, the entire group is recreated so caddy always tries getting a certificate