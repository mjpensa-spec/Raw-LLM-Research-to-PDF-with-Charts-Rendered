# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for WeasyPrint, Playwright, and build tools
RUN apt-get update && apt-get install -y \
    # Build essentials for pip packages
    gcc \
    g++ \
    make \
    # WeasyPrint dependencies
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    libcairo2-dev \
    shared-mime-info \
    # Fonts for rendering (use Debian Trixie compatible packages)
    fonts-liberation \
    fonts-noto-core \
    fonts-noto-cjk \
    # Playwright dependencies
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libxshmfence1 \
    # Additional Chromium dependencies
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcb-dri3-0 \
    libxext6 \
    libxi6 \
    libxtst6 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium browser
# NOTE: We do NOT use --with-deps because we've already installed all system dependencies above
# Using --with-deps would try to install ttf-ubuntu-font-family and ttf-unifont which don't exist in Debian Trixie
RUN echo "Installing Playwright Chromium..." && \
    playwright install chromium && \
    echo "Playwright Chromium installed successfully"

# Verify Playwright installation works
RUN python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright verification passed')"

# Copy application code
COPY *.py .
COPY templates/ templates/
COPY static/ static/

# Create directories for uploads and outputs
RUN mkdir -p /tmp/md_uploads /tmp/pdf_outputs

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Run the application
CMD ["python", "app.py"]
