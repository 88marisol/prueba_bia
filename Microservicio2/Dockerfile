FROM python:3.9.7
LABEL maintainer="88marisol@gmail.com"
WORKDIR ./app
COPY -R ../Microservicio1/instance ./instance
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app/app.py"]
#CMD ["python3", "app.py"]