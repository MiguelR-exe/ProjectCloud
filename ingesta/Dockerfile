FROM python:3.11-slim
WORKDIR /app
RUN pip install boto3 pandas sqlalchemy pymysql
COPY ingest.py .
CMD ["python", "ingest.py"]
