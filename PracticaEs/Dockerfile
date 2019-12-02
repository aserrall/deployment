FROM python:3.6.8

RUN mkdir /code
WORKDIR /code
COPY requeriments.txt /code/
RUN pip3 install -r requeriments.txt
COPY . /code
RUN pip install Pillow

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
