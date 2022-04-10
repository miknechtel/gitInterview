FROM python:3.6.1-alpine
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install jproperties
RUN pip install requests
COPY app.py /app.py
COPY app-config.properties /app-config.properties
CMD ["python","-u","app.py"]

