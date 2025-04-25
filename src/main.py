import asyncio
import logging
from crawler.orchestrator import Orchestrator

async def main():
    config = {
        'mongodb_uri': 'mongodb://localhost:27017',
        'seed_urls': [
            'https://www.crunchbase.com',
            'https://angel.co',
            # Add more seed URLs
        ],
        'allowed_domains': {
            'crunchbase.com',
            'angel.co',
            # Add more allowed domains
        },
        'proxies': [
            {'id': 'proxy1', 'host': 'proxy1.example.com', 'port': 8080},
            # Add more proxies
        ],
        'requests_per_second': 2,
        'worker_count': 5
    }
    
    orchestrator = Orchestrator(config)
    await orchestrator.initialize()
    
    try:
        await orchestrator.start()
    except KeyboardInterrupt:
        await orchestrator.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) 