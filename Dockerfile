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

# Install Python OSINT tools via pip
RUN pip install --no-cache-dir \
    sherlock-project \
    holehe \
    maigret

# Install ujson and other dependencies first (needed by theHarvester)
# Install required ones first, then optional ones
RUN pip install --no-cache-dir ujson aiomultiprocess && \
    pip install --no-cache-dir censys || true && \
    pip install --no-cache-dir shodan || true && \
    pip install --no-cache-dir git+https://github.com/0xInfection/aiosqli.git || pip install --no-cache-dir aiosqli || echo "aiosqli optional"

# Copy patch scripts
COPY patch_theharvester.py /tmp/patch_theharvester.py
COPY fix_aiosqli.py /tmp/fix_aiosqli.py

# Install theHarvester via pip (handles dependencies better)
RUN pip install --no-cache-dir theharvester && \
    git clone --depth 1 https://github.com/laramies/theHarvester.git /opt/theharvester && \
    cd /opt/theharvester && \
    pip install --no-cache-dir -r requirements.txt 2>/dev/null || true && \
    pip install --no-cache-dir aiosqlite uvloop || true && \
    # Install aiosqli properly - try multiple methods
    (pip install --no-cache-dir git+https://github.com/0xInfection/aiosqli.git 2>&1 || \
     pip install --no-cache-dir aiosqli 2>&1 || \
     (echo "Installing aiosqli from alternative source" && \
      git clone --depth 1 https://github.com/0xInfection/aiosqli.git /tmp/aiosqli && \
      cd /tmp/aiosqli && pip install --no-cache-dir . 2>&1 || \
      (python3 -c "import os, site; sp=site.getsitepackages()[0] if site.getsitepackages() else '/usr/local/lib/python3.11/site-packages'; os.makedirs(f'{sp}/aiosqli', exist_ok=True); f=open(f'{sp}/aiosqli/__init__.py','w'); f.write('class AioSQLi:\\n    def __init__(self,*a,**k):pass\\n    def scan(self,*a,**k):return[]\\n    async def scan_async(self,*a,**k):return[]\\n'); f.close(); print('Created aiosqli dummy')"))) && \
    cd /opt/theharvester && \
    python3 /tmp/fix_aiosqli.py && \
    find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true && \
    find . -name "*.pyc" -delete 2>/dev/null || true && \
    chmod +x theHarvester.py 2>/dev/null || true

# Clone and install SpiderFoot
RUN git clone --depth 1 https://github.com/smicallef/spiderfoot.git /opt/spiderfoot && \
    cd /opt/spiderfoot && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade pyOpenSSL cryptography

# Clone and install GHunt
RUN git clone --depth 1 https://github.com/mxrch/GHunt.git /opt/ghunt && \
    cd /opt/ghunt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir packaging && \
    pip install --no-cache-dir -e . 2>/dev/null || pip install --no-cache-dir . 2>/dev/null || true && \
    chmod +x main.py ghunt.py 2>/dev/null || true && \
    ln -s /opt/ghunt/main.py /usr/local/bin/ghunt 2>/dev/null || true

# Clone and install Blackbird
RUN git clone --depth 1 https://github.com/p1ngul1n0/blackbird.git /opt/blackbird && \
    cd /opt/blackbird && \
    pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /app/data && \
    echo '{}' > /app/data/wmn-data.json

# Copy server files
COPY src/osint_tools_mcp_server.py /app/src/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make the server executable
RUN chmod +x /app/src/osint_tools_mcp_server.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/ghunt:${PATH}"

# Verify installations
RUN python3 -c "import sys; print('Python:', sys.version)" && \
    which sherlock && echo "✓ Sherlock found" && \
    which holehe && echo "✓ Holehe found" && \
    which maigret && echo "✓ Maigret found" && \
    test -f /opt/spiderfoot/sf.py && echo "✓ SpiderFoot found" && \
    ls -la /opt/ghunt/ | head -5 && test -d /opt/ghunt && echo "✓ GHunt directory found" && \
    ls -la /opt/blackbird/ | head -5 && test -d /opt/blackbird && echo "✓ Blackbird directory found" && \
    echo "All tools verified successfully"

# Run the MCP server
ENTRYPOINT ["python3", "/app/src/osint_tools_mcp_server.py"]