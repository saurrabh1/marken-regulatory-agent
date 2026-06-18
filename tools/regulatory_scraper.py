"""
Marken Regulatory Intelligence Tool
Scrapes FDA and EMA regulatory websites for guidance documents and PDFs
"""

import re
import requests
from typing import Optional
from bs4 import BeautifulSoup
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field

# Target URLs for regulatory sources
FDA_URL = "https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs"
EMA_URL = "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/scientific-guidelines"


class RegulatoryContent(BaseModel):
    """Structured output for regulatory content"""
    source: str = Field(description="Source of the content (FDA or EMA)")
    page_title: str = Field(description="Title of the main page")
    page_content: str = Field(description="Main text content from the page")
    pdf_summaries: list[str] = Field(description="List of extracted PDF content summaries")
    total_pdfs_found: int = Field(description="Total number of PDFs found on the page")
    total_pdfs_extracted: int = Field(description="Number of PDFs successfully extracted")


@tool
def scrape_regulatory_content(
    source: str = "fda",
    max_pdfs: int = 3
) -> str:
    """
    Scrapes regulatory guidance documents from FDA or EMA websites.
    
    This tool fetches the latest regulatory information directly from official government
    health authority websites. It extracts both the main page content and downloads/parses
    PDF guidance documents to provide comprehensive regulatory intelligence.
    
    Use this tool when users ask about:
    - Latest FDA drug guidance documents
    - Recent EMA scientific guidelines
    - New regulatory changes or updates
    - Compliance requirements for pharmaceuticals
    - Regulatory deadlines or effective dates
    
    Args:
        source: Either "fda", "ema", or a direct URL to scrape. Defaults to "fda".
        max_pdfs: Maximum number of PDFs to extract text from (for performance). Defaults to 3.
    
    Returns:
        A formatted string containing the page title, main content, and extracted PDF summaries.
    """
    
    # Determine target URL
    if source.lower() == "fda":
        target_url = FDA_URL
        source_name = "FDA"
    elif source.lower() == "ema":
        target_url = EMA_URL
        source_name = "EMA"
    elif source.startswith("http"):
        target_url = source
        source_name = "Custom URL"
    else:
        return f"Error: Invalid source '{source}'. Use 'fda', 'ema', or provide a direct URL."
    
    try:
        # Fetch the main page using requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(target_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract page title
        title_elem = soup.find('h1')
        page_title = title_elem.get_text(strip=True) if title_elem else "Regulatory Guidance Page"
        
        # Extract main text content (remove scripts, styles, navigation)
        # Get all paragraph text
        paragraphs = soup.find_all('p')
        main_content = "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # Limit main content to reasonable size
        if len(main_content) > 5000:
            main_content = main_content[:5000] + "...\n[Content truncated for brevity]"
        
        # Find all PDF links
        all_links = soup.find_all('a')
        pdf_links = []
        
        for link in all_links:
            href = link.get('href', '')
            if href.lower().endswith('.pdf'):
                # Make absolute URL if relative
                if not href.startswith('http'):
                    if href.startswith('/'):
                        base_url = '/'.join(target_url.split('/')[:3])
                        href = base_url + href
                    else:
                        href = target_url.rsplit('/', 1)[0] + '/' + href
                
                pdf_links.append({
                    'url': href,
                    'title': link.text.strip() or href.split('/')[-1]
                })
        
        total_pdfs_found = len(pdf_links)
        
        # Extract text from PDFs (limit to max_pdfs for performance)
        pdf_summaries = []
        pdfs_to_process = pdf_links[:max_pdfs]
        
        for idx, pdf_info in enumerate(pdfs_to_process, 1):
            try:
                # Import pdfplumber and io here to avoid import errors if not installed
                import pdfplumber
                import io
                
                # Download PDF (using requests from module-level import)
                pdf_response = requests.get(pdf_info['url'], timeout=30)
                pdf_response.raise_for_status()
                
                # Extract text using pdfplumber
                with pdfplumber.open(io.BytesIO(pdf_response.content)) as pdf:
                    # Extract text from first 3 pages only (for demo performance)
                    text_parts = []
                    for page_num, page in enumerate(pdf.pages[:3], 1):
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(f"[Page {page_num}]\n{page_text}")
                    
                    pdf_text = "\n\n".join(text_parts)
                    
                    # Limit PDF text size
                    if len(pdf_text) > 2000:
                        pdf_text = pdf_text[:2000] + "...\n[PDF content truncated]"
                    
                    pdf_summaries.append(
                        f"--- PDF {idx}: {pdf_info['title']} ---\n"
                        f"URL: {pdf_info['url']}\n\n"
                        f"{pdf_text}"
                    )
            
            except Exception as pdf_error:
                pdf_summaries.append(
                    f"--- PDF {idx}: {pdf_info['title']} ---\n"
                    f"URL: {pdf_info['url']}\n"
                    f"[Error extracting PDF: {str(pdf_error)}]"
                )
        
        # Build final output
        output_parts = [
            f"=" * 80,
            f"REGULATORY INTELLIGENCE REPORT",
            f"Source: {source_name}",
            f"URL: {target_url}",
            f"=" * 80,
            "",
            f"--- PAGE TITLE ---",
            page_title,
            "",
            f"--- PAGE CONTENT ---",
            main_content,
            "",
            f"--- PDF DOCUMENTS ---",
            f"Total PDFs found: {total_pdfs_found}",
            f"PDFs extracted: {len(pdf_summaries)}",
            ""
        ]
        
        if pdf_summaries:
            output_parts.extend(pdf_summaries)
        else:
            output_parts.append("[No PDFs were successfully extracted]")
        
        output_parts.append("")
        output_parts.append("=" * 80)
        output_parts.append(f"End of {source_name} Regulatory Report")
        output_parts.append("=" * 80)
        
        return "\n".join(output_parts)
    
    except Exception as e:
        return f"Error scraping {source_name}: {str(e)}\n\nPlease verify the URL is accessible and try again."


# For local testing
if __name__ == "__main__":
    print("Testing FDA scraper...")
    result = scrape_regulatory_content(source="fda", max_pdfs=2)
    print(result)
    print("\n" + "="*80 + "\n")
    print("Testing EMA scraper...")
    result = scrape_regulatory_content(source="ema", max_pdfs=2)
    print(result)

# Made with Bob
