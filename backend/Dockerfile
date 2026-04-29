# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data required during build
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Copy the rest of the application
COPY . .

# Expose the port that the application listens on
EXPOSE 7860

# Run the web service on container startup
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
