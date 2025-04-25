import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, requests_per_second: float):
        self.delay = 1.0 / requests_per_second
        self.last_request = datetime.min
        self.lock = asyncio.Lock()
        
    async def acquire(self):
        async with self.lock:
            now = datetime.now()
            time_since_last = (now - self.last_request).total_seconds()
            if time_since_last < self.delay:
                await asyncio.sleep(self.delay - time_since_last)
            self.last_request = datetime.now()
            
    async def release(self):
        pass  # For compatibility with other rate limiters 