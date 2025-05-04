FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    libzbar0 libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Non-root user setup with PATH configuration
RUN useradd -m appuser && \
    mkdir -p /home/appuser/.local/bin && \
    chown -R appuser:appuser /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
WORKDIR /app

COPY --chown=appuser:appuser . .

USER appuser

# Install dependencies with upgraded pip and proper PATH
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Verify streamlit location
RUN which streamlit

CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]