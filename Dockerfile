FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    libzbar0 libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Non-root setup
RUN useradd -m appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser

# PATH configuration (NEW - Critical)
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Verify installations (NEW)
RUN which streamlit && streamlit --version

# Final command (IMPORTANT CHANGE)
CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]