from typing import List, Set, Dict
import asyncio
import logging
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup

class DiscoveryService:
    def __init__(self, seed_urls: List[str], allowed_domains: Set[str] = None):
        self.seed_urls = seed_urls
        self.allowed_domains = allowed_domains
        self.url_frontier = asyncio.Queue()
        self.visited_urls = set()
        self.priority_scores = {}
        
    async def initialize(self):
        for url in self.seed_urls:
            await self.url_frontier.put(url)
            self.priority_scores[url] = 1.0
            
    def is_allowed_domain(self, url: str) -> bool:
        if not self.allowed_domains:
            return True
        domain = urlparse(url).netloc
        return domain in self.allowed_domains
        
    async def extract_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                if self.is_allowed_domain(absolute_url):
                    links.append(absolute_url)
        return links
        
    async def add_urls(self, urls: List[str]):
        for url in urls:
            if url not in self.visited_urls:
                await self.url_frontier.put(url)
                
    async def get_next_url(self) -> str:
        return await self.url_frontier.get() 