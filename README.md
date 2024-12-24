# Treediculous

## Description

This project aims to classify Xmas trees. The dataset is composed of images
of Xmas trees retrieved from the internet, reddit, facebook groups, ...
With treediculous, you'll be able to get a **real** opinion on your Xmas tree.

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