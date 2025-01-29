from src.bot.command import Command
from ...utils import log, getTB
import asyncio
from typing import List

@Command.register(["join"], category="multi")
async def join_command(ctx, *args):
    """Joins a multi lobby, use matchid from end of match history link"""
    try:
        # Check if a match ID was provided
        if not args:
            return ["Please provide a match ID"], []
            
        # Extract match ID and clean it
        match_id = args[0].strip()
        
        # Remove 'mp_' prefix if user included it
        if match_id.startswith('mp_'):
            match_id = match_id[3:]
            
        # Join the channel
        channel = f"mp_{match_id}"
        await ctx.bot.joinChannel(channel)
        
        # Send welcome message to the lobby
        await ctx.bot.sendMessage(channel, "Hey there! I am Loki's IRC Bot. !lokihelp for commands. Have fun playing!")
        
        return [f"Successfully joined match #{match_id}"], []
        
    except Exception as e:
        log(f"Error joining lobby: {str(e)}\nTraceback:\n{getTB()}", "error")
        return [f"Error joining lobby: {str(e)}"], []

@Command.register(["start"], category="multi")
async def mpStart_command(ctx, *args):
    """Starts the match after a specified delay or 3 seconds"""
    try:
        countdown = int(args[0]) if args else 3
        
        # Create list of tuples for delayed messages
        timeout_messages = []
        
        if countdown > 30:
            timeout_messages.append(("Match starting in 30 seconds!", countdown - 30))
        if countdown > 10:
            timeout_messages.append(("Match starting in 10 seconds!", countdown - 10))
        if countdown > 5:
            timeout_messages.append(("Match starting in 5 seconds!", countdown - 5))
            
        # Add final messages
        timeout_messages.extend([
            ("Match starting now!", countdown),
            ("!mp start", countdown)
        ])
        
        return [f"Match starting in {countdown} seconds!"], timeout_messages
        
    except ValueError:
        return ["Invalid countdown value! Usage: !start [seconds]"], []

@Command.register("matchinfo", category="multi", subcategory="debug")
async def handle_match_info(ctx):
    """Get debug information about current match"""
    match_id = ctx.channel.replace('mp_', '')
    log(f"mID: {match_id}", "debug")
    
    debug_info = await ctx.match_manager.get_match_debug_info(match_id)
    info_lines = debug_info.split('\n')
    
    # Group lines into sets of 3
    grouped_lines = []
    for i in range(0, len(info_lines), 4):
        group = info_lines[i:i+4]
        grouped_lines.append(' | '.join(group))
    
    return grouped_lines, []

