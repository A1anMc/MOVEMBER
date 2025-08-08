#!/usr/bin/env python3
"""
Movember AI Rules System - Data Scraper
Collects data from various sources with UK spelling and AUD currency standards.
"""

import asyncio
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import httpx
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import requests
from urllib.parse import urljoin, urlparse
import re
import os

from rules.domains.movember_ai.behaviours import convert_to_uk_spelling, format_aud_currency

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///movember_ai.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@dataclass
class ScrapingConfig:
    """Configuration for data scraping."""
    target_url: str
    selectors: Dict[str, str]
    data_mapping: Dict[str, str]
    rate_limit: float = 1.0  # requests per second
    max_pages: int = 10
    timeout: int = 30
    user_agent: str = "Movember AI Data Scraper"
    authentication: Optional[Dict] = None
    pagination: Optional[Dict] = None
    filters: Optional[Dict] = None
    uk_spelling_conversion: bool = True
    aud_currency_conversion: bool = True


@dataclass
class ScrapedData:
    """Structure for scraped data."""
    source_url: str
    timestamp: datetime
    data_type: str
    raw_data: Dict
    processed_data: Dict
    quality_score: float
    uk_spelling_issues: int
    aud_currency_issues: int
    total_records: int
    valid_records: int


class MovemberDataScraper:
    """Data scraper for Movember AI Rules System."""
    
    def __init__(self):
        self.db = SessionLocal()
        self.logger = logging.getLogger(__name__)
        self.session = None
        self.scraping_history = []
        
        # Common selectors for different data sources
        self.common_selectors = {
            "grants": {
                "title": "h1, h2, .title, .grant-title",
                "description": ".description, .summary, .content",
                "budget": ".budget, .amount, .funding",
                "organisation": ".organisation, .institution, .applicant",
                "deadline": ".deadline, .due-date, .closing-date",
                "contact": ".contact, .email, .phone"
            },
            "research": {
                "title": "h1, h2, .title, .research-title",
                "abstract": ".abstract, .summary, .description",
                "authors": ".authors, .researchers, .team",
                "institution": ".institution, .university, .organisation",
                "publication_date": ".date, .published, .publication-date",
                "keywords": ".keywords, .tags, .topics"
            },
            "impact_reports": {
                "title": "h1, h2, .title, .report-title",
                "summary": ".summary, .executive-summary, .overview",
                "metrics": ".metrics, .outcomes, .results",
                "methodology": ".methodology, .approach, .methods",
                "conclusions": ".conclusions, .findings, .results",
                "recommendations": ".recommendations, .suggestions"
            }
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            headers={"User-Agent": "Movember AI Data Scraper"},
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def scrape_grants_data(self, config: ScrapingConfig) -> ScrapedData:
        """Scrape grants data from specified source."""
        try:
            self.logger.info(f"Starting grants data scraping from: {config.target_url}")
            
            # Scrape data
            raw_data = await self._scrape_pages(config)
            
            # Process and validate data
            processed_data = await self._process_grants_data(raw_data, config)
            
            # Calculate quality metrics
            quality_metrics = await self._calculate_quality_metrics(processed_data)
            
            scraped_data = ScrapedData(
                source_url=config.target_url,
                timestamp=datetime.now(),
                data_type="grants",
                raw_data=raw_data,
                processed_data=processed_data,
                quality_score=quality_metrics["quality_score"],
                uk_spelling_issues=quality_metrics["uk_spelling_issues"],
                aud_currency_issues=quality_metrics["aud_currency_issues"],
                total_records=len(raw_data),
                valid_records=quality_metrics["valid_records"]
            )
            
            # Store scraped data
            await self._store_scraped_data(scraped_data)
            
            self.logger.info(f"Grants data scraping completed: {len(processed_data)} records")
            return scraped_data
        
        except Exception as e:
            self.logger.error(f"Error scraping grants data: {str(e)}")
            raise
    
    async def scrape_research_data(self, config: ScrapingConfig) -> ScrapedData:
        """Scrape research data from specified source."""
        try:
            self.logger.info(f"Starting research data scraping from: {config.target_url}")
            
            # Scrape data
            raw_data = await self._scrape_pages(config)
            
            # Process and validate data
            processed_data = await self._process_research_data(raw_data, config)
            
            # Calculate quality metrics
            quality_metrics = await self._calculate_quality_metrics(processed_data)
            
            scraped_data = ScrapedData(
                source_url=config.target_url,
                timestamp=datetime.now(),
                data_type="research",
                raw_data=raw_data,
                processed_data=processed_data,
                quality_score=quality_metrics["quality_score"],
                uk_spelling_issues=quality_metrics["uk_spelling_issues"],
                aud_currency_issues=quality_metrics["aud_currency_issues"],
                total_records=len(raw_data),
                valid_records=quality_metrics["valid_records"]
            )
            
            # Store scraped data
            await self._store_scraped_data(scraped_data)
            
            self.logger.info(f"Research data scraping completed: {len(processed_data)} records")
            return scraped_data
        
        except Exception as e:
            self.logger.error(f"Error scraping research data: {str(e)}")
            raise
    
    async def scrape_impact_data(self, config: ScrapingConfig) -> ScrapedData:
        """Scrape impact data from specified source."""
        try:
            self.logger.info(f"Starting impact data scraping from: {config.target_url}")
            
            # Scrape data
            raw_data = await self._scrape_pages(config)
            
            # Process and validate data
            processed_data = await self._process_impact_data(raw_data, config)
            
            # Calculate quality metrics
            quality_metrics = await self._calculate_quality_metrics(processed_data)
            
            scraped_data = ScrapedData(
                source_url=config.target_url,
                timestamp=datetime.now(),
                data_type="impact",
                raw_data=raw_data,
                processed_data=processed_data,
                quality_score=quality_metrics["quality_score"],
                uk_spelling_issues=quality_metrics["uk_spelling_issues"],
                aud_currency_issues=quality_metrics["aud_currency_issues"],
                total_records=len(raw_data),
                valid_records=quality_metrics["valid_records"]
            )
            
            # Store scraped data
            await self._store_scraped_data(scraped_data)
            
            self.logger.info(f"Impact data scraping completed: {len(processed_data)} records")
            return scraped_data
        
        except Exception as e:
            self.logger.error(f"Error scraping impact data: {str(e)}")
            raise
    
    async def _scrape_pages(self, config: ScrapingConfig) -> List[Dict]:
        """Scrape data from multiple pages."""
        scraped_data = []
        current_page = 1
        
        while current_page <= config.max_pages:
            try:
                # Construct URL for current page
                if config.pagination:
                    page_url = self._construct_page_url(config.target_url, current_page, config.pagination)
                else:
                    page_url = config.target_url
                
                # Scrape single page
                page_data = await self._scrape_single_page(page_url, config)
                
                if not page_data:
                    break  # No more data
                
                scraped_data.extend(page_data)
                
                # Rate limiting
                await asyncio.sleep(1 / config.rate_limit)
                
                current_page += 1
                
            except Exception as e:
                self.logger.error(f"Error scraping page {current_page}: {str(e)}")
                break
        
        return scraped_data
    
    async def _scrape_single_page(self, url: str, config: ScrapingConfig) -> List[Dict]:
        """Scrape data from a single page."""
        try:
            # Make request
            headers = {"User-Agent": config.user_agent}
            if config.authentication:
                headers.update(config.authentication)
            
            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    self.logger.warning(f"HTTP {response.status} for {url}")
                    return []
                
                content = await response.text()
            
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract data using selectors
            extracted_data = []
            
            # Find all data containers (adjust selector based on source)
            containers = soup.select(config.selectors.get("container", "div"))
            
            for container in containers:
                item_data = {}
                
                for field, selector in config.selectors.items():
                    if field == "container":
                        continue
                    
                    elements = container.select(selector)
                    if elements:
                        # Extract text content
                        text_content = " ".join([elem.get_text(strip=True) for elem in elements])
                        item_data[field] = text_content
                
                if item_data:  # Only add if we found some data
                    extracted_data.append(item_data)
            
            return extracted_data
        
        except Exception as e:
            self.logger.error(f"Error scraping page {url}: {str(e)}")
            return []
    
    def _construct_page_url(self, base_url: str, page: int, pagination_config: Dict) -> str:
        """Construct URL for specific page number."""
        if pagination_config.get("type") == "query_param":
            param_name = pagination_config.get("param_name", "page")
            separator = "&" if "?" in base_url else "?"
            return f"{base_url}{separator}{param_name}={page}"
        elif pagination_config.get("type") == "path":
            pattern = pagination_config.get("pattern", "/page/{page}")
            return base_url + pattern.format(page=page)
        else:
            return base_url
    
    async def _process_grants_data(self, raw_data: List[Dict], config: ScrapingConfig) -> List[Dict]:
        """Process and validate grants data."""
        processed_data = []
        
        for item in raw_data:
            processed_item = {}
            
            # Map fields according to configuration
            for source_field, target_field in config.data_mapping.items():
                if source_field in item:
                    processed_item[target_field] = item[source_field]
            
            # Apply UK spelling conversion
            if config.uk_spelling_conversion:
                for field in ["title", "description", "summary", "organisation"]:
                    if field in processed_item:
                        processed_item[field] = convert_to_uk_spelling(processed_item[field])
            
            # Apply AUD currency conversion
            if config.aud_currency_conversion:
                for field in ["budget", "amount", "funding"]:
                    if field in processed_item:
                        processed_item[field] = self._convert_to_aud_currency(processed_item[field])
            
            # Add metadata
            processed_item["scraped_at"] = datetime.now().isoformat()
            processed_item["source_url"] = config.target_url
            processed_item["currency"] = "AUD"
            processed_item["spelling_standard"] = "UK"
            
            processed_data.append(processed_item)
        
        return processed_data
    
    async def _process_research_data(self, raw_data: List[Dict], config: ScrapingConfig) -> List[Dict]:
        """Process and validate research data."""
        processed_data = []
        
        for item in raw_data:
            processed_item = {}
            
            # Map fields according to configuration
            for source_field, target_field in config.data_mapping.items():
                if source_field in item:
                    processed_item[target_field] = item[source_field]
            
            # Apply UK spelling conversion
            if config.uk_spelling_conversion:
                for field in ["title", "abstract", "description", "institution"]:
                    if field in processed_item:
                        processed_item[field] = convert_to_uk_spelling(processed_item[field])
            
            # Add metadata
            processed_item["scraped_at"] = datetime.now().isoformat()
            processed_item["source_url"] = config.target_url
            processed_item["spelling_standard"] = "UK"
            
            processed_data.append(processed_item)
        
        return processed_data
    
    async def _process_impact_data(self, raw_data: List[Dict], config: ScrapingConfig) -> List[Dict]:
        """Process and validate impact data."""
        processed_data = []
        
        for item in raw_data:
            processed_item = {}
            
            # Map fields according to configuration
            for source_field, target_field in config.data_mapping.items():
                if source_field in item:
                    processed_item[target_field] = item[source_field]
            
            # Apply UK spelling conversion
            if config.uk_spelling_conversion:
                for field in ["title", "summary", "methodology", "conclusions", "recommendations"]:
                    if field in processed_item:
                        processed_item[field] = convert_to_uk_spelling(processed_item[field])
            
            # Apply AUD currency conversion for financial metrics
            if config.aud_currency_conversion:
                for field in ["cost", "budget", "funding"]:
                    if field in processed_item:
                        processed_item[field] = self._convert_to_aud_currency(processed_item[field])
            
            # Add metadata
            processed_item["scraped_at"] = datetime.now().isoformat()
            processed_item["source_url"] = config.target_url
            processed_item["currency"] = "AUD"
            processed_item["spelling_standard"] = "UK"
            
            processed_data.append(processed_item)
        
        return processed_data
    
    def _convert_to_aud_currency(self, value: str) -> str:
        """Convert currency values to AUD format."""
        try:
            # Extract numeric value
            numeric_value = re.findall(r'[\d,]+\.?\d*', value)
            if numeric_value:
                # Remove commas and convert to float
                amount = float(numeric_value[0].replace(',', ''))
                return format_aud_currency(amount)
            else:
                return value
        except (ValueError, TypeError):
            return value
    
    async def _calculate_quality_metrics(self, processed_data: List[Dict]) -> Dict:
        """Calculate quality metrics for scraped data."""
        total_records = len(processed_data)
        uk_spelling_issues = 0
        aud_currency_issues = 0
        valid_records = 0
        
        for item in processed_data:
            # Check UK spelling
            text_fields = ["title", "description", "summary", "organisation", "abstract", "methodology"]
            for field in text_fields:
                if field in item and self._contains_american_spelling(item[field]):
                    uk_spelling_issues += 1
                    break
            
            # Check AUD currency
            currency_fields = ["budget", "amount", "funding", "cost"]
            for field in currency_fields:
                if field in item and not self._is_aud_currency(item[field]):
                    aud_currency_issues += 1
                    break
            
            # Count valid records
            if "title" in item and item["title"]:
                valid_records += 1
        
        # Calculate quality score
        spelling_score = 1.0 - (uk_spelling_issues / total_records) if total_records > 0 else 1.0
        currency_score = 1.0 - (aud_currency_issues / total_records) if total_records > 0 else 1.0
        completeness_score = valid_records / total_records if total_records > 0 else 0.0
        
        quality_score = (spelling_score + currency_score + completeness_score) / 3
        
        return {
            "quality_score": quality_score,
            "uk_spelling_issues": uk_spelling_issues,
            "aud_currency_issues": aud_currency_issues,
            "valid_records": valid_records,
            "spelling_score": spelling_score,
            "currency_score": currency_score,
            "completeness_score": completeness_score
        }
    
    def _contains_american_spelling(self, text: str) -> bool:
        """Check if text contains American spelling."""
        american_spellings = [
            'color', 'behavior', 'organization', 'realize', 'analyze',
            'center', 'meter', 'program', 'license', 'defense', 'offense',
            'specialize', 'standardize', 'optimize', 'customize', 'summarize',
            'categorize', 'prioritize'
        ]
        
        text_lower = text.lower()
        return any(spelling in text_lower for spelling in american_spellings)
    
    def _is_aud_currency(self, value: str) -> bool:
        """Check if value is in AUD currency format."""
        return "A$" in value or "AUD" in value.upper()
    
    async def _store_scraped_data(self, scraped_data: ScrapedData):
        """Store scraped data in database."""
        try:
            with self.db.begin():
                self.db.execute(text("""
                    INSERT INTO scraped_data (
                        source_url, timestamp, data_type, raw_data_json, processed_data_json,
                        quality_score, uk_spelling_issues, aud_currency_issues,
                        total_records, valid_records
                    ) VALUES (
                        :source_url, :timestamp, :data_type, :raw_data_json, :processed_data_json,
                        :quality_score, :uk_spelling_issues, :aud_currency_issues,
                        :total_records, :valid_records
                    )
                """), {
                    "source_url": scraped_data.source_url,
                    "timestamp": scraped_data.timestamp,
                    "data_type": scraped_data.data_type,
                    "raw_data_json": json.dumps(scraped_data.raw_data),
                    "processed_data_json": json.dumps(scraped_data.processed_data),
                    "quality_score": scraped_data.quality_score,
                    "uk_spelling_issues": scraped_data.uk_spelling_issues,
                    "aud_currency_issues": scraped_data.aud_currency_issues,
                    "total_records": scraped_data.total_records,
                    "valid_records": scraped_data.valid_records
                })
        except Exception as e:
            self.logger.error(f"Error storing scraped data: {str(e)}")
    
    def get_scraping_history(self) -> List[ScrapedData]:
        """Get scraping history."""
        return self.scraping_history
    
    def create_grants_scraping_config(self, target_url: str) -> ScrapingConfig:
        """Create configuration for scraping grants data."""
        return ScrapingConfig(
            target_url=target_url,
            selectors={
                "container": ".grant-item, .funding-opportunity, .grant",
                "title": ".title, .grant-title, h2, h3",
                "description": ".description, .summary, .content",
                "budget": ".budget, .amount, .funding-amount",
                "organisation": ".organisation, .institution, .applicant",
                "deadline": ".deadline, .due-date, .closing-date",
                "contact": ".contact, .email, .phone"
            },
            data_mapping={
                "title": "title",
                "description": "description",
                "budget": "budget",
                "organisation": "organisation",
                "deadline": "deadline",
                "contact": "contact"
            },
            rate_limit=1.0,
            max_pages=10,
            uk_spelling_conversion=True,
            aud_currency_conversion=True
        )
    
    def create_research_scraping_config(self, target_url: str) -> ScrapingConfig:
        """Create configuration for scraping research data."""
        return ScrapingConfig(
            target_url=target_url,
            selectors={
                "container": ".research-item, .publication, .study",
                "title": ".title, .research-title, h2, h3",
                "abstract": ".abstract, .summary, .description",
                "authors": ".authors, .researchers, .team",
                "institution": ".institution, .university, .organisation",
                "publication_date": ".date, .published, .publication-date",
                "keywords": ".keywords, .tags, .topics"
            },
            data_mapping={
                "title": "title",
                "abstract": "abstract",
                "authors": "authors",
                "institution": "institution",
                "publication_date": "publication_date",
                "keywords": "keywords"
            },
            rate_limit=1.0,
            max_pages=10,
            uk_spelling_conversion=True,
            aud_currency_conversion=False
        )
    
    def create_impact_scraping_config(self, target_url: str) -> ScrapingConfig:
        """Create configuration for scraping impact data."""
        return ScrapingConfig(
            target_url=target_url,
            selectors={
                "container": ".impact-item, .report, .study",
                "title": ".title, .report-title, h2, h3",
                "summary": ".summary, .executive-summary, .overview",
                "metrics": ".metrics, .outcomes, .results",
                "methodology": ".methodology, .approach, .methods",
                "conclusions": ".conclusions, .findings, .results",
                "recommendations": ".recommendations, .suggestions"
            },
            data_mapping={
                "title": "title",
                "summary": "summary",
                "metrics": "metrics",
                "methodology": "methodology",
                "conclusions": "conclusions",
                "recommendations": "recommendations"
            },
            rate_limit=1.0,
            max_pages=10,
            uk_spelling_conversion=True,
            aud_currency_conversion=True
        )


async def main():
    """Main function to run the data scraper."""
    async with MovemberDataScraper() as scraper:
        # Example: Scrape grants data
        grants_config = scraper.create_grants_scraping_config("https://example-grants-site.com")
        grants_data = await scraper.scrape_grants_data(grants_config)
        
        # Example: Scrape research data
        research_config = scraper.create_research_scraping_config("https://example-research-site.com")
        research_data = await scraper.scrape_research_data(research_config)
        
        # Example: Scrape impact data
        impact_config = scraper.create_impact_scraping_config("https://example-impact-site.com")
        impact_data = await scraper.scrape_impact_data(impact_config)
        
        print(f"Scraped {grants_data.total_records} grants records")
        print(f"Scraped {research_data.total_records} research records")
        print(f"Scraped {impact_data.total_records} impact records")


if __name__ == "__main__":
    asyncio.run(main()) 