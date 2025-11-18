FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY protos/ ./protos/
COPY server.py .
COPY generate_protos.sh .

RUN chmod +x generate_protos.sh

RUN ./generate_protos.sh

EXPOSE 50051

CMD ["python3", "server.py"]
