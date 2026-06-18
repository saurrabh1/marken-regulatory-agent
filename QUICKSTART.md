# 🚀 Quick Start Guide - Marken Regulatory Agent

Get the agent deployed in **5 minutes** with this streamlined guide.

## Prerequisites Check

```bash
# 1. Verify Python version (3.8+)
python --version

# 2. Verify orchestrate CLI is installed
orchestrate --version

# 3. Check available environments
orchestrate env list
```

## One-Command Deployment

### Option 1: Automated Script (Recommended)

```bash
cd marken_regulatory_agent
chmod +x deploy.sh
./deploy.sh
```

The script will:
- ✅ Install all dependencies (including Scrapling from GitHub)
- ✅ Import the tool to watsonx Orchestrate
- ✅ Import the agent configuration
- ✅ Verify successful deployment

### Option 2: Manual Step-by-Step

```bash
# Navigate to project
cd marken_regulatory_agent

# Install dependencies
pip install git+https://github.com/D4Vinci/Scrapling.git
pip install "scrapling[fetchers]"
scrapling install
pip install pdfplumber requests

# Activate environment
orchestrate env activate <your-environment-name>

# Import tool
orchestrate tools import -k python -f tools/regulatory_scraper.py -r requirements.txt

# Import agent
orchestrate agents import -f agent.yaml

# Verify
orchestrate agents list | grep marken_regulatory_agent
```

## Test the Agent

### Via UI (Best for Demo)

1. Open watsonx Orchestrate: `https://dl.watson-orchestrate.ibm.com`
2. Go to **Chat** → Search **"Marken Regulatory Agent"**
3. Try: *"What are the latest FDA drug guidance documents?"*

### Via CLI

```bash
orchestrate chat start
# Select: marken_regulatory_agent
# Type: What are the latest FDA drug guidance updates?
```

## Demo Video Script

**Perfect 2-minute demo flow:**

```
1. User: "What are the latest FDA drug guidance documents?"
   → Agent scrapes FDA.gov, extracts PDFs, returns structured summary

2. User: "Are any of these related to biosimilars?"
   → Agent uses memory to filter previous results

3. User: "Now check EMA for similar updates"
   → Agent scrapes EMA, shows multi-source capability
```

## Expected Output Example

```
Executive Summary:
The FDA has published 3 new draft guidance documents related to drug 
development. Two guidances have comment periods ending in Q2 2026.

Key Updates:
• Draft Guidance: Bioequivalence Studies with Pharmacokinetic Endpoints
  - Comment period ends: June 15, 2026
  - Affects: Generic drug applications
  
• Updated: Clinical Trial Considerations for Biosimilar Products
  - Effective immediately

Source: FDA Guidances for Drugs
Scraped: 2026-05-26
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `scrapling not found` | Run: `pip install git+https://github.com/D4Vinci/Scrapling.git` |
| `orchestrate not found` | Run: `pip install ibm-watsonx-orchestrate` |
| Tool not calling | Verify `style: react` in agent.yaml |
| Environment not active | Run: `orchestrate env activate <name>` |

## What Makes This Demo Impressive

✅ **Real-time data** - Not training data, actual live FDA/EMA content  
✅ **PDF extraction** - Reads actual guidance documents, not just links  
✅ **Multi-source** - Handles both FDA and EMA seamlessly  
✅ **Production-ready** - Error handling, rate limiting, clean output  
✅ **Adaptive scraping** - Uses Scrapling to bypass anti-bot systems  

## Next Steps

After successful deployment:

1. **Customize** the agent instructions in `agent.yaml`
2. **Adjust** `max_pdfs` parameter for performance tuning
3. **Add sources** by extending the tool with more URLs
4. **Integrate** with workflows using Flow Builder

## Support

- Full documentation: See `README.md`
- Tool code: `tools/regulatory_scraper.py`
- Agent config: `agent.yaml`

---

**Ready to impress Gargi and the Marken CEO! 🎬**