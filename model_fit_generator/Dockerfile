FROM python:3.9-slim

# create the app group and user
RUN addgroup --system app && \
    adduser --system --group app

# change the working directory
WORKDIR /app

# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt 

# copy files to the app directory
COPY ./ ./

# chown all the files to the app user
RUN chown -R app:app /app

# change to the app user
# switch to a non-root user, which is recommended.
USER app

# run the app
CMD ["dramatiq", "model_creator.worker", "-p", "1", "-t", "1"]