FROM python:3.12-alpine
WORKDIR /agent
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sender.py .
CMD ["python", "sender.py"]
