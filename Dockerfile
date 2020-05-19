FROM python:3.8.1-alpine

# set working directory
WORKDIR /dockerBuild

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# add and install requirements
COPY ./requirements.txt /dockerBuild/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /dockerBuild

# run server
CMD ["flask", "run", "--host", "0.0.0.0"]