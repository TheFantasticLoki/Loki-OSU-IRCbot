import aiohttp
from typing import Optional, Dict, Any

class OsuApiService:
    """
    A service class for interacting with the osu! API v2.
    
    This class handles authentication and API requests to the osu! API,
    providing methods to fetch user data and manage OAuth2 tokens.
    
    Attributes:
        client_id (str): The OAuth2 client ID for the osu! API
        client_secret (str): The OAuth2 client secret for the osu! API
        token (Optional[str]): The current OAuth2 access token
        session (Optional[aiohttp.ClientSession]): The HTTP session for making requests
    """
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize the OsuApiService with client credentials.
        
        Args:
            client_id (str): The OAuth2 client ID obtained from osu!
            client_secret (str): The OAuth2 client secret obtained from osu!
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self) -> None:
        """
        Initialize the API service by creating a new HTTP session and obtaining an access token.
        
        This method should be called before making any API requests.
        
        Returns:
            None
        """
        self.session = aiohttp.ClientSession()
        await self.get_token()
        
    async def get_token(self) -> None:
        """
        Obtain a new OAuth2 access token from the osu! API.
        
        This method makes a POST request to the osu! OAuth endpoint to get
        a new access token using the client credentials flow.
        
        Returns:
            None
        
        Note:
            The obtained token is stored in the instance's token attribute.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
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
        """
        Fetch user information from the osu! API.
        
        This method retrieves detailed information about a specific user
        using their username.
        
        Args:
            username (str): The username of the osu! player to look up
            
        Returns:
            Dict[str, Any]: A dictionary containing the user's information
                           as returned by the osu! API
        
        Note:
            Requires a valid access token to be present in the instance.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self.session.get(
            f'https://osu.ppy.sh/api/v2/users/{username}',
            headers=headers
        ) as response:
            return await response.json()
    async def get_user_best(self, user_id: int, limit: int = 1) -> Dict[str, Any]:
        """
        Fetch a user's best scores from the osu! API.
        
        Args:
            user_id (int): The user's osu! ID
            limit (int): Number of scores to retrieve (default: 1)
            
        Returns:
            Dict[str, Any]: The user's top scores as returned by the API
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
            
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self.session.get(
            f'https://osu.ppy.sh/api/v2/users/{user_id}/scores/best',
            params={'limit': limit},
            headers=headers
        ) as response:
            scores = await response.json()
            return scores[0] if limit == 1 else scores
    async def get_user_recent(self, user_id: int, limit: int = 1) -> Dict[str, Any]:
        """
        Fetch a user's recent scores from the osu! API.
        
        Args:
            user_id (int): The user's osu! ID
            limit (int): Number of scores to retrieve (default: 1)
                
        Returns:
            Dict[str, Any]: The user's recent scores as returned by the API
            
        Raises:
            ValueError: If user has no recent plays
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
                
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self.session.get(
            f'https://osu.ppy.sh/api/v2/users/{user_id}/scores/recent',
            params={'include_fails': 1, 'limit': limit},
            headers=headers
        ) as response:
            scores = await response.json()
            
            if not scores:  # Check if scores list is empty
                raise ValueError(f"No recent plays found for user ID {user_id}")
                
            return scores[0] if limit == 1 else scores
    async def get_match(self, match_id: int) -> Dict[str, Any]:
        """Get details about a specific multiplayer match"""
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self.session.get(
            f'https://osu.ppy.sh/api/v2/matches/{match_id}',
            headers=headers
        ) as response:
            return await response.json()
    
    async def get_match_events(self, match_id: int) -> Dict[str, Any]:
        """Get events/history of a multiplayer match"""
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self.session.get(
            f'https://osu.ppy.sh/api/v2/matches/{match_id}/events',
            headers=headers
        ) as response:
            return await response.json()