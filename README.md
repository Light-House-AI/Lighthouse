# Lighthouse-AI

An end-to-end platform for creating and shipping machine learning models to production.

## Getting started

### Docker environment

1. Add `.env` file in the `server` directory.
2. Run the docker-compose up command: `docker-compose -f ./deploy/docker-compose.yml -d up`

### Without docker

#### Client

```bash
TODO
```

#### Server

Install the required dependencies:

```bash
cd server
pip install -r requirements.txt
```

Add the `.env` file in the `server` directory.

Run the server:

```bash
start.sh # or start.bat for windows
```

## System architecture

![./docs/system_design.jpg](docs/system_design.jpg)

## Project structure

```
├── .github         <- GitHub templates and CI files.
│
├── client          <- Client code.
│
├── deploy
│   ├── k8s                 <- k8s manifests for deployment.
│   └── docker-compose.yml  <- Docker compose file for development.
│
├── docs            <- Documentation and examples.
│
├── infrastructure  <- Infrastructure code.
│
├── server          <- Server code.
│   │
│   └── lighthouse
│       │
│       ├── automl
│       │
│       ├── ml_projects
│       │   ├── api             <- ML projects API.
│       │   ├── db              <- ML projects database and migration scripts.
│       │   └── services        <- Contains the logic for orchestrating ML projects.
│       │
│       ├── mlops
│       │   ├── monitoring      <- Models monitoring service.
│       │   └── serving         <- Models deployment service.
│       │
│       ├── __main__.py         <- The entrypoint for the server.
│       ├── config.py           <- Contains the configuration for the server.
│       └── logger.py           <- Logging utility.
│
└── wrapper         <- ML model wrapper code.

```
