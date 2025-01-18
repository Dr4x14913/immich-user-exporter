FROM python:3.9-slim

RUN apt update && apt install -y git

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app /app
COPY ./zoho_api.json /

# Set working directory
WORKDIR /app

# Expose the application port
EXPOSE 8050

# Start the app
CMD ["gunicorn", "wsgi:application", "-c", "gunicorn.py"]
