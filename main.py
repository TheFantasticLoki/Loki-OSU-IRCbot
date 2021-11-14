import osu_irc
import _thread
import asyncio
from time import sleep
import requests
from pprint import pprint
import datetime
from osu_sr_calculator import calculateStarRating

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'Https://osu.ppy.sh/oauth/token'

class LokiIRC(osu_irc.Client):
    async def get_token(self):
        data = {
            'client_id': 8120,
            'client_secret': 'placeholder',
            'grant_type': 'client_credentials',
            'scope': 'public'
        }

        response = requests.post(TOKEN_URL, data=data)
        print(response)

        return response.json().get('access_token')

    async def onReady(self):
        print("BOT: Connected")

    async def onMessage(self, message):
        print(f'INPUT: {message.Author.name}: {message.content}')
        if message.content == "!lokihelp":
            await message.reply(self, "Welcome to Loki's IRC Bot! Developed by The Fantastic Loki")
            await message.reply(self, "Current List of Commands | ! = Loki | % = Cryceptio | $ = Mylk | @ = Kippz:")
            await message.reply(self, "!join <Match_history_id> - Use this to have Loki IRC join your multi room, !mp addref Fantastic Loki first!")
            await message.reply(self, '!twitch - Sends my Twitch link')
            await message.reply(self, '!skin - Sends link to my skins')
            await message.reply(self, '!discord - Sends permanent Discord Invite Link')
            await message.reply(self, '!vc - Sends Permanent Discord VC Invite Link that will join OSU! VC automatically')
            await message.reply(self, "!lokistats - Sends custom stats output for Fantastic Loki")
            await message.reply(self, "!collections - Sends List of Loki's Collections for viewing/downloading.")
            await message.reply(self, 'Thanks to [https://osu.ppy.sh/users/13431764/ minisbett] for helping with the initial code')
        elif message.content == "!twitch":
            await message.reply(self, "Check out my [https://twitch.tv/TheFantasticLoki/ Twitch Channel] where you can watch me play live.")
            await message.reply(self, 'https://twitch.tv/TheFantasticLoki')
        elif message.content == "!skin":
            await message.reply(self, "Check out my [https://drive.google.com/drive/folders/1Kz2ag71kdRZ6Guy5WSxzQHl_2C9p5uHm?usp=sharing/ Custom Skin] focused on minimalism, good for aim and sightreading! Latest Version: V4")
            await message.reply(self, 'https://drive.google.com/drive/folders/1Kz2ag71kdRZ6Guy5WSxzQHl_2C9p5uHm?usp=sharing')
        elif message.content == "!discord":
            await message.reply(self, 'Come join my [https://bit.ly/LokiHubDiscord discord] where you can find channels for Games such as OSU!, CSGO, Minecraft, and other topics.')
            await message.reply(self, 'https://bit.ly/LokiHubDiscord')
        elif message.content == "!vc":
            await message.reply(self, "Come Join this [https://bit.ly/LokiOSUVCInv Voice Chat]! It will join directly to the OSU! VC in my server.")
            await message.reply(self, 'https://bit.ly/LokiOSUVCInv')
        elif message.content == "!lokistats":
            token = await self.get_token()

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            lokiapi = requests.get(f"{API_URL}/users/12792332", headers=headers)
            loki = lokiapi.json()
            loki_top = requests.get(f"{API_URL}/users/12792332/scores/best?limit=1", headers=headers)
            loki_top_info = loki_top.json()[0]
            #pprint(loki_top_info['beatmapset'], indent=2, depth=3)
            await message.reply(self, f"Showing stats for [https://osu.ppy.sh/users/12792332/ Fantastic Loki] #{loki['statistics']['global_rank']}")
            await message.reply(self, f"PP: {loki['statistics']['pp']} | Accuracy: {round(loki['statistics']['hit_accuracy'], 2)} | Playcount: {loki['statistics']['play_count']:,}")
            await message.reply(self, f"Ranked Score: {loki['statistics']['ranked_score']:,} (Lvl: {loki['statistics']['level']['current']}) | Total Score: {loki['statistics']['total_score']:,}")
            await message.reply(self, f"Highest PP Play: {loki_top_info['pp']}PP on [{loki_top_info['beatmap']['url']} {loki_top_info['beatmapset']['artist']} - {loki_top_info['beatmapset']['title']} ({loki_top_info['beatmap']['version']})]")
            await asyncio.sleep(5)
            await message.reply(self, 'Achieved Supremacy Medal at #1,000,000')
            await message.reply(self, 'Notable Scores:')
            await message.reply(self, '[https://i.imgur.com/MtgdwHp.png/ Cycle Hit HR 20 Miss 598 Combo Pass]')
            await message.reply(self, '[https://i.imgur.com/g8Dwy0Q.png/ Crystalia - Luminosity 7.88* 28 Miss Pass]')
            await message.reply(self, '[https://i.imgur.com/htrui5D.png/ Psalm dla Ciebie - Poloz mnie na swym ramieniu 8.21* 66 Miss Choke]')
        elif message.content == "!collections":
            await message.reply(self, "Check out some of my [https://osustats.ppy.sh/collections/1?user=12792332/ Collections]. Import and Use with [https://github.com/Piotrekol/CollectionManager/releases/ Collections Manager by Piotrekol] or just view inside browser.")
            await message.reply(self, "[https://osustats.ppy.sh/collection/7572/ Multiplayer Collection] - Loki's Hand Picked Maps for playing Multi. Contains the following types of maps: Fun, Challenge, Banger Songs, Intresting Mapping, etc.")
            await message.reply(self, "[https://osustats.ppy.sh/collection/7573/ Stream Consistency Collection] - Collection of Maps for Practicing Streams.")
            await message.reply(self, "[https://osustats.ppy.sh/collection/7575/ Bangers Collection] - A collection all about good music meant to get you hyped or groovin.")
        elif message.content == "!last":
            token = await self.get_token()
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            username = message.Author.name.replace('_',' ') #replace underscores in usernames with spaces and define username
            user = requests.get(f"{API_URL}/users/{username}", headers=headers) # requests user data
            user_info = user.json() # store user data in variable
            user_id = user_info['id'] # define user id
            user_recent_scores = requests.get(f"{API_URL}/users/{user_id}/scores/recent?include_fails=1&limit=1", headers=headers) # request users most recent score including fails from osu!api
            user_recent_scores_info = user_recent_scores.json()[0] # store recent score data in variable
            recent_map = requests.get(f"{API_URL}/beatmaps/{user_recent_scores_info['beatmap']['id']}", headers=headers) # requests beatmap data from users most recent score
            user_map_info = recent_map.json() # store beatmap data in variable
            length_conversion = datetime.timedelta(seconds=int(user_map_info['total_length'])) # convert map length to hour min seconds format
            formated_length = str(length_conversion) # convert map length to string format
            user_recent_mods = "".join(user_recent_scores_info['mods']) # join mods together
            # Cap Beatmap Difficulty stats such as cs, od, ar, and hp to 10 unless user_recent_scores_info['mods'] == ['DT'] in which case cap to 11
            hrar = round(user_recent_scores_info['beatmap']['ar'] * 1.4, 2)
            if hrar > 10:
                hrar = 10
            hrcs = round(user_recent_scores_info['beatmap']['cs'] * 1.3, 2)
            if hrcs > 10:
                hrcs = 10
            hrod = round(user_recent_scores_info['beatmap']['accuracy'] * 1.4, 2)
            if hrod > 10:
                hrod = 10
            hrhp = round(user_recent_scores_info['beatmap']['drain'] * 1.4, 2)
            if hrhp > 10:
                hrhp = 10
            # calculate starRating for map_id=(user_recent_scores_info['beatmap_id']), mods=[(user_recent_mods)]
            starRating = calculateStarRating(map_id=f"{user_recent_scores_info['beatmap']['id']}", mods=[f"{user_recent_mods}"])
            #pprint(user_recent_mods, indent=2, depth=3)
            await message.reply(self, f"Showing Info for Latest Score from [https://osu.ppy.sh/users/{user_id}/ {username}]:")
            await message.reply(self, f"Map: [{user_recent_scores_info['beatmap']['url']} {user_recent_scores_info['beatmapset']['artist']} - {user_recent_scores_info['beatmapset']['title']} [{user_recent_scores_info['beatmap']['version']}]]")
            # show unmodified cs/ar/od/hp if user_recent_scores_info['mods'] == [] elif user_recent_scores_info['mods'] == ['hr'] multiply cs by 30% and ar/od/hp by 40%
            if user_recent_scores_info['mods'] == []:
                await message.reply(self, f"Map Stats (*NM): Stars: {user_recent_scores_info['beatmap']['difficulty_rating']} | CS: {user_recent_scores_info['beatmap']['cs']} | AR: {user_recent_scores_info['beatmap']['ar']} | HP: {user_recent_scores_info['beatmap']['drain']} | OD: {user_recent_scores_info['beatmap']['accuracy']} | Length: {formated_length}")
            elif user_recent_scores_info['mods'] == ['HR']:
                await message.reply(self, f"Map Stats (*HR): Stars: {round(starRating['HR'], 2)} | CS: {hrcs} | AR: {hrar} | HP: {hrhp} | OD: {hrod} | Length: {formated_length}")
            else:
                await message.reply(self, f"Map Stats (*NM): Stars: {user_recent_scores_info['beatmap']['difficulty_rating']} | CS: {user_recent_scores_info['beatmap']['cs']} | AR: {user_recent_scores_info['beatmap']['ar']} | HP: {user_recent_scores_info['beatmap']['drain']} | OD: {user_recent_scores_info['beatmap']['accuracy']} | Length: {formated_length}")
            #await message.reply(self, f"Map Stats (*NC): Stars: {user_recent_scores_info['beatmap']['difficulty_rating']} | CS: {user_recent_scores_info['beatmap']['cs']} | AR: {user_recent_scores_info['beatmap']['ar']} | HP: {user_recent_scores_info['beatmap']['drain']} | OD: {user_recent_scores_info['beatmap']['accuracy']} | Length: {user_map_info['total_length']/60} minutes")
            await message.reply(self, f"Play Stats: Mods: {user_recent_scores_info['mods']} | Combo: {user_recent_scores_info['max_combo']}/{user_map_info['max_combo']} | Rank: {user_recent_scores_info['rank']} | Acc: {round(user_recent_scores_info['accuracy'] * 100, 2)}% | Misses: {user_recent_scores_info['statistics']['count_miss']} | PP: {user_recent_scores_info['pp']} | Score: {user_recent_scores_info['score']:,}")
        elif message.content == "!stats":
            token = await self.get_token()
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            username = message.Author.name.replace('_',' ') #replace underscores in usernames with spaces and define username
            userapi = requests.get(f"{API_URL}/users/{username}", headers=headers)
            user = userapi.json() #store user data in variable
            user_id = user['id'] # define user id
            user_top = requests.get(f"{API_URL}/users/{user_id}/scores/best?limit=1", headers=headers)
            user_top_info = user_top.json()[0]
            pprint(userapi, indent=2, depth=3)
            await message.reply(self, f"Showing stats for [https://osu.ppy.sh/users/{user_id}/ {username}] | #{user['statistics']['global_rank']} | {user['follower_count']} Followers")
            await message.reply(self, f"PP: {user['statistics']['pp']} | Accuracy: {round(user['statistics']['hit_accuracy'], 2)} | Playcount: {user['statistics']['play_count']:,} | Replays Watched: {user['statistics']['replays_watched_by_others']}")
            await message.reply(self, f"Grade Counts: HD SS: {user['statistics']['grade_counts']['ssh']} | SS: {user['statistics']['grade_counts']['ss']} | HD S: {user['statistics']['grade_counts']['sh']} | S: {user['statistics']['grade_counts']['s']} | A: {user['statistics']['grade_counts']['a']}")
            await message.reply(self, f"Ranked Score: {user['statistics']['ranked_score']:,} (Lvl: {user['statistics']['level']['current']})")
            await message.reply(self, f"Total Score: {user['statistics']['total_score']:,}")
            await message.reply(self, f"Highest PP Play: {user_top_info['pp']}PP on [{user_top_info['beatmap']['url']} {user_top_info['beatmapset']['artist']} - {user_top_info['beatmapset']['title']} ({user_top_info['beatmap']['version']})]")
            await message.reply(self, f"Loki!IRC bot Developed by [https://osu.ppy.sh/users/12792332/ The Fantastic Loki]")
            if message.Author.name == "Fantastic_Loki":
                await asyncio.sleep(5)
                await message.reply(self, 'Achieved Supremacy Medal at #1,000,000')
                await message.reply(self, 'Notable Scores:')
                await message.reply(self, '[https://i.imgur.com/MtgdwHp.png/ Cycle Hit HR 20 Miss 598 Combo Pass]')
                await message.reply(self, '[https://i.imgur.com/g8Dwy0Q.png/ Crystalia - Luminosity 7.88* 28 Miss Pass]')
                await message.reply(self, '[https://i.imgur.com/htrui5D.png/ Psalm dla Ciebie - Poloz mnie na swym ramieniu 8.21* 66 Miss Choke]')
            elif message.Author.name == "MudKippz":
                await asyncio.sleep(5)
                await message.reply(self, 'Highest Ranked Pass: 9.64*')
                await message.reply(self, 'Notable Scores:')
                await message.reply(self, '[https://www.youtube.com/watch?v=I7R3uzbUNL4&ab_channel=MudKippz/ Astrid HDHR FC #6 Global]')
                await message.reply(self, '[https://www.youtube.com/watch?v=w9pWF6iS_8U/ Cory in the House 4th DT Fc Global]')
                await message.reply(self, '[https://www.youtube.com/watch?v=Kz5IlKSbRps/ Horizon Blue NM FC #22 Global]')
        elif message.Author.name == "Fantastic_Loki" and message.content == "!test":
            token = await self.get_token()
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            username_test = requests.get(f"{API_URL}/users/{message.Author.name}", headers=headers)
            user_test = username_test.json() # test if username uses underscores
            user_test_error = user_test['error'] # test if username is in database
            username = message.Author.name.replace('_',' ') #replace underscores in usernames with spaces and define username
            # if username_test returns 404, then replace underscores with spaces and try again
            if user_test_error == None:
                userapi = requests.get(f"{API_URL}/users/{username}", headers=headers)
            else:
                userapi = requests.get(f"{API_URL}/users/{message.Author.name}", headers=headers)
            #userapi = requests.get(f"{API_URL}/users/{username}", headers=headers)
            user = userapi.json() #store user data in variable
            print ("test name")
            pprint(user_test, indent=2, depth=3)
            print ("formated Name")
            pprint(user, indent=2, depth=3)
            await message.reply(self, "Test successful!")
        elif message.content == "!test":
            token = await self.get_token()
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            username_test = requests.get(f"{API_URL}/users/{message.Author.name}", headers=headers)
            user_test = username_test.json() # test if username uses underscores
            user_test_error = user_test['error'] # test if username is in database
            username = message.Author.name.replace('_',' ') #replace underscores in usernames with spaces and define username
            # if username_test returns 404, then replace underscores with spaces and try again
            if user_test_error == None:
                userapi = requests.get(f"{API_URL}/users/{username}", headers=headers)
            else:
                userapi = requests.get(f"{API_URL}/users/{message.Author.name}", headers=headers)
            #userapi = requests.get(f"{API_URL}/users/{username}", headers=headers)
            user = userapi.json() #store user data in variable
            print ("formated Name")
            pprint(user, indent=2, depth=3)
            await message.reply(self, "Test successful!")
        elif message.content.startswith("!join"):
            args = message.content.split()
            if(len(args) != 2):
                await message.reply(self, "Usage: !join <Multiplayer Room ID> | Find ID from Match History Link NOT Invite Link")
            else:
                print(f"JOIN #mp-{args[1]}")
                await self.joinChannel(f"mp_{args[1]}")
                await self.sendMessage(f"mp_{args[1]}", "Hey there! I am [https://osu.ppy.sh/users/12792332/ Loki's] IRC Bot. !lokihelp for commands. Have fun playing!")
                await message.reply(self, f"I joined your multi room. Have fun playing! (#mp_{args[1]})")
        elif message.content == "%crychelp":
            await message.reply(self, "Welcome to Loki's IRC Bot! Developed by The Fantastic Loki")
            await message.reply(self, "Current List of Commands | % = Cryceptio | ! = Loki | $ = Mylk | @ = Kippz:")
            await message.reply(self, "%crychelp - Current Help Page")
            await message.reply(self, "!join <Match_history_id> - DM [https://osu.ppy.sh/users/12792332/ Loki] this to have Loki IRC join your multi room, !mp addref Fantastic Loki first!")
            await message.reply(self, '%twitch - Sends my Twitch link')
            await message.reply(self, "%skin - Sends a link to my OSU! Skin")
            await message.reply(self, "%discord - Sends a link to my discord in chat")
            await message.reply(self, 'Thanks to [https://osu.ppy.sh/users/13431764/ minisbett] for helping with the initial code & [https://osu.ppy.sh/users/12792332/ Loki] for use of the bot.')
        elif message.content == "%twitch":
            await message.reply(self, 'https://www.twitch.tv/cryceptio')
        elif message.content == "%skin":
            await message.reply(self, "http://www.mediafire.com/file/8eam0d8axrwa4qo/Parasyte_v1.1.osk")
        elif message.content == "%discord":
            await message.reply(self, "https://discord.com/invite/y5UpTHY")
        elif message.content == "$mylkhelp":
            await message.reply(self, "Welcome to Loki's IRC Bot! Developed by The Fantastic Loki")
            await message.reply(self, "Current List of Commands | $ = Mylk | % = Cryceptio | ! = Loki | @ = Kippz:")
            await message.reply(self, "$mylkhelp - Current Help Page")
            await message.reply(self, "!join <Match_history_id> - DM [https://osu.ppy.sh/users/12792332/ Loki] this to have Loki IRC join your multi room, !mp addref Fantastic Loki first!")
            await message.reply(self, '$twitch - Sends my Twitch link')
            await message.reply(self, "$skin - Sends my OSU! Skin")
            await message.reply(self, "$discord - Sends a link to my discord in chat")
            await message.reply(self, "$mylkstats - Sends custom stats output for raptorclaw 66")
            await message.reply(self, 'Thanks to [https://osu.ppy.sh/users/13431764/ minisbett] for helping with the initial code & [https://osu.ppy.sh/users/12792332/ Loki] for use of the bot.')
        elif message.content == "$twitch":
            await message.reply(self, 'https://www.twitch.tv/RaptorThumbs')
        elif message.content == "$skin":
            await message.reply(self, "https://www.dropbox.com/s/rb2qt885uj4z4lb/Nyxa%20v3.2.osk?dl=0")
        elif message.content == "$discord":
            await message.reply(self, "https://discord.com/invite/Na3zhJM")
        elif message.content == "$mylkstats":
            token = await self.get_token()

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            mylkapi = requests.get(f"{API_URL}/users/14652571", headers=headers)
            mylk = mylkapi.json()
            mylk_top = requests.get(f"{API_URL}/users/14652571/scores/best?limit=1", headers=headers)
            mylk_top_info = mylk_top.json()[0]
            #pprint(loki_top_info['beatmapset']['artist'], indent=2, depth=3)
            #pprint(loki_top_info['beatmapset'], indent=2, depth=3)
            await message.reply(self, f"Showing stats for [https://osu.ppy.sh/users/14652571/ raptorclaw 66] #{mylk['statistics']['global_rank']}")
            await message.reply(self, f"PP: {mylk['statistics']['pp']} | Accuracy: {round(mylk['statistics']['hit_accuracy'], 2)} | Playcount: {mylk['statistics']['play_count']:,}")
            await message.reply(self, f"Ranked Score: {mylk['statistics']['ranked_score']:,} (Lvl: {mylk['statistics']['level']['current']})")
            await message.reply(self, f"Total Score: {mylk['statistics']['total_score']:,}")
            await message.reply(self, f"Highest PP Play: {mylk_top_info['pp']}PP on [{mylk_top_info['beatmap']['url']} {mylk_top_info['beatmapset']['artist']} - {mylk_top_info['beatmapset']['title']} ({mylk_top_info['beatmap']['version']})]")
        elif message.content == "@kippzhelp":
            await message.reply(self, "Welcome to Loki's IRC Bot! Developed by The Fantastic Loki")
            await message.reply(self, "Current List of Commands | @ = Kippz | % = Cryceptio | $ = Mylk | ! = Loki:")
            await message.reply(self, "@kippzhelp - Current Help Page")
            await message.reply(self, "!join <Match_history_id> - DM [https://osu.ppy.sh/users/12792332/ Loki] this to have Loki IRC join your multi room, !mp addref Fantastic Loki first!")
            await message.reply(self, '@twitch - Sends my Twitch link')
            await message.reply(self, "@kippzstats - Sends custom stats output for MudKippz")
            await message.reply(self, 'Thanks to [https://osu.ppy.sh/users/13431764/ minisbett] for helping with the initial code & [https://osu.ppy.sh/users/12792332/ Loki] for use of the bot.')
        elif message.content == "@twitch":
            await message.reply(self, "Check out my [https://www.twitch.tv/kipprz/ Twitch Channel] where you can watch me play live.")
            await message.reply(self, 'https://www.twitch.tv/kipprz/')


x = LokiIRC(token="placeholder", nickname="fantastic_loki",reconnect=True, request_limit=15)

async def main():
    while True == True:
        text = input()
        await x.joinChannel(f"mp_{text}")
        print(f"BOT: Joined #mp_{text}")
        await x.sendMessage(f"mp_{text}", "Hey there! I am Loki's IRC Bot. !lokihelp for commands. Have fun playing!")
        

_thread.start_new_thread(x.run, ())

while x.running == False:
    sleep(1)

sleep(3)

asyncio.run(main())
