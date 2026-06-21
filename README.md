# Marken Regulatory Agent

DEMO VIDEO [LINK](https://youtu.be/rTVyl07_-bc)

A specialized AI agent for monitoring and summarizing regulatory changes from FDA and EMA for the pharmaceutical and life sciences industry.

## 🎯 Overview

The Marken Regulatory Agent automatically scrapes public regulatory websites (FDA and EMA), extracts content from guidance documents and PDFs, and provides structured summaries of regulatory updates. Built for watsonx Orchestrate using the Agent Development Kit (ADK).

## ✨ Features

- **Real-time Regulatory Monitoring**: Scrapes live FDA and EMA websites
- **PDF Content Extraction**: Downloads and extracts text from guidance PDFs
- **Intelligent Summarization**: Provides executive summaries with key action items
- **Adaptive Scraping**: Uses Scrapling library to handle anti-bot systems and dynamic content
- **Production-Ready**: Handles errors gracefully, includes rate limiting considerations

## 📋 Prerequisites

- Python 3.8+
- IBM watsonx Orchestrate environment (SaaS or local)
- watsonx Orchestrate CLI installed (`pip install ibm-watsonx-orchestrate`)
- Active environment configured

## 🚀 Installation & Deployment

### Step 1: Install Scrapling from GitHub

Scrapling must be installed directly from GitHub to get the latest version:

```bash
# Navigate to the project directory
cd marken_regulatory_agent

# Install Scrapling from GitHub
pip install git+https://github.com/D4Vinci/Scrapling.git

# Install Scrapling with fetchers support
pip install "scrapling[fetchers]"

# Run Scrapling setup (installs browser drivers)
scrapling install

# Install remaining dependencies
pip install pdfplumber requests
```

### Step 2: Activate Your watsonx Orchestrate Environment

```bash
# List available environments
orchestrate env list

# Activate your environment (replace with your environment name)
orchestrate env activate <your-environment-name>

# For local development
orchestrate env activate local
```

### Step 3: Import the Regulatory Scraper Tool

```bash
# Import the Python tool
orchestrate tools import -k python -f tools/regulatory_scraper.py -r requirements.txt
```

**Expected Output:**
```
✓ Tool 'scrape_regulatory_content' imported successfully
```

### Step 4: Verify Tool Import

```bash
# List all tools to confirm
orchestrate tools list
```

You should see `scrape_regulatory_content` in the list.

### Step 5: Import the Agent

```bash
# Import the agent configuration
orchestrate agents import -f agent.yaml
```

**Expected Output:**
```
✓ Agent 'marken_regulatory_agent' imported successfully
```

### Step 6: Verify Agent Import

```bash
# List all agents to confirm
orchestrate agents list
```

You should see `marken_regulatory_agent` in the list.

## 🧪 Testing the Agent

### Option 1: Test via watsonx Orchestrate UI

1. Log in to your watsonx Orchestrate environment at:
   - **SaaS**: `https://dl.watson-orchestrate.ibm.com` (or your regional URL)
   - **Local**: `http://localhost:4321`

2. Navigate to **Chat** or **Orchestrate Chat** in the left sidebar

3. Search for **"Marken Regulatory Agent"** in the agent catalog

4. Click to open a chat session

5. Try these test prompts:
   - *"What are the latest FDA drug guidance documents?"*
   - *"Give me a summary of recent EMA scientific guidelines"*
   - *"Are there any new regulations related to biosimilars?"*

### Option 2: Test via CLI

```bash
# Start interactive chat
orchestrate chat start

# Select 'marken_regulatory_agent' from the list

# Type your query
> What are the latest FDA drug guidance updates?
```

## 📊 Expected Output

The agent will:

1. **Call the tool** to scrape the FDA or EMA website
2. **Extract content** from the main page and up to 3 PDFs
3. **Analyze** the content using the LLM
4. **Return** a structured summary with:
   - Executive summary (2-3 sentences)
   - Bullet-point list of key updates
   - Deadlines and effective dates
   - Source citation

**Example Response:**
```
Executive Summary:
The FDA has published 3 new draft guidance documents related to drug 
development, including updates to bioequivalence studies and clinical 
trial design. Two guidances have comment periods ending in Q2 2026.

Key Updates:
• Draft Guidance: Bioequivalence Studies with Pharmacokinetic Endpoints
  - Comment period ends: June 15, 2026
  - Affects: Generic drug applications
  
• Updated: Clinical Trial Considerations for Biosimilar Products
  - Effective immediately
  - Clarifies immunogenicity assessment requirements

Source: FDA Guidances for Drugs
URL: https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs
Scraped: 2026-05-26
```

## 🎬 Demo Video Tips

For the best demo experience:

1. **Start with FDA**: The FDA page produces clean, impressive output with real guidance titles
2. **Show PDF extraction**: Highlight that the agent reads actual PDF content, not just links
3. **Ask follow-up questions**: Demonstrate the agent's memory by asking clarifying questions
4. **Switch to EMA**: Show multi-source capability
5. **Highlight real-time**: Emphasize that this is live data, not training data

**Recommended Demo Flow:**
```
1. "What are the latest FDA drug guidance documents?"
   → Agent scrapes FDA, extracts PDFs, summarizes

2. "Are any of these related to clinical trials?"
   → Agent uses memory to filter previous results

3. "Now check the EMA for similar updates"
   → Agent scrapes EMA, compares with FDA findings
```

## 🔧 Troubleshooting

### Tool Import Fails

**Error:** `Module 'scrapling' not found`

**Solution:**
```bash
pip install git+https://github.com/D4Vinci/Scrapling.git
pip install "scrapling[fetchers]"
scrapling install
```

### Agent Not Calling Tool

**Issue:** Agent responds without using the tool

**Solution:** The agent is configured with `style: react` which enables tool calling. Verify:
```bash
orchestrate agents get marken_regulatory_agent
```

Check that `tools: [scrape_regulatory_content]` is present.

### PDF Extraction Fails

**Issue:** PDFs are found but text extraction fails

**Cause:** Some PDFs are scanned images without OCR text

**Behavior:** The agent will note the failure and continue with available content

### Rate Limiting

**Issue:** Scraping fails with 429 errors

**Solution:** The tool is configured to scrape conservatively (max 3 PDFs by default). For production, consider:
- Adding delays between requests
- Implementing caching
- Using the `max_pdfs` parameter to limit extraction

## 📁 Project Structure

```
marken_regulatory_agent/
├── tools/
│   └── regulatory_scraper.py    # Scrapling-based scraper tool
├── agent.yaml                    # Agent configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔐 Security Notes

- No API keys required (scrapes public websites)
- No authentication needed for FDA/EMA sites
- All data is publicly accessible regulatory information
- Tool runs in watsonx Orchestrate's secure execution environment

## 🌐 Target URLs

- **FDA**: https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs
- **EMA**: https://www.ema.europa.eu/en/human-regulatory-overview/research-development/scientific-guidelines

Both URLs are live, public, and contain real regulatory documents.

## 📚 Technical Details

### Scrapling Library

- **GitHub**: https://github.com/D4Vinci/Scrapling
- **Features**: Adaptive scraping, anti-bot handling, dynamic page support
- **License**: Open source (MIT)

### Tool Parameters

- `source`: `"fda"`, `"ema"`, or custom URL (default: `"fda"`)
- `max_pdfs`: Maximum PDFs to extract (default: `3`)

### LLM Configuration

- **Model**: `groq/openai/gpt-oss-120b`
- **Style**: `react` (enables tool calling)
- **Memory**: Enabled (maintains conversation context)

## 🎯 Use Cases

1. **Regulatory Intelligence**: Stay informed about new guidance documents
2. **Compliance Monitoring**: Track regulatory changes affecting your products
3. **Competitive Analysis**: Monitor industry-wide regulatory trends
4. **Due Diligence**: Research regulatory requirements for new markets
5. **Training**: Educate teams on current regulatory landscape

## 🚀 Next Steps

After successful deployment:

1. **Test thoroughly** with various queries
2. **Customize prompts** in `agent.yaml` for your specific needs
3. **Adjust `max_pdfs`** parameter based on performance requirements
4. **Add more sources** by extending the tool with additional URLs
5. **Integrate with workflows** using watsonx Orchestrate's flow builder

## 📞 Support

For issues or questions:
- Check watsonx Orchestrate documentation
- Review Scrapling GitHub issues
- Verify environment configuration with `orchestrate env list`

## 📄 License

This agent is provided as-is for use with IBM watsonx Orchestrate. Scrapling library is MIT licensed.

---

**Built for Marken | Powered by IBM watsonx Orchestrate**
