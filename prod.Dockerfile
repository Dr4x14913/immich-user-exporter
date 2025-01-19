FROM python:3.9-slim

RUN apt update && apt install -y git

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app /app

# Set working directory
WORKDIR /app

# Start the app
CMD ["gunicorn", "-c", "/app/gunicorn.py", "app:app"]
