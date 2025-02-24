FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /app

COPY setup.py requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only requirements first (for caching layers)
COPY . /app/

# Set the default command
CMD ["python3", "server/main.py"]

# Example: docker run --env-file .env my-python-app
