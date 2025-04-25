import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from src.crawler.crawler_service import CrawlerService

@pytest.fixture
async def crawler_service():
    proxy_manager = Mock()
    proxy_manager.get_next_proxy = AsyncMock(return_value={'id': 'test_proxy', 'host': 'proxy.test', 'port': 8080})
    
    rate_limiter = Mock()
    rate_limiter.acquire = AsyncMock()
    rate_limiter.release = AsyncMock()
    
    service = CrawlerService(proxy_manager, rate_limiter)
    await service.setup()
    yield service
    # Cleanup
    await service.playwright.stop()

@pytest.mark.asyncio
async def test_crawl_url(crawler_service):
    url = "https://example.com"
    result = await crawler_service.crawl_url(url)
    
    assert result is not None
    assert 'url' in result
    assert 'title' in result
    assert 'meta_description' in result
    assert 'structured_data' in result
    assert 'crawled_at' in result
    assert 'proxy_used' in result 