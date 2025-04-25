from typing import List, Dict
import asyncio
import logging
from datetime import datetime, timedelta

from .crawler_service import CrawlerService
from .discovery_service import DiscoveryService
from .parser_service import ParserService
from .storage_service import StorageService
from .proxy_manager import ProxyManager
from .rate_limiter import RateLimiter

class Orchestrator:
    def __init__(self, config: Dict):
        self.config = config
        self.running = False
        
        # Initialize services
        self.proxy_manager = ProxyManager(config['proxies'])
        self.rate_limiter = RateLimiter(config['requests_per_second'])
        self.crawler = CrawlerService(self.proxy_manager, self.rate_limiter)
        self.discovery = DiscoveryService(config['seed_urls'], config['allowed_domains'])
        self.parser = ParserService()
        self.storage = StorageService(config['mongodb_uri'])
        
        self.worker_count = config.get('worker_count', 5)
        
    async def initialize(self):
        await self.crawler.setup()
        await self.discovery.initialize()
        await self.storage.initialize()
        
    async def crawl_worker(self):
        while self.running:
            try:
                url = await self.discovery.get_next_url()
                
                # Crawl URL
                page_data = await self.crawler.crawl_url(url)
                if not page_data:
                    continue
                    
                # Parse company data
                company_data = await self.parser.parse_company_data(
                    page_data['html'],
                    url
                )
                
                # Store results
                await self.storage.store_company(company_data)
                
                # Discover new URLs
                new_urls = await self.discovery.extract_links(
                    page_data['html'],
                    url
                )
                await self.discovery.add_urls(new_urls)
                
            except Exception as e:
                logging.error(f"Worker error: {str(e)}")
                await asyncio.sleep(1)
                
    async def start(self):
        self.running = True
        
        # Start worker tasks
        workers = [
            asyncio.create_task(self.crawl_worker())
            for _ in range(self.worker_count)
        ]
        
        # Wait for workers
        await asyncio.gather(*workers)
        
    async def stop(self):
        self.running = False 