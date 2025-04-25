import pytest
from src.crawler.parser_service import ParserService

@pytest.fixture
def parser_service():
    return ParserService()

@pytest.mark.asyncio
async def test_parse_company_data(parser_service):
    html = '''
    <html>
        <head>
            <meta property="og:title" content="Test Company">
            <meta name="description" content="Company description">
            <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
        </head>
        <body>
            <h1>Test Company</h1>
            <p>Contact: test@example.com</p>
            <a href="https://linkedin.com/company/test">LinkedIn</a>
        </body>
    </html>
    '''
    
    result = await parser_service.parse_company_data(html, 'https://example.com')
    
    assert result['name'] == 'Test Company'
    assert 'React' in result['technologies'] 