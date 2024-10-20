FROM python:3.9-slim

#Set up the working directory in the container (app.py = app)
WORKDIR /app 

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 

ENV FLASK_APP = app.py
ENV FLASK_RUN_HOST = 0.0.0.0
ENV FLASK_RUN_PORT = 5000

EXPOSE 5000 

CMD ["flask", "run"]
#CMD ["flask", "run", "--host = 0.0.0.0"]
