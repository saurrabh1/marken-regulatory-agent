#!/bin/bash
# Marken Regulatory Agent - Deployment Script
# This script automates the deployment to watsonx Orchestrate

set -e  # Exit on error

echo "=========================================="
echo "Marken Regulatory Agent Deployment"
echo "=========================================="
echo ""

# Check if orchestrate CLI is available
if ! command -v orchestrate &> /dev/null; then
    echo "❌ Error: 'orchestrate' CLI not found"
    echo "   Install it with: pip install ibm-watsonx-orchestrate"
    exit 1
fi

echo "✓ orchestrate CLI found"
echo ""

# Check if environment is activated
echo "Checking environment status..."
orchestrate env list
echo ""

read -p "Is your environment activated? (y/n): " env_active
if [[ $env_active != "y" ]]; then
    echo ""
    echo "Please activate your environment first:"
    echo "  orchestrate env activate <your-environment-name>"
    echo ""
    echo "For local development:"
    echo "  orchestrate env activate local"
    exit 1
fi

echo ""
echo "=========================================="
echo "Step 1: Installing Dependencies"
echo "=========================================="
echo ""

# Install Scrapling from GitHub
echo "Installing Scrapling from GitHub..."
pip install git+https://github.com/D4Vinci/Scrapling.git

echo "Installing Scrapling with fetchers..."
pip install "scrapling[fetchers]"

echo "Running Scrapling setup..."
scrapling install

echo "Installing remaining dependencies..."
pip install pdfplumber requests

echo "✓ Dependencies installed"
echo ""

echo "=========================================="
echo "Step 2: Importing Tool"
echo "=========================================="
echo ""

# Import the tool
echo "Importing scrape_regulatory_content tool..."
orchestrate tools import -k python -f tools/regulatory_scraper.py -r requirements.txt

echo "✓ Tool imported"
echo ""

# Verify tool import
echo "Verifying tool import..."
orchestrate tools list | grep scrape_regulatory_content || echo "⚠️  Tool not found in list"
echo ""

echo "=========================================="
echo "Step 3: Importing Agent"
echo "=========================================="
echo ""

# Import the agent
echo "Importing marken_regulatory_agent..."
orchestrate agents import -f agent.yaml

echo "✓ Agent imported"
echo ""

# Verify agent import
echo "Verifying agent import..."
orchestrate agents list | grep marken_regulatory_agent || echo "⚠️  Agent not found in list"
echo ""

echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Test via UI:"
echo "   - Open watsonx Orchestrate UI"
echo "   - Navigate to Chat"
echo "   - Search for 'Marken Regulatory Agent'"
echo "   - Try: 'What are the latest FDA drug guidance documents?'"
echo ""
echo "2. Test via CLI:"
echo "   orchestrate chat start"
echo "   > Select 'marken_regulatory_agent'"
echo "   > What are the latest FDA drug guidance updates?"
echo ""
echo "3. For demo video:"
echo "   - Start with FDA query (clean output)"
echo "   - Show PDF extraction capability"
echo "   - Switch to EMA for variety"
echo ""
echo "=========================================="

# Made with Bob
