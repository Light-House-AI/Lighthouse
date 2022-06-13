# Network Generator

A module that generates the best possible network for a given set of parameters.

## Installation

```bash
pip install -r requirements.txt
```

## Run as a Worker

When run as a worker, the module will listen to a Redis queue and generates a network when a job is available.
When finished the worker will upload the model to an Azure Blob Storage container. The worker will also notify the master when it is done using a webhook.

1. Set environment variables in `.env` file.
2. Run `dramatiq network_generator.worker -p 1 -t 1`.
