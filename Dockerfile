# Use a slim Python base image
FROM python:3.12-slim

# Install system dependencies needed by OpenCV and pyzbar
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default port (Railway will override with $PORT)
ENV PORT=8000

# Run Streamlit using Railway's environment variable
CMD ["sh", "-c", "ls -l && pwd && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]