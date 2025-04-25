# Company Data Crawler 🕷️

A high-performance, distributed web crawler system designed to extract company information at scale. Built with Python's
modern async capabilities, this crawler efficiently discovers and processes company data from various online sources.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Capabilities

- ✨ Distributed crawling with multiple workers
- 🔄 Intelligent proxy rotation with health checks
- 🚦 Configurable rate limiting
- 🎯 Smart URL discovery and prioritization
- 📊 Structured data extraction
- 💾 MongoDB-based storage with deduplication
- 🛡️ Built-in fault tolerance and error handling

### Data Extraction

- Company profiles and metadata
- Contact information
- Technology stack detection
- Social media presence
- Employee information
- Location data

## Architecture

### Component Overview

```ascii
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Orchestrator  │────▶│ Discovery Service│────▶│ Crawler Service │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                              │
         │                                              ▼
         │                                    ┌─────────────────┐
         │                                    │ Parser Service  │
         │                                    └─────────────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────┐                          ┌─────────────────┐
│    MongoDB      │◀─────────────────────────│ Storage Service │
└─────────────────┘                          └─────────────────┘
```

### Key Components

1. **Orchestrator (`src/crawler/orchestrator.py`)**

   - Manages worker lifecycle
   - Coordinates services
   - Handles error recovery

2. **Discovery Service (`src/crawler/discovery_service.py`)**

   - URL frontier management
   - Domain filtering
   - Link extraction

3. **Crawler Service (`src/crawler/crawler_service.py`)**

   - Web page fetching
   - Proxy management
   - Rate limiting

4. **Parser Service (`src/crawler/parser_service.py`)**

   - HTML parsing
   - Data extraction
   - Format normalization

5. **Storage Service (`src/crawler/storage_service.py`)**
   - Data persistence
   - Deduplication
   - Index management

## Installation

### Prerequisites

- Python 3.8+
- MongoDB 4.0+
- Node.js (for Playwright)

### Setup Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/company-data-crawler.git
cd company-data-crawler
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

4. Configure MongoDB:

```bash
# Start MongoDB service
mongod --dbpath /path/to/data/db
```

## Configuration

### Basic Configuration

Edit `src/main.py`:

```python
config = {
    'mongodb_uri': 'mongodb://localhost:27017',
    'seed_urls': [
        'https://www.crunchbase.com',
        'https://angel.co',
    ],
    'allowed_domains': {
        'crunchbase.com',
        'angel.co',
    },
    'proxies': [
        {'id': 'proxy1', 'host': 'proxy1.example.com', 'port': 8080},
    ],
    'requests_per_second': 2,
    'worker_count': 5
}
```

## Usage

### Basic Usage

```bash
# Start the crawler
python src/main.py
```

### Monitoring

Monitor logs in real-time:

```bash
tail -f crawler.log
```

### Data Access

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.company_crawler

# Get all companies
companies = db.companies.find({})
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_crawler_service.py
```

### Test Files

- `test_crawler_service.py`: Tests web crawling functionality
- `test_discovery_service.py`: Tests URL management
- `test_parser_service.py`: Tests data extraction
- `test_storage_service.py`: Tests database operations

## API Documentation

### CrawlerService

```python
class CrawlerService:
    async def crawl_url(url: str) -> Dict:
        """
        Crawls a single URL and returns extracted data.

        Args:
            url (str): Target URL to crawl

        Returns:
            Dict: Extracted page data including metadata
        """
```

### DiscoveryService

```python
class DiscoveryService:
    async def add_urls(urls: List[str]):
        """
        Adds new URLs to the crawling frontier.

        Args:
            urls (List[str]): List of URLs to add
        """
```

### ParserService

```python
class ParserService:
    async def parse_company_data(html: str, url: str) -> Dict:
        """
        Extracts structured company data from HTML.

        Args:
            html (str): Raw HTML content
            url (str): Source URL

        Returns:
            Dict: Structured company data
        """
```

### StorageService

```python
class StorageService:
    async def store_company(company_data: Dict):
        """
        Stores or updates company data in MongoDB.

        Args:
            company_data (Dict): Company information to store
        """
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for new functions
- Add tests for new features

### Pull Request Process

1. Update documentation
2. Add tests
3. Update CHANGELOG.md
4. Submit PR with description

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Join our server](https://discord.gg/example)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/company-data-crawler/issues)

## Project Structure

```
company-data-crawler/
├── src/
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── crawler_service.py    # Web page fetching
│   │   ├── discovery_service.py  # URL management
│   │   ├── parser_service.py     # Data extraction
│   │   ├── storage_service.py    # MongoDB integration
│   │   ├── proxy_manager.py      # Proxy rotation
│   │   ├── rate_limiter.py       # Request throttling
│   │   └── orchestrator.py       # Coordination
│   └── main.py                   # Entry point
├── tests/
│   ├── __init__.py
│   ├── test_crawler_service.py
│   ├── test_discovery_service.py
│   ├── test_parser_service.py
│   └── test_storage_service.py
├── requirements.txt
└── README.MD



```
