
FROM python:3.10
WORKDIR src

# dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

# source
COPY src/*.py src/
COPY *.py .
COPY openapi.yaml .
COPY config.json .
COPY .env.local .

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "50001"]
