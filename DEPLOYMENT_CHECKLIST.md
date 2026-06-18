# ✅ Deployment Checklist - Marken Regulatory Agent

Use this checklist to ensure successful deployment to watsonx Orchestrate.

## Pre-Deployment

- [ ] Python 3.8+ installed (`python --version`)
- [ ] watsonx Orchestrate CLI installed (`orchestrate --version`)
- [ ] Environment configured and accessible (`orchestrate env list`)
- [ ] Internet connection available (for GitHub and package downloads)

## Installation Steps

- [ ] Navigate to project directory: `cd marken_regulatory_agent`
- [ ] Install Scrapling from GitHub: `pip install git+https://github.com/D4Vinci/Scrapling.git`
- [ ] Install Scrapling with fetchers: `pip install "scrapling[fetchers]"`
- [ ] Run Scrapling setup: `scrapling install`
- [ ] Install pdfplumber: `pip install pdfplumber`
- [ ] Install requests: `pip install requests`
- [ ] Verify ibm-watsonx-orchestrate is installed

## Environment Setup

- [ ] Activate environment: `orchestrate env activate <name>`
- [ ] Verify activation: `orchestrate env list` (should show active environment)
- [ ] Test connection: `orchestrate agents list` (should return without error)

## Tool Deployment

- [ ] Import tool: `orchestrate tools import -k python -f tools/regulatory_scraper.py -r requirements.txt`
- [ ] Verify tool import: `orchestrate tools list | grep scrape_regulatory_content`
- [ ] Check for import errors in output
- [ ] Confirm tool appears in list

## Agent Deployment

- [ ] Import agent: `orchestrate agents import -f agent.yaml`
- [ ] Verify agent import: `orchestrate agents list | grep marken_regulatory_agent`
- [ ] Check for import errors in output
- [ ] Confirm agent appears in list

## Testing - CLI

- [ ] Start chat: `orchestrate chat start`
- [ ] Select agent: `marken_regulatory_agent`
- [ ] Test FDA query: "What are the latest FDA drug guidance documents?"
- [ ] Verify tool is called (check output for tool invocation)
- [ ] Verify response includes:
  - [ ] Executive summary
  - [ ] Bullet-point list of updates
  - [ ] Source citation (FDA URL)
  - [ ] PDF content (if available)

## Testing - UI

- [ ] Log in to watsonx Orchestrate UI
- [ ] Navigate to Chat section
- [ ] Search for "Marken Regulatory Agent"
- [ ] Open agent chat
- [ ] Test FDA query: "What are the latest FDA drug guidance documents?"
- [ ] Verify response quality
- [ ] Test EMA query: "Summarize recent EMA scientific guidelines"
- [ ] Test follow-up: "Are any of these related to biosimilars?"

## Demo Preparation

- [ ] Test demo script (see QUICKSTART.md)
- [ ] Verify FDA query produces clean output
- [ ] Verify EMA query works
- [ ] Verify follow-up questions use memory
- [ ] Prepare talking points:
  - [ ] Real-time data (not training data)
  - [ ] PDF extraction capability
  - [ ] Multi-source support (FDA + EMA)
  - [ ] Production-ready error handling
  - [ ] Adaptive scraping (bypasses anti-bot)

## Troubleshooting Verification

- [ ] Test with invalid source: `scrape_regulatory_content(source="invalid")`
- [ ] Verify graceful error handling
- [ ] Test with unreachable URL
- [ ] Verify timeout handling

## Documentation Review

- [ ] README.md is complete and accurate
- [ ] QUICKSTART.md tested and verified
- [ ] deploy.sh script is executable (`chmod +x deploy.sh`)
- [ ] All file paths are correct

## Final Checks

- [ ] Agent responds within reasonable time (< 30 seconds)
- [ ] PDF extraction works (at least 1 PDF successfully parsed)
- [ ] Memory is working (follow-up questions reference previous context)
- [ ] Error messages are clear and helpful
- [ ] Output is formatted and readable

## Demo Day Checklist

- [ ] Environment is active and tested
- [ ] Agent is responding correctly
- [ ] Demo queries prepared and tested
- [ ] Backup plan if live scraping fails (screenshot of working output)
- [ ] Talking points memorized
- [ ] Questions anticipated and answers prepared

## Post-Demo

- [ ] Gather feedback from Gargi and CEO
- [ ] Note any issues or improvements needed
- [ ] Document any custom requests
- [ ] Plan next steps for production deployment

---

## Quick Reference Commands

```bash
# Activate environment
orchestrate env activate <name>

# List tools
orchestrate tools list

# List agents
orchestrate agents list

# Start chat
orchestrate chat start

# View logs (if available)
orchestrate logs follow

# Re-import tool (if changes made)
orchestrate tools import -k python -f tools/regulatory_scraper.py -r requirements.txt

# Re-import agent (if changes made)
orchestrate agents import -f agent.yaml
```

## Success Criteria

✅ Tool imports without errors  
✅ Agent imports without errors  
✅ Agent calls tool when asked about regulations  
✅ Tool successfully scrapes FDA and EMA  
✅ PDF extraction works (at least partially)  
✅ Output is structured and professional  
✅ Follow-up questions work (memory enabled)  
✅ Demo impresses stakeholders  

---

**When all boxes are checked, you're ready to demo! 🎬**