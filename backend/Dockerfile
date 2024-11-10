# Dockerfile for Backend

FROM python:3.10
WORKDIR /app

# Install dependencies with specific NumPy version
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of your app code
COPY . /app

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]