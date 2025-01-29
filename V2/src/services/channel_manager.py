class ChannelManager:
    def __init__(self, database):
        self.database = database
        self.irc_client = None
    
    def init(self, bot):
        self.irc_client = bot
    
    async def add_channel(self, channel_name: str, is_match: bool = False):
        """Store channel with match flag"""
        query = """
        INSERT OR IGNORE INTO active_channels 
        (channel_name, is_match) VALUES (?, ?)
        """
        await self.database.execute(query, channel_name, int(is_match))

    async def handle_match_disband(self, channel: str):
        """Remove match channel when disbanded"""
        await self.remove_channel(channel)
    
    async def remove_channel(self, channel_name: str):
        """Remove channel from auto-rejoin"""
        query = "DELETE FROM active_channels WHERE channel_name = ?"
        await self.database.execute(query, channel_name)
    
    async def get_active_channels(self):
        """Get list of channels to auto-rejoin"""
        query = "SELECT channel_name FROM active_channels WHERE auto_rejoin = 1"
        results = await self.database.fetch_all(query)
        return [row[0] for row in results]
    
    async def rejoin_channels(self):
        """Rejoin all stored channels"""
        channels = await self.get_active_channels()
        for channel in channels:
            await self.irc_client.joinChannel(channel)
            await self.irc_client.sendMessage(channel, "Rejoined after reconnect/restart!")
