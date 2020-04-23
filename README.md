


# Tickets API

  

You are working in a large Telecommunication company as a developer and you got the task to build a new API for their soon to be popular ticket management system. API should support following use case scenarios: create a new ticket, update ticket data, find ticket by id, find ticket by filter criteria.
  
## Project Structue:

models  - pydantic models that are used in api

db      - db specific utils

core    - some general components (configuration for db url)

api     - handlers for routes

main.py - FastAPI application instance and api router including

## Project setup - without docker

1. Create the virtual environment.

```

virtualenv /path/to/venv --python=/path/to/python3

```

You can find out the path to your `python3` interpreter with the command `which python3`.

  

2. Activate the environment and install dependencies.

```

source /path/to/venv/bin/activate

pip install -r requirements.txt

```

  

3. Launch the service

```

uvicorn app.main:app

```

  

## Posting requests locally

When the service is running, try

```

127.0.0.1/docs

```


## Project setup with Docker

1. Build the Docker image

```

docker-compose build

```


2. Launching the service

```

docker-compose up

```
This command looks for the `docker-compose.yaml` configuration file. If you want to use another configuration file,

it can be specified with the `-f` switch. For example

  

docker compose options:

```
    -d Detached mode: Run containers in the background,

    print new container names. Incompatible with

    --abort-on-container-exit.

    --force-recreate Recreate containers even if their configuration

    and image haven't changed.

    --build Build images before starting containers.

    --no-deps Don't start linked services.
```