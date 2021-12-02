import osu_irc
import _thread
import asyncio
from time import sleep
from pprint import pprint
import datetime
import aiohttp
import nng_oppai
import urllib.request
import os.path
from os.path import exists
import json

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'Https://osu.ppy.sh/oauth/token'

API_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}' # {} to format token within the code
}

TOKEN_DATA = {
    'client_id': 8120,
    'client_secret': 'hVPf8DCcoP55pkGnqpzAsvKNjkaKbaTukVte43vE',
    'grant_type': 'client_credentials',
    'scope': 'public'
}

commands = {} # command list

# initalize command list for each prefix
commands['!'] = {}
commands['%'] = {}
commands['$'] = {}
commands['@'] = {}

async def get_token():
    async with aiohttp.ClientSession() as web:
        async with web.post(TOKEN_URL, data=TOKEN_DATA) as response:
            return (await response.json()).get('access_token')

def command(prefix, name, timeout: bool = False): # command decorator
    def wrapper(callback): # callback = function to run
        commands[prefix][name] = {'cb': callback, 'timeout': timeout} # add the name of the command to the list of commands for this prefix giving what to run
        return callback

    return wrapper

@command(prefix='!', name='lokihelp')
async def loki_help(message, args, prefix):
    """List all available commands to the user"""
    command_list = [] # initiate list of all available commands
    
    for cmd, info in commands[prefix].items(): # get command name & the function
        command_list.append(f'{prefix}{cmd} - {info["cb"].__doc__}') # add cmd to the list and also the explanation of what it does (__doc__ = info given in a function)

    messages = [ # initiate messages to return back
        'Welcome to Loki\'s IRC Bot! Developed by The Fantastic Loki',
        'Current List of Commands | ! = Loki | % = Cryceptio | $ = Mylk | @ = Kippz:'
    ]
    
    messages.extend(command_list) # add the entire command list to list to return
    messages.append(
        'Thanks to [https://osu.ppy.sh/users/13431764/ minisbett] for helping me with the initialcode'
    )
    
    return messages

@command(prefix='!', name='stats', timeout=True)
async def user_stats(message, args, prefix):
    """Sends a specified user's / your stats to the user"""
    token = await get_token()

    headers = API_HEADERS
    headers['Authorization'] = f'Bearer {token}'

    if args:
        username = ' '.join(args)
    else:
        username = message.Author.name.replace('_', ' ')

    async with aiohttp.ClientSession() as web:
        async with web.get(f'{API_URL}/users/{username}', headers=headers) as response:
            user = await response.json()

    uid = user['id']

    async with aiohttp.ClientSession() as web:
        async with web.get(f"{API_URL}/users/{uid}/scores/best?limit=1", headers=headers) as response:
            user_top = (await response.json())[0]

    playtime_conversion = datetime.timedelta(seconds=int(user['statistics']['play_time'])) # convert map length to hour min seconds format
    formated_playtime = str(playtime_conversion) # convert map length to string format

    #pprint(user_top, indent=2, depth=3)

    msg = [
        f"Showing stats for [https://osu.ppy.sh/users/{uid}/ {username}] | #{user['statistics']['global_rank']} | {user['follower_count']} Followers | Playtime: {formated_playtime}",
        f"PP: {user['statistics']['pp']} | Accuracy: {round(user['statistics']['hit_accuracy'], 2)}% | Playcount: {user['statistics']['play_count']:,} | Replays Watched: {user['statistics']['replays_watched_by_others']}",
        f"Grade Counts: HD SS: {user['statistics']['grade_counts']['ssh']} | SS: {user['statistics']['grade_counts']['ss']} | HD S: {user['statistics']['grade_counts']['sh']} | S: {user['statistics']['grade_counts']['s']} | A: {user['statistics']['grade_counts']['a']}",
        f"Ranked Score: {user['statistics']['ranked_score']:,} (Lvl: {user['statistics']['level']['current']}) | Total Score: {user['statistics']['total_score']:,}",
        f"Highest PP Play: {user_top['pp']}PP on [{user_top['beatmap']['url']} {user_top['beatmapset']['artist']} - {user_top['beatmapset']['title']} ({user_top['beatmap']['version']})] with {round(user_top['accuracy'] * 100, 2)}% {user_top['mods']}",
    ]

    tm = []

    if username == 'Fantastic Loki':
        tm.extend([
            'Achieved Supremacy Medal at #1,000,000',
            'Notable Scores:',
            '[https://i.imgur.com/is2g8SM.png/ XI - Freedom Dive (tpz Overcute Remix) POG DIMENSIONS 8.02* 235BPM Tech 53 Miss Pass Choke] - [https://osu.ppy.sh/ss/17011607/cb48 SS] - [https://drive.google.com/file/d/1G9CO0yNB615fFA8VTu4XTwZvd10CSUb9/view?usp=sharing Replay File] - [https://osu.ppy.sh/beatmapsets/895846#osu/1871842 Map Link]',
            '[https://i.imgur.com/g8Dwy0Q.png/ Crystalia - Luminosity 7.88* 28 Miss Pass] - [https://www.dropbox.com/s/8u9543z43vftozu/Fantastic%20Loki%20-%20DJ%20TOTTO%20-%20Crystalia%20%5BLuminosity%5D%2028%20Miss%20Pass%20%282021-05-13%29.osr?dl=1 Replay] - [https://osu.ppy.sh/beatmapsets/691220#osu/1519160 Map Link]',
            '[https://i.imgur.com/MtgdwHp.png/ Cycle Hit HR 20 Miss 598 Combo Pass] - [https://www.dropbox.com/s/taep9jfxqseuhef/Fantastic%20Loki%20-%20KASAI%20HARCORES%20-%20Cycle%20Hit%20%5BHome%20Run%5D%20HR%2020%20Miss%20%282021-06-16%29.osr?dl=1 Replay] - [https://osu.ppy.sh/beatmapsets/636839#osu/1351114 Map Link]'
        ])
    elif username == 'MudKippz':
        tm.extend([
            'Highest Ranked Pass: 9.64*',
            'Notable Scores:',
            '[https://www.youtube.com/watch?v=I7R3uzbUNL4&ab_channel=MudKippz/ Astrid HDHR FC #6 Global]',
            '[https://www.youtube.com/watch?v=w9pWF6iS_8U/ Cory in the House 4th DT Fc Global]',
            '[https://www.youtube.com/watch?v=Kz5IlKSbRps/ Horizon Blue NM FC #22 Global]'
        ])

    return (msg, tm)

@command(prefix='!', name='last')
async def user_recent(message, args, prefix):
    """Sends a specified user's / your latest score to the user"""
    token = await get_token()

    headers = API_HEADERS
    headers['Authorization'] = f'Bearer {token}'

    # Add username validity check
    if args:
        username = ' '.join(args)
    else:
        username = message.Author.name.replace('_', ' ')

    async with aiohttp.ClientSession() as web:
        async with web.get(f'{API_URL}/users/{username}', headers=headers) as response:
            user = await response.json()

    uid = user['id']

    async with aiohttp.ClientSession() as web:
        async with web.get(f"{API_URL}/users/{uid}/scores/recent?include_fails=1&limit=1", headers=headers) as response:
            user_recent = (await response.json())[0]

    async with aiohttp.ClientSession() as web:
        async with web.get(f"{API_URL}/beatmaps/{user_recent['beatmap']['id']}", headers=headers) as response:
            user_recent_map = await response.json()

    length_conversion = datetime.timedelta(seconds=int(user_recent_map['total_length'])) # convert map length to hour min seconds format
    formated_length = str(length_conversion) # convert map length to string format
    user_recent_mods = "".join(user_recent['mods']) # join mods together
    print(user_recent_mods)

    #mods = user_recent['mods']
    MODS_NF = (1<<0)
    MODS_EZ = (1<<1)
    MODS_TD = (1<<2)
    MODS_HD = (1<<3)
    MODS_HR = (1<<4)
    MODS_SD = (1<<5)
    MODS_DT = (1<<6)
    MODS_RX = (1<<7)
    MODS_HT = (1<<8)
    MODS_NC = (1<<9)
    MODS_FL = (1<<10)
    MODS_AT = (1<<11)
    MODS_SO = (1<<12)
    MODS_AP = (1<<13)
    MODS_PF = (1<<14)
    MODS_KEY4 = (1<<15)
    MODS_KEY5 = (1<<16)
    MODS_KEY6 = (1<<17)
    MODS_KEY7 = (1<<18)
    MODS_KEY8 = (1<<19)
    MODS_FADEIN = (1<<20)
    MODS_RANDOM = (1<<21)
    MODS_CINEMA = (1<<22)
    MODS_TARGET = (1<<23)
    MODS_KEY9 = (1<<24)
    MODS_KEYCOOP = (1<<25)
    MODS_KEY1 = (1<<26)
    MODS_KEY3 = (1<<27)
    MODS_KEY2 = (1<<28)
    MODS_SCOREV2 = (1<<29)
    #MODS_TOUCH_DEVICE MODS_TD
    #MODS_NOVIDEO MODS_TD /* never forget */
    #MODS_SPEED_CHANGING (MODS_DT | MODS_HT | MODS_NC)
    #MODS_MAP_CHANGING (MODS_HR | MODS_EZ | MODS_SPEED_CHANGING)
    def mods_func(str):
        mods = 0
        if 'DT' in str:
            mods |= MODS_DT
        if 'NC' in str:
            mods |= MODS_NC
        if 'HT' in str:
            mods |= MODS_HT
        if 'HR' in str:
            mods |= MODS_HR
        if 'HD' in str:
            mods |= MODS_HD
        if 'NF' in str:
            mods |= MODS_NF
        if 'EZ' in str:
            mods |= MODS_EZ
        if 'TD' in str:
            mods |= MODS_TD
        if 'SD' in str:
            mods |= MODS_SD
        if 'RX' in str:
            mods |= MODS_RX
        if 'FL' in str:
            mods |= MODS_FL
        if 'AT' in str:
            mods |= MODS_AT
        if 'SO' in str:
            mods |= MODS_SO
        if 'AP' in str:
            mods |= MODS_AP
        if 'PF' in str:
            mods |= MODS_PF
        return mods
        
    mods = mods_func(user_recent_mods)
    print(mods_func(user_recent_mods))
    file_exists = os.path.exists(f"/osu_maps/{user_recent['beatmap']['id']}.osu")
    if file_exists == True:
        map_path = f"/osu_maps/{user_recent['beatmap']['id']}.osu"
    else:
        url = f"http://old.ppy.sh/osu/{user_recent['beatmap']['id']}"
        urllib.request.urlretrieve(url, f"/osu_maps/{user_recent['beatmap']['id']}.osu")
        map_path = f"/osu_maps/{user_recent['beatmap']['id']}.osu"

    pp_ptr = nng_oppai.load_map(f'{mods}|{map_path}')

    acc = user_recent['accuracy']
    miss_count = user_recent['statistics']['count_miss']
    max_combo = user_recent['max_combo']
    pp = nng_oppai.calc_pp_single(f'{pp_ptr}|{mods}|{acc}|{miss_count}|{max_combo}')
    map_stats = json.loads(nng_oppai.get_beatmap_stats(pp_ptr))
    #map_stats = nng_oppai.get_beatmap_stats(pp_ptr)

    print('pp: ', nng_oppai.calc_pp_single(f'{pp_ptr}|{mods}|{acc}|{miss_count}|{max_combo}'))

    print('map_stats', nng_oppai.get_beatmap_stats(pp_ptr))
    nng_oppai.free_map(pp_ptr) # Free the pp_ptr once you are done
    #pprint(user_recent, indent=2, depth=3)

    return [
        f"Showing Info for Latest Score from #{user['statistics']['global_rank']} [https://osu.ppy.sh/users/{uid}/ {username}]:",
        f"Map: [{user_recent['beatmap']['url']} {user_recent['beatmapset']['artist']} - {user_recent['beatmapset']['title']} [{user_recent['beatmap']['version']}]]",
        f"Map Stats: Status: {user_recent['beatmap']['status']} | Stars: {map_stats['total_stars']} | CS: {map_stats['cs']} | AR: {map_stats['ar']} | HP: {map_stats['drain']} | OD: {map_stats['accuracy']} | BPM: {user_recent['beatmap']['bpm']} | Length: {formated_length}",
        f"Play Stats: Mods: {user_recent['mods']} | Combo: {user_recent['max_combo']}/{user_recent_map['max_combo']} | Rank: {user_recent['rank']} | Acc: {round(user_recent['accuracy'] * 100, 2)}% | Misses: {user_recent['statistics']['count_miss']} | PP: {round(pp, 2)} | Score: {user_recent['score']:,} | FC: {user_recent['perfect']}"
    ]


@command(prefix='!', name='collections')
async def loki_collections(message, args, prefix):
    """Sends Loki's OSU! Collections to the user"""
    return [
        "Check out some of my [https://osustats.ppy.sh/collections/1?user=12792332/ Collections]. Import and Use with [https://github.com/Piotrekol/CollectionManager/releases/ Collections Manager by Piotrekol] or just view inside browser.",
        "[https://osustats.ppy.sh/collection/7572 Multiplayer Collection] - Loki's Hand Picked Maps for playing Multi. Contains the following types of maps: Fun, Challenge, Banger Songs, Intresting Mapping, etc.",
        "[https://osustats.ppy.sh/collection/7573 Stream Consistency Collection] - Collection of Maps for Practicing Streams.",
        "[https://osustats.ppy.sh/collection/7575 Bangers Collection] - A collection all about good music meant to get you hyped or groovin."
    ]

@command(prefix='!', name='twitch')
async def loki_twitch(message, args, prefix):
    """Send Loki's Twitch channel to the user"""
    return [
        'Check out my [https://twitch.tv/TheFantasticLoki/ Twitch Channel] where you can watch me play live.'
    ]

@command(prefix='!', name='skin')
async def loki_skin(message, args, prefix):
    """Send Loki's skin to the user"""
    return [
        'Check out my [https://drive.google.com/drive/folders/1Kz2ag71kdRZ6Guy5WSxzQHl_2C9p5uHm?usp=sharing/ Custom Skin] focused on minimalism, good for aim and sightreading! Latest Version: V5 Now Supporting Lazer'
        'Be sure to /invite yourself before importing the skin so you can easily join back.'
    ]

@command(prefix='!', name='guilded')
async def loki_guilded(message, args, prefix):
    """Sends Lokiverse Guild server to the user"""
    return [
        'Come join The [https://www.guilded.gg/i/k1bm8yzp Lokiverse Guild] where you can get the @osu role and find groups dedicated to multiple games such as OSU!, Minecraft, CSGO, GTA, and More!'
    ]

@command(prefix='!', name='guildedvc')
async def loki_guilded_vc(message, args, prefix):
    """Sends an invite to Lokiverse osu! vc to the user"""
    return [
        'Come join [https://www.guilded.gg/i/k5alYKWk?cid=46c9ee4e-5320-406b-99bd-e48e14e41802&intent=voice OSU VC] in the Lokiverse Guild! Multiple VC rooms, Sub-Room VC with direct vc between members in different rooms and More!'
    ]

@command(prefix='!', name='osulive')
async def loki_osulive(message, args, prefix):
    """Sends an invite to OSU Live in Lokiverse to the user"""
    return [
        'Come join [https://www.guilded.gg/i/2GaJ0BBp?cid=a7988af4-dd71-4e6a-9d8b-0335dd22fdb6&intent=stream Lokiverse OSU Live] where you can stream your game and chat with others!'
    ]

@command(prefix='!', name='discord')
async def loki_discord(message, args, prefix):
    """Send Loki's Discord server to the user"""
    return [
        'Come join my [https://bit.ly/LokiHubDiscord discord] where you can find channels for Games such as OSU!, CSGO, Minecraft, and other topics.'
    ]

@command(prefix='!', name='vc')
async def loki_vc(message, args, prefix):
    """Sends an invite to Loki's osu! vc to the user"""
    return [
        'Come Join this [https://bit.ly/LokiOSUVCInv Voice Chat]! It will join directly to the OSU! VC in my server.'
    ]

@command(prefix='!', name='test')
async def loki_test(message, args, prefix):
    """Send test command"""
    print(nng_oppai.test(1))
    return [
        'test complete'
    ]



class LokiIRC(osu_irc.Client):
    async def onReady(self):
        print("BOT: Connected")

    async def onMessage(self, message):
        print(f'INPUT: {message.Author.name}: {message.content}')
        
        prefix = message.content[0] # get the prefix they used
        split_msg = message.content[1:].split() # [cmd, arg1, arg2 etc....]

        command = split_msg[0]
        args = split_msg[1:]
        
        if not (command_list := commands.get(prefix)):
            return # invalid prefix
        
        if not (cmd_info := command_list.get(command)):
            return # invalid command

        callback = cmd_info['cb']
        timeout = cmd_info['timeout']

        timeout_messages = None
        
        if not timeout:
            messages = await callback(message, args, prefix) # give the message and any args to the function for this command
        else:
            messages, timeout_messages = await callback(message, args, prefix)
        
        for msg in messages: # allow multiple messages to be sent using a list: [message1, message2 etc.]
            await message.reply(self, msg)

        if timeout_messages:
            await asyncio.sleep(5)
            for msg in timeout_messages:
                await message.reply(self, msg)

x = LokiIRC(token="34f2f6cc", nickname="fantastic_loki", reconnect=True, request_limit=15)

async def main():
    while True:
        text = input()
        
        if not 'JOIN' in text:
            await x.joinChannel(f"mp_{text}")
            print(f"BOT: Joined #mp_{text}")
            await x.sendMessage(f"mp_{text}", "Hey there! I am Loki's IRC Bot. !lokihelp for commands. Have fun playing!")
        else:
            # wants to join a channel (format: JOIN channel_name)
            channel = text.split(' ')[1]
            
            if '#' in channel:
                pass # public channels not allowed

            await x.joinChannel(channel)
            print(f'BOT: Joined {channel}')
            await x.sendMessage(channel, "Hey there! I am Loki's IRC Bot. !lokihelp for commands. Have fun playing!")

_thread.start_new_thread(x.run, ())

while x.running == False:
    sleep(1)

sleep(3)

asyncio.run(main())
