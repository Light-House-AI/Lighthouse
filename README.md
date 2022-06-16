# Lighthouse-AI

An end-to-end platform for creating and shipping machine learning models to production.

## Getting started

### Docker environment

Run the following command to setup the environment:

```bash
cd deploy
docker-compose up -d --build
```

Notes:

- You can change the environment variables in the `deploy/.env` file.
- You can comment unwanted services in the `deploy/docker-compose.yml` file.

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
├── datasets        <- Datasets used for testing.
│
├── deploy
│   ├── k8s                 <- k8s manifests for deployment.
│   └── docker-compose.yml  <- Docker compose file for development.
│
├── docs                <- Documentation and examples.
│
├── infrastructure      <- Infrastructure code.
│
├── network_generator   <- Network generator module.
│
├── notebooks           <- Development code.
│
├── server              <- Server code.
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
