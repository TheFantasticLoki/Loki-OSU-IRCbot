from typing import Dict, List, Optional
import asyncio
import time

class MultiplayerManager:
    def __init__(self, bot, osu_api):
        self.bot = bot
        self.osu_api = osu_api
        self.matches: Dict[str, "MatchState"] = {}
        self.host_rotation_timers: Dict[str, asyncio.Task] = {}
        
    async def start_match(self, channel: str, countdown: int = 30):
        """Start a match with countdown"""
        match_id = channel.replace('mp_', '')
        if countdown > 0:
            for i in range(countdown, 0, -5):
                await self.bot.sendMessage(channel, f"Match starting in {i} seconds!")
                await asyncio.sleep(5)
        await self.bot.sendMessage(channel, "START!")
        # Send IRC command to start match
        await self.bot.sendMessage(channel, "!mp start")

    async def monitor_host_activity(self, channel: str, timeout: int = 120):
        """Monitor host map selection and rotate if inactive"""
        match_id = channel.replace('mp_', '')
        while True:
            match_data = await self.osu_api.get_match(match_id)
            if not match_data['current_game_id']:
                # No map selected, check timeout
                if time.time() - match_data['last_activity'] > timeout:
                    await self.rotate_host(channel)
            await asyncio.sleep(30)

class MatchState:
    def __init__(self):
        self.current_host: Optional[str] = None
        self.players: List[str] = []
        self.queue: List[str] = []
        self.settings: Dict[str, Any] = {}
        self.last_activity: float = time.time()
