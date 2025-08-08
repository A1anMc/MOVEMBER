#!/usr/bin/env python3
"""
Movember AI Rules System - Data Scraper
Collects grants, research, and impact data from various web sources
"""

import asyncio
import aiohttp
import logging
import sqlite3
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import time
import random
import os
from urllib.parse import urljoin, urlparse
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MovemberDataScraper:
    """Data scraper for the Movember AI Rules System."""
    
    def __init__(self, db_path: str = "movember_ai.db"):
        self.db_path = db_path
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.rate_limit_delay = 2  # seconds between requests
        self.max_retries = 3
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def convert_to_uk_spelling(self, text: str) -> str:
        """Convert American spelling to UK spelling."""
        spelling_map = {
            'color': 'colour',
            'favor': 'favour',
            'center': 'centre',
            'theater': 'theatre',
            'realize': 'realise',
            'organize': 'organise',
            'analyze': 'analyse',
            'program': 'programme',
            'traveling': 'travelling',
            'counseling': 'counselling',
            'modeling': 'modelling',
            'labeling': 'labelling',
            'canceled': 'cancelled',
            'traveled': 'travelled',
            'modeled': 'modelled',
            'labeled': 'labelled'
        }
        
        converted_text = text
        for american, british in spelling_map.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(american) + r'\b'
            converted_text = re.sub(pattern, british, converted_text, flags=re.IGNORECASE)
        
        return converted_text
    
    def format_aud_currency(self, amount: float) -> str:
        """Format amount in AUD currency."""
        return f"A${amount:,.2f}"
    
    def extract_currency_amount(self, text: str) -> Optional[float]:
        """Extract currency amounts from text and convert to AUD."""
        # Common currency patterns
        patterns = [
            r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|dollars?)',  # 1,234.56 USD
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:AUD|Australian\s+dollars?)',  # 1,234.56 AUD
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:GBP|pounds?)',  # 1,234.56 GBP
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:EUR|euros?)',  # 1,234.56 EUR
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Convert to float and assume USD if no currency specified
                amount = float(matches[0].replace(',', ''))
                return amount  # For now, return as-is (would need exchange rates for conversion)
        
        return None
    
    def validate_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and score data quality."""
        score = 0
        issues = []
        
        # Check required fields
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                issues.append(f"Missing {field}")
            else:
                score += 25
        
        # Check UK spelling
        if 'description' in data and data['description']:
            original_text = data['description']
            uk_text = self.convert_to_uk_spelling(original_text)
            if original_text != uk_text:
                data['description'] = uk_text
                issues.append("Converted American spelling to UK spelling")
            score += 25
        
        # Check currency format
        if 'budget' in data and data['budget']:
            if isinstance(data['budget'], str):
                # Try to extract numeric value
                amount = self.extract_currency_amount(data['budget'])
                if amount:
                    data['budget'] = amount
                    data['budget_formatted'] = self.format_aud_currency(amount)
                    score += 25
            elif isinstance(data['budget'], (int, float)):
                data['budget_formatted'] = self.format_aud_currency(data['budget'])
                score += 25
        
        # Check for frameworks in impact reports
        if 'frameworks' in data and data['frameworks']:
            valid_frameworks = ['ToC', 'CEMP', 'SDG', 'Theory of Change', 'Common Evaluation and Measurement Protocol', 'Sustainable Development Goals']
            if any(framework in str(data['frameworks']) for framework in valid_frameworks):
                score += 25
        
        data['quality_score'] = score
        data['quality_issues'] = issues
        
        return data
    
    async def scrape_grants_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scrape grants data from configured sources."""
        logger.info(f"🕷️ Starting grants scraping from {len(config['sources'])} sources...")
        
        all_grants = []
        
        for source in config['sources']:
            try:
                logger.info(f"📄 Scraping grants from: {source['url']}")
                
                # Fetch the page
                async with self.session.get(source['url'], timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        grants = await self.parse_grants_page(html, source)
                        
                        # Validate and process each grant
                        for grant in grants:
                            grant = self.validate_data_quality(grant)
                            grant['source_url'] = source['url']
                            grant['scraped_at'] = datetime.now().isoformat()
                            all_grants.append(grant)
                        
                        logger.info(f"✅ Scraped {len(grants)} grants from {source['url']}")
                    else:
                        logger.warning(f"⚠️ Failed to fetch {source['url']}: {response.status}")
                
                # Rate limiting
                await asyncio.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"❌ Error scraping {source['url']}: {e}")
        
        # Store scraped data
        await self.store_scraped_data(all_grants, 'grants')
        
        return all_grants
    
    async def scrape_research_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scrape research data from configured sources."""
        logger.info(f"🔬 Starting research scraping from {len(config['sources'])} sources...")
        
        all_research = []
        
        for source in config['sources']:
            try:
                logger.info(f"📄 Scraping research from: {source['url']}")
                
                # Fetch the page
                async with self.session.get(source['url'], timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        research = await self.parse_research_page(html, source)
                        
                        # Validate and process each research item
                        for item in research:
                            item = self.validate_data_quality(item)
                            item['source_url'] = source['url']
                            item['scraped_at'] = datetime.now().isoformat()
                            all_research.append(item)
                        
                        logger.info(f"✅ Scraped {len(research)} research items from {source['url']}")
                    else:
                        logger.warning(f"⚠️ Failed to fetch {source['url']}: {response.status}")
                
                # Rate limiting
                await asyncio.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"❌ Error scraping {source['url']}: {e}")
        
        # Store scraped data
        await self.store_scraped_data(all_research, 'research')
        
        return all_research
    
    async def scrape_impact_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scrape impact data from configured sources."""
        logger.info(f"📊 Starting impact data scraping from {len(config['sources'])} sources...")
        
        all_impact = []
        
        for source in config['sources']:
            try:
                logger.info(f"📄 Scraping impact data from: {source['url']}")
                
                # Fetch the page
                async with self.session.get(source['url'], timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        impact_data = await self.parse_impact_page(html, source)
                        
                        # Validate and process each impact item
                        for item in impact_data:
                            item = self.validate_data_quality(item)
                            item['source_url'] = source['url']
                            item['scraped_at'] = datetime.now().isoformat()
                            all_impact.append(item)
                        
                        logger.info(f"✅ Scraped {len(impact_data)} impact items from {source['url']}")
                    else:
                        logger.warning(f"⚠️ Failed to fetch {source['url']}: {response.status}")
                
                # Rate limiting
                await asyncio.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"❌ Error scraping {source['url']}: {e}")
        
        # Store scraped data
        await self.store_scraped_data(all_impact, 'impact')
        
        return all_impact
    
    async def parse_grants_page(self, html: str, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse grants from HTML content."""
        grants = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Generic grant parsing (can be customized per source)
        grant_elements = soup.find_all(['div', 'article', 'section'], class_=re.compile(r'grant|funding|opportunity', re.I))
        
        for element in grant_elements:
            try:
                # Extract title
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                title = title_elem.get_text(strip=True) if title_elem else "Untitled Grant"
                
                # Extract description
                desc_elem = element.find(['p', 'div'], class_=re.compile(r'description|summary|content', re.I))
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract budget (look for currency patterns)
                budget_text = element.get_text()
                budget = self.extract_currency_amount(budget_text)
                
                # Extract organisation
                org_elem = element.find(['span', 'div'], class_=re.compile(r'organisation|organization|institution', re.I))
                organisation = org_elem.get_text(strip=True) if org_elem else "Unknown Organisation"
                
                if title and description:
                    grants.append({
                        'title': title,
                        'description': description,
                        'budget': budget,
                        'organisation': organisation,
                        'currency': 'AUD' if budget else None,
                        'timeline_months': 12,  # Default
                        'status': 'draft'
                    })
            
            except Exception as e:
                logger.warning(f"⚠️ Error parsing grant element: {e}")
        
        return grants
    
    async def parse_research_page(self, html: str, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse research data from HTML content."""
        research = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Generic research parsing
        research_elements = soup.find_all(['div', 'article', 'section'], class_=re.compile(r'research|study|publication', re.I))
        
        for element in research_elements:
            try:
                # Extract title
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                title = title_elem.get_text(strip=True) if title_elem else "Untitled Research"
                
                # Extract description
                desc_elem = element.find(['p', 'div'], class_=re.compile(r'abstract|summary|content', re.I))
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract authors
                author_elem = element.find(['span', 'div'], class_=re.compile(r'author|researcher', re.I))
                authors = author_elem.get_text(strip=True) if author_elem else "Unknown Authors"
                
                if title and description:
                    research.append({
                        'title': title,
                        'description': description,
                        'authors': authors,
                        'type': 'research',
                        'frameworks': ['ToC', 'CEMP'],  # Default frameworks
                        'status': 'draft'
                    })
            
            except Exception as e:
                logger.warning(f"⚠️ Error parsing research element: {e}")
        
        return research
    
    async def parse_impact_page(self, html: str, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse impact data from HTML content."""
        impact = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Generic impact parsing
        impact_elements = soup.find_all(['div', 'article', 'section'], class_=re.compile(r'impact|outcome|result', re.I))
        
        for element in impact_elements:
            try:
                # Extract title
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                title = title_elem.get_text(strip=True) if title_elem else "Untitled Impact Report"
                
                # Extract description
                desc_elem = element.find(['p', 'div'], class_=re.compile(r'description|summary|content', re.I))
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract frameworks
                frameworks = ['ToC', 'CEMP', 'SDG']  # Default frameworks
                framework_elem = element.find(['span', 'div'], class_=re.compile(r'framework|methodology', re.I))
                if framework_elem:
                    framework_text = framework_elem.get_text(strip=True)
                    if 'theory of change' in framework_text.lower():
                        frameworks = ['ToC']
                    elif 'cemp' in framework_text.lower():
                        frameworks = ['CEMP']
                    elif 'sdg' in framework_text.lower():
                        frameworks = ['SDG']
                
                if title and description:
                    impact.append({
                        'title': title,
                        'description': description,
                        'type': 'impact',
                        'frameworks': frameworks,
                        'status': 'draft'
                    })
            
            except Exception as e:
                logger.warning(f"⚠️ Error parsing impact element: {e}")
        
        return impact
    
    async def store_scraped_data(self, data: List[Dict[str, Any]], data_type: str):
        """Store scraped data in database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create scraped data table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraped_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_type TEXT,
                    raw_data_json TEXT,
                    processed_data_json TEXT,
                    quality_score REAL,
                    uk_spelling_issues INTEGER,
                    aud_currency_issues INTEGER,
                    total_records INTEGER,
                    valid_records INTEGER
                )
            """)
            
            # Calculate quality metrics
            total_records = len(data)
            valid_records = sum(1 for item in data if item.get('quality_score', 0) >= 75)
            uk_spelling_issues = sum(1 for item in data if 'quality_issues' in item and any('spelling' in issue for issue in item['quality_issues']))
            aud_currency_issues = sum(1 for item in data if 'quality_issues' in item and any('currency' in issue for issue in item['quality_issues']))
            
            # Store the data
            cursor.execute("""
                INSERT INTO scraped_data (
                    source_url, data_type, raw_data_json, processed_data_json,
                    quality_score, uk_spelling_issues, aud_currency_issues,
                    total_records, valid_records
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data[0]['source_url'] if data else '',
                data_type,
                json.dumps(data),
                json.dumps(data),  # Processed data is the same for now
                sum(item.get('quality_score', 0) for item in data) / max(len(data), 1),
                uk_spelling_issues,
                aud_currency_issues,
                total_records,
                valid_records
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"💾 Stored {total_records} {data_type} records (quality score: {sum(item.get('quality_score', 0) for item in data) / max(len(data), 1):.1f}%)")
            
        except Exception as e:
            logger.error(f"❌ Failed to store scraped data: {e}")
    
    def create_grants_scraping_config(self, base_url: str) -> Dict[str, Any]:
        """Create a configuration for grants scraping."""
        return {
            "type": "grants",
            "sources": [
                {
                    "url": base_url,
                    "selectors": {
                        "grant_container": "div.grant, article.grant, section.grant",
                        "title": "h1, h2, h3",
                        "description": "p.description, div.summary",
                        "budget": "span.budget, div.funding",
                        "organisation": "span.organisation, div.institution"
                    }
                }
            ]
        }
    
    def create_research_scraping_config(self, base_url: str) -> Dict[str, Any]:
        """Create a configuration for research scraping."""
        return {
            "type": "research",
            "sources": [
                {
                    "url": base_url,
                    "selectors": {
                        "research_container": "div.research, article.study, section.publication",
                        "title": "h1, h2, h3",
                        "description": "p.abstract, div.summary",
                        "authors": "span.author, div.researcher"
                    }
                }
            ]
        }
    
    def create_impact_scraping_config(self, base_url: str) -> Dict[str, Any]:
        """Create a configuration for impact data scraping."""
        return {
            "type": "impact",
            "sources": [
                {
                    "url": base_url,
                    "selectors": {
                        "impact_container": "div.impact, article.outcome, section.result",
                        "title": "h1, h2, h3",
                        "description": "p.description, div.summary",
                        "frameworks": "span.framework, div.methodology"
                    }
                }
            ]
        }

async def main():
    """Main function to run the data scraper."""
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Example scraping configuration
    grants_config = {
        "sources": [
            {"url": "https://example-grants-site.com/grants"},
            {"url": "https://another-grants-site.com/funding"}
        ]
    }
    
    research_config = {
        "sources": [
            {"url": "https://example-research-site.com/publications"},
            {"url": "https://another-research-site.com/studies"}
        ]
    }
    
    impact_config = {
        "sources": [
            {"url": "https://example-impact-site.com/reports"},
            {"url": "https://another-impact-site.com/outcomes"}
        ]
    }
    
    async with MovemberDataScraper() as scraper:
        logger.info("🕷️ Starting Movember Data Scraper...")
        
        # Scrape different types of data
        grants = await scraper.scrape_grants_data(grants_config)
        research = await scraper.scrape_research_data(research_config)
        impact = await scraper.scrape_impact_data(impact_config)
        
        logger.info(f"✅ Scraping completed - Grants: {len(grants)}, Research: {len(research)}, Impact: {len(impact)}")

if __name__ == "__main__":
    asyncio.run(main()) 