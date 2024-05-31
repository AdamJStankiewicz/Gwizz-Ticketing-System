FROM python:3.12.2

ADD server.py .

RUN pip install uuid pysqlite3 Flask Flask-SocketIO public-ip

EXPOSE 1477
CMD [ "python", "server.py"]