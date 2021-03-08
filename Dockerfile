FROM python:latest 
COPY . . 
ENV DB_TYPE=postgresql+psycopg2
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=postgres
ENV DB_ENDPOINT=localhost:5432 
ENV DB_TEST_NAME=bit_schema_test
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432
RUN pip install -r requirements.txt
CMD python run.py