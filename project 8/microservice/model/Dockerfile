 FROM python:3.8

 COPY requirements.txt ./app_requirements/requirements.txt
 CMD pep install --no-cache-dir -r ./app_requirements/requirements.txt
 COPY ./src/ .

 RUN python ./model.py