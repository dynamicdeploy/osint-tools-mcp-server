# API Keys Reference for mcpServer.json

This document explains all API keys available in `mcpServer.json` organized by tool.

## SpiderFoot API Keys

SpiderFoot supports 100+ modules with API keys. These enable premium data sources and enhanced functionality.

### Core Security APIs
- **SHODAN_API_KEY** - Shodan internet search and device intelligence
- **VIRUSTOTAL_API_KEY** - VirusTotal malware and URL analysis
- **HAVEIBEENPWNED_API_KEY** - Have I Been Pwned breach database
- **ABUSEIPDB_API_KEY** - AbuseIPDB IP reputation and abuse reports
- **CENSYS_API_ID** / **CENSYS_API_SECRET** - Censys internet-wide search

### Threat Intelligence
- **ALIENVAULT_OTX_API_KEY** - AlienVault OTX threat intelligence
- **GREYNOISE_API_KEY** - GreyNoise IP reputation
- **HYBRIDANALYSIS_API_KEY** - Hybrid Analysis malware sandbox
- **THREATBOOK_API_KEY** - ThreatBook threat intelligence
- **THREATFOX_API_KEY** - ThreatFox malware IOCs
- **PULSEDIVE_API_KEY** - Pulsedive threat intelligence

### Domain & DNS Intelligence
- **SECURITYTRAILS_API_KEY** - SecurityTrails domain and DNS intelligence
- **PASSIVETOTAL_API_USERNAME** / **PASSIVETOTAL_API_KEY** - PassiveTotal threat intelligence
- **FARSIGHT_API_KEY** - Farsight Security DNSDB
- **DNSDB_API_KEY** - DNSDB passive DNS database
- **WHOISXML_API_KEY** - WhoisXML API whois data

### IP & Network Intelligence
- **IPINFO_API_KEY** - IPInfo.io IP geolocation
- **IPWHOIS_API_KEY** - IPWhois IP information
- **CRIMINALIP_API_KEY** - Criminal IP threat intelligence
- **ONYPHE_API_KEY** - Onyphe cyber threat intelligence
- **ZOOMEYE_API_KEY** - ZoomEye cyberspace search

### Malware & Security
- **MALSHARE_API_KEY** - MalShare malware repository
- **LEAKIX_API_KEY** - LeakIX data breach search
- **URLSCAN_API_KEY** - urlscan.io URL analysis
- **SAFEBROWSING_API_KEY** - Google Safe Browsing API

### Cloud & Infrastructure
- **CLOUDFLARE_API_KEY** / **CLOUDFLARE_API_EMAIL** - Cloudflare API
- **GITHUB_API_KEY** - GitHub API for code search

### Specialized Services
- **BINARYEDGE_API_KEY** - BinaryEdge attack surface intelligence
- **BITCOINABUSE_API_KEY** - BitcoinAbuse cryptocurrency tracking
- **BLOCKLIST_DE_API_KEY** - Blocklist.de IP blocklist
- **CIRCL_API_USERNAME** / **CIRCL_API_PASSWORD** - CIRCL passive DNS
- **CROWDSTRIKE_API_KEY** / **CROWDSTRIKE_API_SECRET** - CrowdStrike Falcon
- **INTELX_API_KEY** - IntelX data breach search
- **MACVENDORS_API_KEY** - MAC Vendors MAC address lookup
- **PASTEBIN_API_KEY** - Pastebin API
- **RISKIQ_API_KEY** / **RISKIQ_API_SECRET** - RiskIQ threat intelligence
- **SOCRADATA_API_KEY** - Socradata threat intelligence
- **SPYSE_API_KEY** - Spyse cybersecurity search

## GHunt API Keys

GHunt uses Google APIs for enhanced account searches and information gathering.

- **GOOGLE_API_KEY** - Google Custom Search API key
- **GOOGLE_CX** - Google Custom Search Engine ID
- **GOOGLE_CLIENT_ID** - Google OAuth client ID (for authenticated searches)
- **GOOGLE_CLIENT_SECRET** - Google OAuth client secret

## theHarvester API Keys

theHarvester uses these keys for premium data sources.

- **HUNTER_API_KEY** - Hunter.io email finder
- **BING_API_KEY** - Bing Search API
- **SHODAN_API_KEY** - Shodan search (shared with SpiderFoot)
- **SECURITYTRAILS_API_KEY** - SecurityTrails (shared with SpiderFoot)
- **ZOOMEYE_API_KEY** - ZoomEye (shared with SpiderFoot)
- **CENSYS_API_ID** / **CENSYS_API_SECRET** - Censys (shared with SpiderFoot)
- **INTELX_API_KEY** - IntelX (shared with SpiderFoot)
- **PASSIVETOTAL_API_USERNAME** / **PASSIVETOTAL_API_KEY** - PassiveTotal (shared with SpiderFoot)
- **GITHUB_API_KEY** - GitHub API (shared with SpiderFoot)
- **TWITTER_API_KEY** / **TWITTER_API_SECRET** - Twitter API credentials
- **TWITTER_ACCESS_TOKEN** / **TWITTER_ACCESS_SECRET** - Twitter OAuth tokens

## Getting API Keys

### Free Tier Available
- **Shodan**: Free tier with limited queries - https://account.shodan.io/register
- **VirusTotal**: Free tier - https://www.virustotal.com/gui/join-us
- **Have I Been Pwned**: Free tier - https://haveibeenpwned.com/API/Key
- **AbuseIPDB**: Free tier - https://www.abuseipdb.com/pricing
- **Censys**: Free tier - https://search.censys.io/register

### Paid Services
- **SecurityTrails**: https://securitytrails.com/
- **Hunter.io**: https://hunter.io/
- **PassiveTotal**: https://www.riskiq.com/products/passivetotal/
- **Google Custom Search**: https://developers.google.com/custom-search

## Usage Notes

1. **Not all keys are required** - Tools work with free sources by default
2. **Keys are optional** - Only add keys for services you want to use
3. **Remove placeholder values** - Delete keys you're not using or set to empty string
4. **Security** - Never commit `mcpServer.json` with real keys to version control

## Priority

When the same key is used by multiple tools (e.g., `SHODAN_API_KEY`), it's shared across all tools that support it. The environment variable is set once and available to all subprocesses.


