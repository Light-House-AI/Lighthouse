FROM python:3.9-slim

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt 

COPY ./ ./ 

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]