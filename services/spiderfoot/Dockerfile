FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Clone and install SpiderFoot
RUN git clone --depth 1 https://github.com/smicallef/spiderfoot.git /opt/spiderfoot && \
    cd /opt/spiderfoot && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade pyOpenSSL cryptography

# Copy server files
COPY src/spiderfoot_mcp_server.py /app/src/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make the server executable
RUN chmod +x /app/src/spiderfoot_mcp_server.py

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Verify installation
RUN test -f /opt/spiderfoot/sf.py && echo "✓ SpiderFoot found"

# Run the MCP server
ENTRYPOINT ["python3", "/app/src/spiderfoot_mcp_server.py"]

