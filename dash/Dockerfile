FROM python:3.8.5

WORKDIR /opt/project/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY aws-cred.json .
EXPOSE 8050/tcp
CMD ["/usr/local/bin/python", "/opt/project/app.py"]