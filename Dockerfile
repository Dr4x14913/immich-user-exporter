FROM python:3.9-slim

RUN apt update && apt install -y git

# # Copy the application code
# COPY app /app

# # Set working directory
# WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8070

# Start the Dash app
CMD ["python", "app/app.py"]
