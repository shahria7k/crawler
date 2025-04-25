import pytest
from src.crawler.discovery_service import DiscoveryService

@pytest.fixture
def discovery_service():
    seed_urls = ['https://example.com']
    allowed_domains = {'example.com'}
    return DiscoveryService(seed_urls, allowed_domains)

@pytest.mark.asyncio
async def test_initialize(discovery_service):
    await discovery_service.initialize()
    url = await discovery_service.get_next_url()
    assert url == 'https://example.com'

def test_is_allowed_domain(discovery_service):
    assert discovery_service.is_allowed_domain('https://example.com/page')
    assert not discovery_service.is_allowed_domain('https://other.com/page')

@pytest.mark.asyncio
async def test_extract_links():
    service = DiscoveryService(['https://example.com'], {'example.com'})
    html = '''
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
            <a href="https://other.com/page3">Page 3</a>
        </body>
    </html>
    '''
    links = await service.extract_links(html, 'https://example.com')
    assert len(links) == 2  # Should only include example.com links 