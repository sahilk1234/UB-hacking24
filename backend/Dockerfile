# backend/Dockerfile
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first for efficient caching
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run Flask with reload enabled
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
