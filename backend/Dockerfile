FROM python:3.11-slim

WORKDIR /app
COPY app.py /app/app.py
RUN pip install flask flask-cors

EXPOSE 5500
CMD ["python", "app.py"]

