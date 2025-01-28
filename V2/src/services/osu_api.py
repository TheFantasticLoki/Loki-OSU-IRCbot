import aiohttp
from typing import Optional, Dict, Any

class OsuApiService:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self) -> None:
        self.session = aiohttp.ClientSession()
        await self.get_token()
        
    async def get_token(self) -> None:
        async with self.session.post(
            'https://osu.ppy.sh/oauth/token',
            json={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
                'scope': 'public'
            }
        ) as response:
            data = await response.json()
            self.token = data['access_token']
            
    async def get_user(self, username: str) -> Dict[str, Any]:
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self.session.get(
            f'https://osu.ppy.sh/api/v2/users/{username}',
            headers=headers
        ) as response:
            return await response.json()
