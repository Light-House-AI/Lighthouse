FROM python:3.9-slim

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt 

COPY ./ ./

WORKDIR /usr/app/src

ENV AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING}

ENV CONTAINER_NAME=models

ENV MODEL_ID=${MODEL_ID}

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
