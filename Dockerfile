FROM python:latest 
COPY ./requirements.txt /dockerBuild/requirements.txt
WORKDIR /dockerBuild
RUN pip install --no-cache-dir -r requirements.txt
COPY . /dockerBuild
ENV DB_TYPE=postgresql
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=postgres
ENV DB_ENDPOINT=postgres:5432 
ENV DB_NAME=bit_schema
ENV DB_TEST_NAME=bit_schema_test
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV MS_URL=http://MS:5000
ENV FLASK_APP=run.py
ENTRYPOINT ["make"]
CMD ["docker_host_dev"]
