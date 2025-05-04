FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    libzbar0 libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Non-root user setup (Railway requirement)
RUN useradd -m appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser

# Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use Railway's dynamic PORT
CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]