FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Note: .env file should NOT be copied to the image
# Use -e or --env-file flag when running the container

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]