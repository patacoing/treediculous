## api-0.5.0 (2025-01-11)

### Feat

- **web**: added ads.txt in public/

### Fix

- **ci**: set ml pipeline to be runnable
- **ci**: used fetch-depth 0 to get all tags
- **ci**: added environment in reusable workflow

### Refactor

- **model**: refactored package to work properly

## api-0.4.5 (2025-01-02)

### Fix

- **ci**: use working directory

## api-0.4.4 (2025-01-02)

### Fix

- **ci**: use fetch-depth instead of ref

## api-0.4.3 (2025-01-02)

### Fix

- **api**: removed group deps in dockerfile

## api-0.4.2 (2025-01-02)

### Fix

- **ci**: fetch all tags

### Refactor

- changed structure

## api-0.4.1 (2025-01-02)

### Fix

- use model/ as a package
- install deps for api
- **ci**: fetch all tags

## api-0.4.0 (2025-01-02)

### Feat

- **deployment**: added terraform and https
- icon, ads header

### Fix

- **ci**: multine line env var
- **ci**: tfplan file
- **ci**: multiline output
- **ci**: put vars into env
- **ci**: checkout
- **ci**: checkout
- **ci**: set working directory
- **deployment**: copy public to docker image

## api-0.3.2 (2024-12-26)

### Feat

- test
- **ci-cd**: build push and deploy frontend
- **ci-cd**: add github workflow, added cz
- **webapp**: react webapp to call the backend
- **api**: api to infer the model
- azureml pipeline

### Fix

- **ci**: wrong var name to get tag
- **ci**: fetch pushed tag
- copy css config to dockerfile
- **ci-cd**: set dir in web deployment
- **ci-cd**: set working directory of the step
- **ci-cd**: add no-cache
- **ci-cd**: set packages permissions to write
- **ci-cd**: can't use env var in environment
- **deployment**: fixed dockerfiles, added tailwind
