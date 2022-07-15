# Model Fit Generator

This module listens to a Redis queue and generates a network when a job is available. When finished the worker will upload the model to an Azure Blob Storage container. The worker will also notify the master when it is done using a webhook.

## Installation

```bash
pip install -r requirements.txt
```

## Run the Model Fit Generator

1. Set environment variables in `.env` file.
2. Run `dramatiq model_fit_generator.worker -p 1 -t 1`.
