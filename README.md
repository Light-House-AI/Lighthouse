# Lighthouse-AI

An end-to-end platform for creating and shipping machine learning models to production.

## Getting started

### Client setup

```bash
TODO
```

### Server setup

```bash
TODO
```

## System architecture

![./docs/system_design.jpg](docs/system_design.jpg)

## Project structure

```
├── .github         <- GitHub templates and CI files.
│
├── client          <- Client code.
│
├── docs            <- Documentation and examples.
│
├── infrastructure  <- Infrastructure code.
│
├── server          <- Server code.
│   │
│   ├── automl
│   │
│   ├── mlops
│   │   ├── monitoring      <- Models monitoring service.
│   │   └── serving         <- Models deployment service.
│   │
│   ├── ml_projects
│   │   ├── alembic     <- Alembic migration scripts.
│   │   └── app         <- FastApi application.
│   │
│   ├── requirements.txt        <- Python requirements.
│   └── requirements-dev.txt    <- Python development dependencies.
│
└── docker-compose.yml      <- Docker compose file for development.

```
