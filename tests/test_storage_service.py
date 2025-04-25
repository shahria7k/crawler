import pytest
from unittest.mock import Mock, AsyncMock
from src.crawler.storage_service import StorageService

@pytest.fixture
def storage_service():
    # Mock MongoDB client
    mock_client = Mock()
    mock_client.company_crawler.companies = AsyncMock()
    mock_client.company_crawler.crawl_history = AsyncMock()
    
    service = StorageService('mongodb://test')
    service.client = mock_client
    service.companies = mock_client.company_crawler.companies
    service.crawl_history = mock_client.company_crawler.crawl_history
    
    return service

@pytest.mark.asyncio
async def test_store_company(storage_service):
    company_data = {
        'domain': 'example.com',
        'name': 'Test Company',
        'url': 'https://example.com'
    }
    
    await storage_service.store_company(company_data)
    
    # Verify that update_one was called
    storage_service.companies.update_one.assert_called_once()
    storage_service.crawl_history.insert_one.assert_called_once() 