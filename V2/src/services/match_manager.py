from typing import Dict, List, Optional
import asyncio
from datetime import datetime, timezone
import time
from ..utils import log, getTB

class MatchManager:
    CHECK_INTERVAL = 300  # 5 minutes in seconds
    def __init__(self, database, channel_manager, osu_api):
        self.database = database
        self.channel_manager = channel_manager
        self.osu_api = osu_api
    
    async def add_match(self, match_id: str):
        """Track new multiplayer match"""
        channel = f"mp_{match_id}"
        # Add to active channels
        await self.channel_manager.add_channel(channel, is_match=True)
    
    async def remove_match(self, match_id: str):
        """Handle match cleanup when disbanded"""
        channel = f"mp_{match_id}"
        await self.channel_manager.remove_channel(channel)
    
    async def start_periodic_check(self):
        """Start periodic checking of match statuses"""
        while True:
            await self.check_all_matches()
            await asyncio.sleep(self.CHECK_INTERVAL)
    
    async def check_all_matches(self):
        """Check all match channels for disbanded status"""
        log("Checking all matches for disbanded event")
        # Get all match channels
        query = ("SELECT channel_name FROM active_channels WHERE channel_name LIKE 'mp_%'" 
                                                if self.database.db_type == 'mysql' 
                                                else "SELECT channel_name FROM active_channels WHERE channel_name GLOB 'mp_*'")
        match_channels = await self.database.fetch_all(query)

        log(f"Match Channels: {match_channels}", "debug")
        
        for (channel_name,) in match_channels:
            match_id = channel_name.replace('mp_', '')
            log(f"mID: {match_id}", "debug")
            try:
                # Get match data from API
                match_data = await self.osu_api.get_match(match_id)
                
                # Check events for disband
                for event in match_data.get('events', []):
                    if event.get('detail', {}).get('type') == 'match-disbanded':
                        # Handle disbanded match
                        await self.channel_manager.handle_match_disband(channel_name)
                        break
            except Exception as e:
                # Log error but continue checking other matches
                log(f"Error checking match {match_id}: {str(e)}\n{getTB()}", "error")
