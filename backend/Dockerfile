FROM python:3.8.3
# Base docker image of python 3.x

RUN pip install --upgrade pip
# Upgrade pip package 

WORKDIR /app
# Change working dir to app

ADD fastapi_test.py requirements.txt /app/
# Copy main.py and requirements.txt from local into app dir inside the container

COPY . .
# Copy the helper_functions module 

RUN pip install -r requirements.txt
# Refering to copied file inside the app dir install the user dependency

EXPOSE 8000
# Expose a port inside the container on which services run

#CMD ["gunicorn" ,"-w", "4", "-k", "uvicorn.workers.UvicornWorker" , "--bind", "0.0.0.0:8000", "fastapi_test:app"]
CMD ["uvicorn", "fastapi_test:app","--host", "0.0.0.0", "--port", "8000"]
# gunicorn command to run the service with 4 worker nodes binding localhost/0.0.0.0 on port 8000 refering app inside the main.py