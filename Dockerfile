FROM python:3.8.5-alpine

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["gunicorn", "-w 4", "main:app", "--bind", "0.0.0.0:5000"]