# Use official Python slim image
FROM python:3.12-slim

# System dependencies for OpenCV and pyzbar
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create application directories with proper permissions
RUN mkdir -p \
    /app/qr_dataset \
    /app/qr_code_images \
    /app/cropped_qr_codes \
    && chmod 755 /app/*

# Create non-root user and set ownership
RUN useradd -m appuser && \
    chown -R appuser:appuser \
        /app/qr_dataset \
        /app/qr_code_images \
        /app/cropped_qr_codes

# Set working directory
WORKDIR /app

# Copy application files with proper ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Configure PATH for user-installed binaries
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Verification step
RUN which streamlit && \
    streamlit --version && \
    ls -ld /app/qr_*  # Verify directory permissions


# ─── Runtime command ────────────────────────────────────────────────
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]