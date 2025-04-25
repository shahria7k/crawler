from typing import Dict, List
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import logging

class StorageService:
    def __init__(self, mongodb_uri: str):
        self.client = AsyncIOMotorClient(mongodb_uri)
        self.db = self.client.company_crawler
        self.companies = self.db.companies
        self.crawl_history = self.db.crawl_history
        
    async def initialize(self):
        # Create indexes
        await self.companies.create_index('domain', unique=True)
        await self.companies.create_index('last_crawled')
        await self.crawl_history.create_index('url')
        
    async def store_company(self, company_data: Dict):
        try:
            # Update or insert company data
            result = await self.companies.update_one(
                {'domain': company_data['domain']},
                {
                    '$set': {
                        **company_data,
                        'last_updated': datetime.utcnow()
                    }
                },
                upsert=True
            )
            
            # Store crawl history
            await self.crawl_history.insert_one({
                'url': company_data['url'],
                'crawled_at': datetime.utcnow(),
                'success': True
            })
            
            return result
            
        except Exception as e:
            logging.error(f"Error storing company data: {str(e)}")
            raise 