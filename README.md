# 🔍 OSINT Tools MCP Server

[![MCP Server](https://img.shields.io/badge/MCP-Server-blue)](https://github.com/modelcontextprotocol/specification)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![OSINT](https://img.shields.io/badge/OSINT-Tools-red)](https://github.com/topics/osint)
[![Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green)](https://github.com/frishtik/osint-tools-mcp-server)

A comprehensive MCP server that exposes multiple OSINT tools to AI assistants like Claude. This server allows AI to perform sophisticated reconnaissance and information gathering tasks using industry-standard OSINT tools.

**✨ New Features:**
- 🐳 **Docker Support** - Run everything in a containerized environment
- 🔑 **API Key Management** - Enhanced functionality with configurable API keys
- ⏱️ **Configurable Timeouts** - Control execution time per tool
- 🧪 **Comprehensive Testing** - Full test suite for all tools
- 📦 **Docker Hub Publishing** - Pre-built images available
- 📚 **Enhanced Documentation** - Complete guides for all features

## 🛠️ Available Tools

### 🔍 **Sherlock** - Username Search
Search for usernames across 399+ social media platforms and websites. Perfect for digital footprint analysis.
- **Input**: Username
- **Output**: List of platforms where username exists

### 📧 **Holehe** - Email Verification  
Check if an email is registered on 120+ platforms. Lightning fast and accurate.
- **Input**: Email address
- **Output**: Platforms where email is registered

### 🕷️ **SpiderFoot** - Comprehensive OSINT
The Swiss Army knife of OSINT. Performs deep reconnaissance with automatic target type detection.
- **Input**: IP, domain, email, phone, username, person name, Bitcoin address, or network block
- **Output**: Comprehensive intelligence report
- **⚠️ Note**: SpiderFoot can take 5-30 minutes to complete a full scan. Be patient!

### 🔎 **GHunt** - Google Account Intel
Extract information from Google accounts using email or Google ID.
- **Input**: Email or Google ID
- **Output**: Google account details and associated information
- **⚠️ Note**: Requires Google authentication session (run `ghunt login` inside container)

### 🌐 **Maigret** - Advanced Username Search
Search across 3000+ sites with false positive detection and detailed analysis.
- **Input**: Username
- **Output**: Detailed report with confidence scores

### 🌾 **TheHarvester** - Domain Intelligence
Gather emails, subdomains, hosts, employee names, and more from public sources.
- **Input**: Domain or company name
- **Output**: Comprehensive domain intelligence
- **API Keys**: Hunter.io, Bing, Shodan, SecurityTrails (optional, for enhanced results)

### 🐦 **Blackbird** - Fast Username OSINT
Lightning-fast searches across 581 sites for username reconnaissance.
- **Input**: Username
- **Output**: Quick profile discovery results

## 🚀 Installation

### 🐳 Docker Installation (Recommended)

The easiest way to get started is using Docker. All tools are pre-installed and configured.

#### Option 1: Use Pre-built Image from Docker Hub

```bash
# Pull the image
docker pull hackerdogs/osint-tools-mcp-server:latest

# Configure Claude Desktop to use Docker
```

Add to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "osint-tools": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "hackerdogs/osint-tools-mcp-server:latest"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

#### Option 2: Build from Source

```bash
# Clone the repository
git clone https://github.com/frishtik/osint-tools-mcp-server.git
cd osint-tools-mcp-server

# Build the Docker image
docker build -t osint-tools-mcp-server:latest .

# Use with Claude Desktop (same config as above, but use local image name)
```

#### Option 3: Docker Compose

```bash
# Use docker-compose for easy management
docker-compose up
```

### 📦 Local Installation (Alternative)

If you prefer to run without Docker:

1. **Clone this repository:**
```bash
git clone https://github.com/frishtik/osint-tools-mcp-server.git
cd osint-tools-mcp-server
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install OSINT tools:**
   - Sherlock, Holehe, Maigret, and TheHarvester are installed via pip
   - See [DOCKER_USAGE.md](DOCKER_USAGE.md) for manual installation of SpiderFoot, GHunt, and Blackbird

4. **Configure Claude Desktop:**

```json
{
  "mcpServers": {
    "osint-tools": {
      "command": "python",
      "args": ["/path/to/osint-tools-mcp-server/src/osint_tools_mcp_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

5. **Restart Claude Desktop** to load the new MCP server.

### 🔑 API Key Configuration (Optional)

For enhanced functionality, configure API keys. See [API_KEYS.md](API_KEYS.md) for complete documentation.

**Quick setup:**
1. Copy `mcpServer.json.example` to your Claude Desktop config directory
2. Replace placeholder values with your actual API keys
3. Restart Claude Desktop

**Supported API keys:**
- **theHarvester**: Hunter.io, Bing, Shodan, SecurityTrails
- **GHunt**: Google session (requires `ghunt login`)
- See [API_KEYS_REFERENCE.md](API_KEYS_REFERENCE.md) for full list

## 🎮 Usage Tips

### Getting Started

Working with AI for OSINT is a bit of an art form. Here's how to get the best results:

#### Start Simple with Holehe
I recommend starting with the **Holehe** tool - it's fast, reliable, and gives you immediate results:

```
"Check if john.doe@example.com is registered on any platforms"
```

#### Level Up to Username Searches
Once you're comfortable, try username searches with Sherlock or Maigret:

```
"Search for the username 'johndoe123' across social media platforms"
```

#### Complex Orchestrations
Here's where it gets interesting. You can chain tools together:

```
"I found an email address contact@suspicious-site.com. Can you:
1. Check what platforms it's registered on
2. Extract the domain and search for subdomains and other emails
3. Search for any usernames associated with this domain"
```

#### Let the AI Be Smart
Sometimes the best approach is to give Claude context and let it decide:

```
"I'm investigating the digital footprint of username 'hackerman2024'. 
Use your judgment to gather as much information as possible."
```

### ⏱️ Timeout Configuration

All tools support configurable timeouts. Set timeouts per tool call:

```
"Search for username 'testuser' with a 60 second timeout"
```

**Recommended timeouts:**
- **Fast tools** (Holehe, GHunt): 30-60 seconds
- **Medium tools** (Maigret, Blackbird): 60-120 seconds
- **Slow tools** (Sherlock, SpiderFoot): 300-600+ seconds

See [TIMEOUT_CONFIGURATION.md](TIMEOUT_CONFIGURATION.md) for detailed timeout guidance.

### Pro Tips 🎯

1. **Be Patient with SpiderFoot**: It's incredibly thorough but can take up to 30 minutes for a full scan. Start it and grab a coffee!

2. **Parallel Processing**: Claude can run multiple tools simultaneously. Don't hesitate to ask for parallel searches:
   ```
   "Search for 'johndoe' on both Sherlock and Maigret at the same time"
   ```

3. **Know When to Hold the Leash**: 
   - For specific investigations: Be explicit about which tools to use
   - For exploratory research: Let Claude choose the tools
   - For time-sensitive tasks: Avoid SpiderFoot, stick to faster tools

4. **Cross-Reference Results**: Different tools have different databases. Maigret might find accounts that Sherlock misses and vice versa.

5. **Email First, Username Second**: If you have an email, start there - it's usually more unique than usernames.

6. **Use API Keys for Better Results**: Configure API keys for theHarvester to access premium sources (Hunter.io, Shodan, etc.)

## ⚖️ Ethical Usage & Legal Compliance

**🚨 IMPORTANT: This tool is for legitimate security research and OSINT investigations only.**

### You MUST:
- ✅ Only gather publicly available information
- ✅ Respect privacy laws in your jurisdiction (GDPR, CCPA, etc.)
- ✅ Follow platforms' Terms of Service
- ✅ Use findings responsibly and ethically
- ✅ Obtain proper authorization for any professional investigations

### You MUST NOT:
- ❌ Use this for stalking, harassment, or any malicious purpose
- ❌ Violate any local, state, or federal laws
- ❌ Access private or protected information
- ❌ Use findings to harm individuals or organizations

## 🧪 Testing

The project includes comprehensive test suites to verify all tools are working:

### Run All Tests
```bash
# Comprehensive test suite (quick tests)
python3 test_all_tools.py

# Functional tests with real data
python3 test_functional_real_data.py

# Docker-specific tests
./test_docker.sh
```

### Test Individual Tools
```bash
# Test a single tool
python3 test_single_tool.py sherlock_username_search
```

**Test Results**: All tools are verified and production-ready. See [PRE_PRODUCTION_TEST_REPORT.md](PRE_PRODUCTION_TEST_REPORT.md) for detailed test results.

## 🔧 Troubleshooting

### Common Issues

**Docker image not found**: 
```bash
# Pull from Docker Hub
docker pull hackerdogs/osint-tools-mcp-server:latest

# Or build locally
docker build -t osint-tools-mcp-server:latest .
```

**Tools not found** (local installation): Make sure all OSINT tools are installed and in your PATH:
```bash
which sherlock holehe maigret theharvester
```

**SpiderFoot errors**: In Docker, SpiderFoot is pre-installed. For local install, ensure it's in `/opt/spiderfoot`.

**Timeout issues**: Some tools may timeout on slow connections. Try increasing the timeout parameter:
```
"Search for username with a 60 second timeout"
```

**GHunt authentication errors**: GHunt requires Google authentication. Run `ghunt login` inside the container or see [API_KEYS.md](API_KEYS.md).

**Rate limiting**: Some platforms rate-limit searches. If you're getting blocked, wait a bit and try again.

**API key issues**: Verify your API keys are correctly configured. See [API_KEYS_VERIFICATION.md](API_KEYS_VERIFICATION.md) for troubleshooting.

## 📚 Documentation

Comprehensive documentation is available for all features:

- **[DOCKER_USAGE.md](DOCKER_USAGE.md)** - Complete Docker setup and usage guide
- **[API_KEYS.md](API_KEYS.md)** - API key configuration and management
- **[API_KEYS_REFERENCE.md](API_KEYS_REFERENCE.md)** - Complete API key reference
- **[MCP_SERVER_CONFIG.md](MCP_SERVER_CONFIG.md)** - Claude Desktop configuration guide
- **[TIMEOUT_CONFIGURATION.md](TIMEOUT_CONFIGURATION.md)** - Timeout configuration guide
- **[PUBLISHING.md](PUBLISHING.md)** - Docker Hub publishing guide
- **[PRE_PRODUCTION_TEST_REPORT.md](PRE_PRODUCTION_TEST_REPORT.md)** - Test results and status

## 🏗️ Architecture

This MCP server uses Python's asyncio for non-blocking tool execution. Each tool runs in a subprocess, allowing for parallel execution and proper timeout handling.

```
Claude Desktop <-> MCP Protocol <-> OSINT MCP Server <-> OSINT Tools
```

### Docker Architecture

```
Claude Desktop -> Docker -> Container -> OSINT Tools
```

All tools are pre-installed and configured in the Docker container, eliminating setup complexity.

## 📦 Publishing

### Publishing to Docker Hub

The project includes a publishing script for easy deployment:

```bash
# Publish with 'latest' tag
./publish_to_docker.sh

# Publish with version tag
./publish_to_docker.sh v1.0.0
```

**Docker Hub**: [hackerdogs/osint-tools-mcp-server](https://hub.docker.com/r/hackerdogs/osint-tools-mcp-server)

See [PUBLISHING.md](PUBLISHING.md) for complete publishing guide.

## 🤝 Contributing

Found a bug? Want to add a new tool? Contributions are welcome! 

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewOSINTTool`)
3. Run tests to ensure everything works: `python3 test_all_tools.py`
4. Commit your changes (`git commit -m 'Add NewOSINTTool support'`)
5. Push to the branch (`git push origin feature/NewOSINTTool`)
6. Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/frishtik/osint-tools-mcp-server.git
cd osint-tools-mcp-server

# Build Docker image for testing
docker build -t osint-tools-mcp-server:latest .

# Run tests
python3 test_all_tools.py
```

## ✅ Production Status

**Status**: ✅ **Production Ready**

- ✅ All 7 OSINT tools functional
- ✅ Docker support with pre-built images
- ✅ Comprehensive test suite (6/6 tests passing)
- ✅ API key management
- ✅ Configurable timeouts
- ✅ Complete documentation

See [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md) and [PRE_PRODUCTION_TEST_REPORT.md](PRE_PRODUCTION_TEST_REPORT.md) for detailed status.

## 📚 Acknowledgments

Special thanks to these awesome projects:
- [mcp-maigret](https://github.com/BurtTheCoder/mcp-maigret) - Inspiration for MCP implementation and README structure. Go give them a ⭐!
- [Model Context Protocol](https://github.com/modelcontextprotocol/specification) - The protocol making all this possible
- All the incredible OSINT tool maintainers:
  - [Sherlock](https://github.com/sherlock-project/sherlock)
  - [Holehe](https://github.com/megadose/holehe)
  - [SpiderFoot](https://github.com/smicallef/spiderfoot)
  - [GHunt](https://github.com/mxrch/GHunt)
  - [Maigret](https://github.com/soxoj/maigret)
  - [theHarvester](https://github.com/laramies/theHarvester)
  - [Blackbird](https://github.com/p1ngul1n0/blackbird)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is provided for educational and legitimate security research purposes only. The authors are not responsible for any misuse or damage caused by this program. Use at your own risk and always ensure you have proper authorization before conducting any investigations.

---

**Remember**: With great power comes great responsibility. Use these tools wisely and ethically! 🦸‍♂️

Built with ❤️ for the OSINT community
