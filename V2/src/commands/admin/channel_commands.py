from src.bot.command import Command
from ...utils import log

@Command.register("listchannels", category="admin", subcategory="channel")
async def list_channels(ctx, *args):
    channels = await ctx.channel_manager.get_active_channels()
    return [f"Active channels: {', '.join(channels)}"], []

@Command.register("disablechannel", category="admin", subcategory="channel")
async def disable_channel(ctx, *args):
    if not args:
        return ["Usage: !disablechannel <channel_name>"], []
    await ctx.channel_manager.remove_channel(args[0])
    return [f"Disabled auto-rejoin for channel: {args[0]}"], []

@Command.register("testmatch", category="test")
async def test_match_api(ctx, *args):
    if not args:
        return ["Usage: !testmatch <match_id>"], []
        
    match_id = args[0]
    messages = []
    
    # Test match details
    match_data = await ctx.osu_api.get_match(match_id)
    log(match_data)
    messages.append(f"Test Complete, check console for output.")
    
    return messages, []
