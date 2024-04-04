FROM python:3.8-buster

COPY mkdocs_requirements.txt .

RUN pip install -r mkdocs_requirements.txt
