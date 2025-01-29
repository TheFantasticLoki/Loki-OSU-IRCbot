from typing import Dict, List, Optional, Tuple
import asyncio
import time

class MessageQueue:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.tasks: Dict[str, asyncio.Task] = {}
        self.message_counts: Dict[str, int] = {}  # Track messages per channel
        self.bot = None
    
    def init(self, bot):
        self.bot = bot
        
    def get_queue(self, channel: str) -> asyncio.Queue:
        """Get or create queue for specific channel"""
        if channel not in self.queues:
            self.queues[channel] = asyncio.Queue()
            # Start processor for this channel
            self.tasks[channel] = asyncio.create_task(self.process_queue(channel))
        return self.queues[channel]
        
    async def add_message(self, channel: str, message: str, delay: float = 0) -> int:
        """Add message to queue and return number of queued messages"""
        queue = self.get_queue(channel)
        await queue.put((message, time.time() + delay))
        self.message_counts[channel] = self.message_counts.get(channel, 0) + 1
        return self.message_counts[channel]

    async def process_queue(self, channel: str):
        """Process messages for a channel"""
        queue = self.queues[channel]
        while True:
            message, send_time = await queue.get()
            current_time = time.time()
            if send_time > current_time:
                await asyncio.sleep(send_time - current_time)
            
            # Actually send the message through IRC
            await self.bot.sendMessage(channel, message)
            self.message_counts[channel] -= 1
            queue.task_done()
