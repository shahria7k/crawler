from typing import Dict, Optional, List
import re
from bs4 import BeautifulSoup
import json

class ParserService:
    def __init__(self):
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.phone_pattern = re.compile(r'\+?[\d\s-]{10,}')
        
    async def parse_company_data(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract company data
        company_data = {
            'name': self._extract_company_name(soup),
            'description': self._extract_description(soup),
            'contact_info': self._extract_contact_info(soup),
            'social_links': self._extract_social_links(soup),
            'technologies': self._extract_technologies(soup),
            'employees': self._extract_employee_info(soup)
        }
        
        return company_data
        
    def _extract_company_name(self, soup: BeautifulSoup) -> Optional[str]:
        # Try multiple common locations
        og_title = soup.find('meta', property='og:title')
        if og_title:
            return og_title['content']
            
        h1 = soup.find('h1')
        if h1:
            return h1.text.strip()
            
        return None
        
    def _extract_technologies(self, soup: BeautifulSoup) -> List[str]:
        technologies = set()
        
        # Check meta tags
        meta_techs = soup.find_all('meta', attrs={'name': re.compile(r'technology|stack|framework', re.I)})
        for tech in meta_techs:
            technologies.add(tech.get('content'))
            
        # Check common technology indicators
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script['src'].lower()
            if 'react' in src:
                technologies.add('React')
            elif 'vue' in src:
                technologies.add('Vue.js')
            # Add more technology checks
            
        return list(technologies) 