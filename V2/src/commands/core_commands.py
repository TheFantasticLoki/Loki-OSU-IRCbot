from src.bot.command import Command
from ..utils import log, getTB
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

@Command.register("last")
@Command.register("r")
@Command.register("recent")
async def last_command(ctx, *args):
    """Sends a specified user's / your latest score"""
    try:
        # Handle username parsing
        username = ' '.join(args) if args else ctx.author.name.replace('_', ' ')

        # Get user data
        user = await ctx.osu_api.get_user(username)
        uid = user['id']

        # Get user's recent score
        try:
            user_recent = await ctx.osu_api.get_user_recent(uid, limit=1)
        except ValueError:
            return [f"No recent plays found for {username}"], []
        
        # Get PP calculation if not ranked
        if user_recent['beatmap']['status'] != 'ranked' or user_recent['pp'] == None:
            log(f"Calculating PP | Mods: {user_recent['mods']}", "debug")
            pp_calc = await ctx.calculator.calculate_score(
                beatmap_id=user_recent['beatmap']['id'],
                mods=user_recent['mods'],
                accuracy=user_recent['accuracy'],
                count_miss=user_recent['statistics']['count_miss'],
                count_50=user_recent['statistics']['count_50'],
                count_100=user_recent['statistics']['count_100'],
                count_300=user_recent['statistics']['count_300'],
                count_katu=user_recent['statistics']['count_katu'],
                count_geki=user_recent['statistics']['count_geki'],
                max_combo=user_recent['max_combo']
            )
            #print(pp_calc)
            pp_value = pp_calc['performance']['totalPerformance']
        else:
            pp_value = user_recent['pp']

        # Use calculated or API PP value
        pp_display = f"{round(pp_value, 2) if pp_value is not None else 'None'}"

        # Format length for display
        length_conversion = timedelta(seconds=int(user_recent['beatmap']['total_length']))
        formatted_length = str(length_conversion)

        # Format response with all V1 information
        return [ # TODO: Fix Map Max Combo not being correct. (THANKS PEPPY!!!!!!!!!)
            f"Showing Info for Latest Score from #{user['statistics']['global_rank']} [https://osu.ppy.sh/users/{uid}/ {username}]:",
            
            f"Map: [{user_recent['beatmap']['url']} {user_recent['beatmapset']['artist']} - {user_recent['beatmapset']['title']} [{user_recent['beatmap']['version']}]]",
            
            f"Map Stats: Status: {user_recent['beatmap']['status']} | Stars: {user_recent['beatmap']['difficulty_rating']} | CS: {user_recent['beatmap']['cs']} | AR: {user_recent['beatmap']['ar']} | HP: {user_recent['beatmap']['drain']} | OD: {user_recent['beatmap']['accuracy']} | BPM: {user_recent['beatmap']['bpm']} | Length: {formatted_length}",
            
            f"Play Stats: Mods: {user_recent['mods']} | Combo: {user_recent['max_combo']}/{user_recent['beatmap']['count_circles'] + user_recent['beatmap']['count_sliders'] + user_recent['beatmap']['count_spinners']} | Rank: {user_recent['rank']} | Acc: {round(user_recent['accuracy'] * 100, 2)}% | Misses: {user_recent['statistics']['count_miss']} | PP: {pp_display} | Score: {user_recent['score']:,} | FC: {user_recent['perfect']}"
        ], []
    except Exception as e:
        log(f"Error fetching recent play: {str(e)}\nTraceback:\n{getTB()}", "error")
        return [f"Error fetching recent play: {str(e)}"], []
