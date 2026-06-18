# 🚀 Deploy to Your watsonx Orchestrate Instance

This guide uses your specific instance credentials from `.env.sdk`.

## Your Instance Details

- **Instance URL**: `https://api.dl.watson-orchestrate.ibm.com/instances/20250520-0801-1088-20aa-664bdb7e0261`
- **API Key**: `azE6dXNyX2I3NDNjMmZmLTNhYjItMzM4Mi05ODYxLWY0NzljNzRlNjFkODpXbGh5SWM0bmFwSVI2TXhWU3ZVMnFlNndVSmRodWx2ZXZCcTNOT21Xd3ZJPTpDcElW`

## ✅ Prerequisites Complete

- [x] Scrapling installed from GitHub
- [x] All dependencies installed (pdfplumber, requests)
- [x] Scrapling setup complete (browser drivers installed)
- [x] Project files created

## 🎯 Deployment Steps

### Step 1: Add/Activate Environment

You have two options:

#### Option A: Use Existing Environment (if already configured)

```bash
# Check existing environments
orchestrate env list

# If you see an environment with your instance URL, activate it:
orchestrate env activate <environment-name>
```

#### Option B: Add New Environment

```bash
# Add new environment
orchestrate env add --name marken_saas --url https://api.dl.watson-orchestrate.ibm.com/instances/20250520-0801-1088-20aa-664bdb7e0261 --activate

# When prompted for API key, paste:
azE6dXNyX2I3NDNjMmZmLTNhYjItMzM4Mi05ODYxLWY0NzljNzRlNjFkODpXbGh5SWM0bmFwSVI2TXhWU3ZVMnFlNndVSmRodWx2ZXZCcTNOT21Xd3ZJPTpDcElW
```

### Step 2: Verify Environment is Active

```bash
orchestrate env list
```

You should see `(active)` next to your environment.

### Step 3: Import the Tool

```bash
cd marken_regulatory_agent
orchestrate tools import -k python -f tools/regulatory_scraper.py -r requirements.txt
```

**Expected Output:**
```
[INFO] - Using requirement file: "requirements.txt"
[INFO] - Tool 'scrape_regulatory_content' imported successfully
```

### Step 4: Verify Tool Import

```bash
orchestrate tools list | grep scrape_regulatory_content
```

You should see the tool in the list.

### Step 5: Import the Agent

```bash
orchestrate agents import -f agent.yaml
```

**Expected Output:**
```
[INFO] - Agent 'marken_regulatory_agent' imported successfully
```

### Step 6: Verify Agent Import

```bash
orchestrate agents list | grep marken_regulatory_agent
```

You should see the agent in the list.

## 🧪 Testing

### Test via CLI

```bash
orchestrate chat start
# Select: marken_regulatory_agent
# Type: What are the latest FDA drug guidance documents?
```

### Test via UI

1. Open: `https://dl.watson-orchestrate.ibm.com`
2. Navigate to **Chat**
3. Search for **"Marken Regulatory Agent"**
4. Try: *"What are the latest FDA drug guidance documents?"*

## 🎬 Demo Script

Perfect 2-minute demo for Gargi and the Marken CEO:

```
1. User: "What are the latest FDA drug guidance documents?"
   → Agent scrapes FDA.gov in real-time
   → Extracts PDF content
   → Returns structured summary

2. User: "Are any of these related to biosimilars?"
   → Demonstrates memory/context
   → Filters previous results

3. User: "Now check EMA for similar updates"
   → Shows multi-source capability
   → Compares FDA vs EMA
```

## 🔧 Troubleshooting

### Issue: Token Expired

```bash
# Reactivate environment
orchestrate env activate marken_saas
# Paste API key when prompted
```

### Issue: Tool Import Fails

```bash
# Verify you're in the right directory
pwd  # Should show: .../marken_regulatory_agent

# Verify file exists
ls -la tools/regulatory_scraper.py

# Try import again
orchestrate tools import -k python -f tools/regulatory_scraper.py -r requirements.txt
```

### Issue: Agent Not Calling Tool

```bash
# Check agent configuration
orchestrate agents get marken_regulatory_agent

# Verify tools list includes scrape_regulatory_content
```

## 📊 Expected Demo Output

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
URL: https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs
Scraped: 2026-05-26
```

## ✅ Success Checklist

- [ ] Environment activated successfully
- [ ] Tool imported without errors
- [ ] Agent imported without errors
- [ ] Tool appears in `orchestrate tools list`
- [ ] Agent appears in `orchestrate agents list`
- [ ] Agent responds to test query
- [ ] Agent calls the scraping tool
- [ ] PDF extraction works
- [ ] Output is structured and professional

## 🎯 Ready for Demo!

Once all checklist items are complete, you're ready to demo to Gargi and the Marken CEO!

---

**Need Help?**
- Check `README.md` for full documentation
- See `QUICKSTART.md` for 5-minute guide
- Review `DEPLOYMENT_CHECKLIST.md` for detailed steps