FROM python:3.13.5-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY utils/ utils/
COPY classes/ classes/
COPY cogs/ cogs/
COPY listeners/ listeners/
COPY tasks/ tasks/
COPY utils/ utils/

CMD ["python", "main.py"]