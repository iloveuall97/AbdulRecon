import aiohttp
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

class SmartRequestHandler:
    """Handle HTTP requests with smart features"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = None
        self.timeout = config.get('scanner.request_timeout', 30)
        self.retry_attempts = config.get('scanner.retry_attempts', 3)
        self.delay = config.get('scanner.delay_between_requests', 1.0)
    
    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make GET request"""
        return await self._request('GET', url, **kwargs)
    
    async def post(self, url: str, data=None, **kwargs) -> Optional[Dict[str, Any]]:
        """Make POST request"""
        return await self._request('POST', url, data=data, **kwargs)
    
    async def _request(self, method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.retry_attempts):
            try:
                # Add delay
                await asyncio.sleep(self.delay)
                
                # Set default headers
                headers = kwargs.get('headers', {})
                if 'User-Agent' not in headers:
                    headers['User-Agent'] = self._get_random_user_agent()
                kwargs['headers'] = headers
                
                # Make request
                async with self.session.request(method, url, timeout=self.timeout, **kwargs) as resp:
                    return {
                        'status': resp.status,
                        'headers': dict(resp.headers),
                        'text': await resp.text(),
                        'content': await resp.read(),
                    }
            
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout on {method} {url} (attempt {attempt+1}/{self.retry_attempts})")
            except Exception as e:
                self.logger.warning(f"Error on {method} {url}: {e} (attempt {attempt+1}/{self.retry_attempts})")
                if attempt == self.retry_attempts - 1:
                    return None
        
        return None
    
    @staticmethod
    def _get_random_user_agent() -> str:
        """Get random user agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
        import random
        return random.choice(user_agents)