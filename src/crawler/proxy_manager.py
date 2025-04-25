from typing import Dict, List
import aiohttp
import random
import asyncio

class ProxyManager:
    def __init__(self, proxy_configs: List[Dict]):
        self.proxies = proxy_configs
        self.current_index = 0
        self.lock = asyncio.Lock()
        
    async def test_proxy(self, proxy: Dict) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://httpbin.org/ip',
                    proxy=f"http://{proxy['host']}:{proxy['port']}",
                    timeout=5
                ) as response:
                    return response.status == 200
        except:
            return False
            
    async def get_next_proxy(self) -> Dict:
        async with self.lock:
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            
            # Test proxy before returning
            if await self.test_proxy(proxy):
                return proxy
                
            # If proxy fails, try next one
            return await self.get_next_proxy() 