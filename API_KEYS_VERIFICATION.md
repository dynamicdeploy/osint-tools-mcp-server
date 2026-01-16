# API Keys Verification and Accuracy

## Important Note

After researching the actual tool documentation, I need to clarify how each tool **actually** reads API keys:

## theHarvester

**Actual Configuration Method**: Uses `api-keys.yaml` file, NOT environment variables directly.

**File Location**: `~/.config/theHarvester/api-keys.yaml` or in theHarvester directory

**Correct Format**:
```yaml
apikeys:
  bing:
    key: "YOUR_BING_API_KEY"
  hunter:
    key: "YOUR_HUNTER_API_KEY"
  shodan:
    key: "YOUR_SHODAN_API_KEY"
  github:
    key: "YOUR_GITHUB_API_KEY"
  virustotal:
    key: "YOUR_VIRUSTOTAL_API_KEY"
```

**Environment Variables**: The current implementation passes environment variables, but **theHarvester may not read them directly**. We need to either:
1. Create the `api-keys.yaml` file from environment variables, OR
2. Verify if theHarvester has been updated to support environment variables

**Verified Keys** (from official docs):
- `bing` (not `BING_API_KEY`)
- `hunter` (not `HUNTER_API_KEY`)
- `shodan` (not `SHODAN_API_KEY`)
- `github` (not `GITHUB_API_KEY`)
- `virustotal` (not `VIRUSTOTAL_API_KEY`)

## GHunt

**Actual Configuration Method**: Uses `.env` file in `/opt/ghunt/.env` or environment variables.

**Verified Keys** (from GHunt docs):
- `GOOGLE_API_KEY` ✅ (correct)
- `GOOGLE_CX` ✅ (correct - Custom Search Engine ID)
- `GOOGLE_CLIENT_ID` - May be used for OAuth
- `GOOGLE_CLIENT_SECRET` - May be used for OAuth

**Note**: GHunt primarily uses Google cookies for authentication, API keys are optional for enhanced searches.

## SpiderFoot

**Actual Configuration Method**: Uses web interface OR config file `/opt/spiderfoot/spiderfoot.cfg`

**Environment Variables**: SpiderFoot modules may read from environment variables, but this needs verification.

**Verified Keys** (common SpiderFoot modules):
- `SHODAN_API_KEY` - Likely correct (needs verification)
- `VIRUSTOTAL_API_KEY` - Likely correct (needs verification)
- Many others need verification against actual SpiderFoot module source code

## Issues with Current mcpServer.json

1. **theHarvester**: Environment variable names may not match what theHarvester expects
2. **SpiderFoot**: Many API key names are assumptions, not verified
3. **Some keys**: May be duplicates or incorrect format

## Recommended Action

We should:
1. **Verify** each tool's actual source code to see how they read API keys
2. **Update** the implementation to create config files if needed
3. **Test** with actual API keys to confirm functionality
4. **Document** the actual working configuration methods

## Current Status

⚠️ **The `mcpServer.json` file contains many unverified API key names.**

Many were added based on:
- Common naming conventions
- Assumptions about tool behavior
- General OSINT tool patterns

**Not all have been verified against actual tool documentation or source code.**

## Next Steps

1. Check theHarvester source code for environment variable support
2. Verify SpiderFoot module API key requirements
3. Test with actual keys to confirm
4. Update documentation with verified information


