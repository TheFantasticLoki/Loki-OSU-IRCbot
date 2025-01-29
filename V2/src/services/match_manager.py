from typing import Dict, List, Optional
import asyncio
from datetime import datetime, timezone
import time
from ..utils import log, getTB
from enum import Enum

class MatchMode(Enum):
    NORMAL = "normal"
    AUTO_HOST_ROTATE = "ahr" 
    MAP_POOL = "pool"
    MAP_QUEUE = "queue"
    ELO = "elo"

class MatchWorker:
    POLL_INTERVAL = 5 # seconds
    def __init__(self, match_id: str, osu_api, database):
        self.match_id = match_id
        self.osu_api = osu_api
        self.database = database
        self.channel = f"mp_{match_id}"
        self.polling_task = None
        
        # Start polling when worker is created
        self.start_polling()
        self.last_check = None
        self.match_details = None
        
        # Match state tracking
        self.last_event_id = None
        self.current_host_id = None
        self.players = set()
        self.current_game = None
        self.match_name = None
        
        # Core match state
        self.mode = MatchMode.NORMAL
        self.settings = {
            'warmups': 2,
            'max_players': 16,
            'score_mode': 'score_v2',
            # Add other general settings here
        }
        
        # Mode-specific data
        self.host_queue = []  # For AHR mode
        self.map_pool = []    # For pool mode
        self.map_queue = []   # For queue mode
        self.elo_ratings = {} # For ELO mode
    
    def start_polling(self):
        """Start the polling loop for match updates"""
        self.polling_task = asyncio.create_task(self._poll_loop())
    
    async def _poll_loop(self):
        """Main polling loop to fetch match updates"""
        while True:
            try:
                match_data = await self.osu_api.get_match(self.match_id)
                await self.process_events(match_data)
                self.last_check = datetime.now(timezone.utc)
            except Exception as e:
                log(f"Error polling match {self.match_id}: {str(e)}", "error")
            await asyncio.sleep(self.POLL_INTERVAL)
    
    def stop_polling(self):
        """Stop the polling loop"""
        if self.polling_task:
            self.polling_task.cancel()
    
    async def process_events(self, match_data: dict):
        """Process all new events from match data"""
        events = match_data.get('events', [])

        # Process events in chronological order
        for i, event in enumerate(events):
            if self.last_event_id and event['id'] <= self.last_event_id:
                continue

            event_type = event['detail']['type']
            timestamp = event['timestamp']
            user_id = event['user_id']

            if event_type == 'match-created':
                self.match_name = match_data['match']['name']
                # Check if next event is host-changed with same user
                if (i + 1 < len(events) and 
                    events[i + 1]['detail']['type'] == 'host-changed' and
                    events[i + 1]['user_id'] == user_id):
                    # Creator joined as player
                    self.players.add(user_id)

            elif event_type == 'host-changed':
                self.current_host_id = user_id
                #if self.mode == MatchMode.AUTO_HOST_ROTATE:
                #    await self.handle_host_change(user_id)

            elif event_type == 'player-joined':
                self.players.add(user_id)

            elif event_type == 'player-left':
                self.players.discard(user_id)

            elif event_type == 'other' and 'game' in event:
                self.current_game = event['game']
                #if self.mode == MatchMode.MAP_POOL:
                #    await self.validate_map_selection(self.current_game['beatmap_id'])

            self.last_event_id = event['id']

    
    async def update_match_details(self):
        """Fetch and update match details from API"""
        self.match_details = await self.osu_api.get_match(self.match_id)
        self.last_check = datetime.now(timezone.utc)
        return self.match_details
    
    async def handle_event(self, event_type: str, event_data: dict):
        """Process different match events"""
        #if event_type == 'host-changed':
        #    if self.settings['auto_host_rotate']:
        #        await self.process_host_rotation(event_data)
        #elif event_type == 'match-finished':
        #    if self.settings['use_elo']:
        #        await self.process_elo_changes(event_data)

class MatchManager:
    CHECK_INTERVAL = 300  # 5 minutes in seconds
    def __init__(self, database, channel_manager, osu_api):
        self.database = database
        self.channel_manager = channel_manager
        self.osu_api = osu_api
        self.match_workers: Dict[str, MatchWorker] = {}
    
    async def add_match(self, match_id: str):
        """Track new multiplayer match"""
        channel = f"mp_{match_id}"
        # Create new match worker
        worker = MatchWorker(match_id, self.osu_api, self.database)
        self.match_workers[match_id] = worker
        # Initialize match details
        await worker.update_match_details()
        # Add to active channels
        await self.channel_manager.add_channel(channel, is_match=True)
    
    async def remove_match(self, match_id: str):
        """Handle match cleanup when disbanded"""
        if match_id in self.match_workers:
            self.match_workers[match_id].stop_polling()
            del self.match_workers[match_id]
        channel = f"mp_{match_id}"
        await self.channel_manager.remove_channel(channel)
    
    async def get_match_details(self, match_id: str):
        """Manual trigger to get match details"""
        if match_id in self.match_workers:
            return await self.match_workers[match_id].update_match_details()
        return None
    
    async def update_match_settings(self, match_id: str, settings: dict):
        """Update settings for specific match"""
        if match_id in self.match_workers:
            self.match_workers[match_id].settings.update(settings)
    
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
            # Create worker if it doesn't exist
            if match_id not in self.match_workers:
                self.match_workers[match_id] = MatchWorker(match_id, self.osu_api, self.database)
            try:
                # Get match data from API
                match_data = await self.osu_api.get_match(match_id)
                # Update worker with new data
                await self.match_workers[match_id].process_events(match_data)
                # Check events for disband
                for event in match_data.get('events', []):
                    if event.get('detail', {}).get('type') == 'match-disbanded':
                        # Handle disbanded match
                        await self.channel_manager.handle_match_disband(channel_name)
                        break
            except Exception as e:
                # Log error but continue checking other matches
                log(f"Error checking match {match_id}: {str(e)}\n{getTB()}", "error")
    
    async def get_match_debug_info(self, match_id: str) -> str:
        """Get detailed debug information about a match worker"""
        log(f"Getting debug info for match {match_id}", "debug")
        log(f"Active workers: {list(self.match_workers.keys())}", "debug")

        if match_id not in self.match_workers:
            # Create worker if it doesn't exist
            log(f"No active worker found for match #{match_id}, creating one.")
            self.match_workers[match_id] = MatchWorker(match_id, self.osu_api, self.database)
            match_data = await self.osu_api.get_match(match_id)
            await self.match_workers[match_id].process_events(match_data)

        worker = self.match_workers[match_id]

        debug_info = [
            f"Match ID: {worker.match_id}",
            f"Match Name: {worker.match_name}",
            f"Current Mode: {worker.mode.value}",
            f"Last Event ID: {worker.last_event_id}",
            f"Current Host: {worker.current_host_id}",
            f"Player Count: {len(worker.players)}",
            f"Players: {', '.join(str(p) for p in worker.players)}",
            f"Polling Active: {worker.polling_task and not worker.polling_task.done()}",
            f"Last Check: {worker.last_check.strftime('%H:%M:%S') if worker.last_check else 'Never'}"
        ]

        if worker.current_game:
            game = worker.current_game
            debug_info.extend([
                "\nCurrent Game:",
                f"Beatmap ID: {game['beatmap_id']}",
                f"Mode: {game['mode']}",
                f"Team Type: {game['team_type']}",
                f"Scoring Type: {game['scoring_type']}"
            ])

        return "\n".join(debug_info)
