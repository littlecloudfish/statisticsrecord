# syntax=docker/dockerfile:1
FROM ubuntu:22.04
FROM python:3.8-slim-buster
# install app dependencies
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update && apt-get install -y python3 python3-pip
COPY ["requirements.txt", "/home/little/Documents/searchweb/flask-wengui-statistics-fishpublic/requirements.txt"]
WORKDIR "/home/little/Documents/searchweb/flask-wengui-statistics-fishpublic/"
RUN pip3 install -r requirements.txt

# install app
COPY . .
# final configuration
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]