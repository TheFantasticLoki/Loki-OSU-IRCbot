from src.bot.command import Command
from datetime import timedelta

@Command.register("stats")
async def stats_command(ctx, *args):
    """Sends a specified user's / your stats to the user"""
    # Handle username parsing
    username = ' '.join(args) if args else ctx.author.name.replace('_', ' ')
    
    # Get user data
    user = await ctx.osu_api.get_user(username)
    uid = user['id']
    
    # Get user's top score
    user_top = await ctx.osu_api.get_user_best(uid, limit=1)
    
    # Format playtime
    playtime = str(timedelta(seconds=int(user['statistics']['play_time'])))
    
    # Construct response messages
    messages = [
        f"Showing stats for [https://osu.ppy.sh/users/{uid}/ {username}] | #{user['statistics']['global_rank']} | {user['follower_count']} Followers | Playtime: {playtime}",
        
        f"PP: {user['statistics']['pp']} | Accuracy: {round(user['statistics']['hit_accuracy'], 2)}% | Playcount: {user['statistics']['play_count']:,} | Replays Watched: {user['statistics']['replays_watched_by_others']}",
        
        f"Grade Counts: HD SS: {user['statistics']['grade_counts']['ssh']} | SS: {user['statistics']['grade_counts']['ss']} | HD S: {user['statistics']['grade_counts']['sh']} | S: {user['statistics']['grade_counts']['s']} | A: {user['statistics']['grade_counts']['a']}",
        
        f"Ranked Score: {user['statistics']['ranked_score']:,} (Lvl: {user['statistics']['level']['current']}) | Total Score: {user['statistics']['total_score']:,}",
        
        f"Highest PP Play: {user_top['pp']}PP on [{user_top['beatmap']['url']} {user_top['beatmapset']['artist']} - {user_top['beatmapset']['title']} ({user_top['beatmap']['version']})] ({user_top['beatmap']['difficulty_rating']}* NM) with {round(user_top['accuracy'] * 100, 2)}% {user_top['mods']}"
    ]
    
    return messages, []  # Return main messages and empty timeout messages list

