FROM python:3.9-slim

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt 

COPY ./ ./

WORKDIR /usr/app/src

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
