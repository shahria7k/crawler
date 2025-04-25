from playwright.async_api import async_playwright
from typing import Dict, List
import asyncio
import logging
from datetime import datetime

class CrawlerService:
    def __init__(self, proxy_manager, rate_limiter):
        self.proxy_manager = proxy_manager
        self.rate_limiter = rate_limiter
        self.browser_contexts = {}
        
    async def setup(self):
        self.playwright = await async_playwright().start()
        
    async def create_browser_context(self, proxy=None):
        browser = await self.playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            proxy=proxy,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        return context
        
    async def crawl_url(self, url: str) -> Dict:
        await self.rate_limiter.acquire()
        proxy = await self.proxy_manager.get_next_proxy()
        
        try:
            context = await self.create_browser_context(proxy)
            page = await context.new_page()
            
            await page.goto(url, wait_until='networkidle')
            
            # Extract basic metadata
            title = await page.title()
            meta_description = await page.evaluate('''
                () => document.querySelector('meta[name="description"]')?.content
            ''')
            
            # Extract structured data
            structured_data = await page.evaluate('''
                () => {
                    const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                    return Array.from(scripts).map(script => JSON.parse(script.textContent));
                }
            ''')
            
            return {
                'url': url,
                'title': title,
                'meta_description': meta_description,
                'structured_data': structured_data,
                'crawled_at': datetime.utcnow().isoformat(),
                'proxy_used': proxy['id']
            }
            
        except Exception as e:
            logging.error(f"Error crawling {url}: {str(e)}")
            return None
            
        finally:
            await context.close()
            await self.rate_limiter.release() 