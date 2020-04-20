# Tickets API

A practical guide with FastAPI, MongoDb and Docker 


## Project setup
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
or 
```
curl
```

## Deployment with Docker
1. Build the Docker image
```
docker build --file Dockerfile --tag fast-tickets-api .
```

2. Running the Docker image
```
docker run -p 8000:8000 fast-tickets-api
```

3. Entering into the Docker image
```
docker run -it --entrypoint /bin/bash fast-tickets-api
```

## docker-compose
1. Launching the service
```
docker-compose up
```
This command looks for the `docker-compose.yaml` configuration file. If you want to use another configuration file,
it can be specified with the `-f` switch. For example  

docker compose options:
    -d                  Detached mode: Run containers in the background,
                        print new container names. Incompatible with
                        --abort-on-container-exit.
    --force-recreate    Recreate containers even if their configuration
                        and image haven't changed.
    --build             Build images before starting containers.
    --no-deps           Don't start linked services.



2. Testing
```
docker-compose -f docker-compose.test.yaml up --abort-on-container-exit --exit-code-from fast-tickets-api
```
