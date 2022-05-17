FROM python:3.9-slim

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt 

COPY ./ ./

WORKDIR /usr/app/src

ENV AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING}

ENV AZURE_CONTAINER_NAME=models

ENV AZURE_BLOB_NAME=${AZURE_BLOB_NAME}

CMD ["uvicorn", "main:app", "--host=0.0.0.0"]
