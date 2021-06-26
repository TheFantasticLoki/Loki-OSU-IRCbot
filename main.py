import osu_irc
import _thread
import asyncio
from time import sleep

class LokiIRC(osu_irc.Client):

    async def onReady(self):
        print("BOT: Connected")

    async def onMessage(self, message):
        print(f'INPUT: {message.content}')
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
            await message.reply(self, 'Thanks to minisbett for helping with the initial code')
        elif message.content == "!twitch":
            await message.reply(self, "Check out my [https://twitch.tv/TheFantasticLoki/ Twitch Channel] where you can watch me play live.")
            await message.reply(self, 'https://twitch.tv/TheFantasticLoki')
        elif message.content == "!skin":
            await message.reply(self, "Check out my [https://drive.google.com/drive/folders/1Kz2ag71kdRZ6Guy5WSxzQHl_2C9p5uHm?usp=sharing/ Custom Skin] focused on minimalism, good for aim and sightreading! Latest Version: V4")
            await message.reply(self, 'https://drive.google.com/drive/folders/1Kz2ag71kdRZ6Guy5WSxzQHl_2C9p5uHm?usp=sharing')
        elif message.content == "!discord":
            await message.reply(self, 'Come join my [https://discord.gg/rNMeVdsw4e/ discord] where you can find channels for Games such as OSU!, CSGO, Minecraft, and other topics.')
            await message.reply(self, 'https://discord.gg/rNMeVdsw4e')
        elif message.content == "!vc":
            await message.reply(self, "Come Join this [https://discord.gg/PjaCQyefHu/ Voice Chat]! It will join directly to the OSU! VC in my server.")
            await message.reply(self, 'https://discord.gg/PjaCQyefHu/')
        elif message.content == "!lokistats":
            await message.reply(self, 'PP: 2.8K')
            await message.reply(self, 'ACC: 91.4%')
            await message.reply(self, 'Highest PP Play: 238PP')
            await message.reply(self, 'Achieved Supremacy Medal at #1,000,000')
            await message.reply(self, 'Notable Scores:')
            await message.reply(self, '[https://i.imgur.com/MtgdwHp.png/ Cycle Hit HR 20 Miss 598 Combo Pass]')
            await message.reply(self, '[https://i.imgur.com/g8Dwy0Q.png/ Crystalia - Luminosity 7.88* 28 Miss Pass]')
            await message.reply(self, '[https://i.imgur.com/htrui5D.png/ Psalm dla Ciebie - Poloz mnie na swym ramieniu 8.21* 66 Miss Choke]')
        elif message.content == "!collections":
            await message.reply(self, "Check out some of my [https://osustats.ppy.sh/collections/1?user=12792332/ Collections]. Import and Use with [https://github.com/Piotrekol/CollectionManager/releases/ Collections Manager by Piotrekol] or just view inside browser.")
            await message.reply(self, "[https://osustats.ppy.sh/collection/5924/ Multiplayer Collection] - Loki's Hand Picked Maps for playing Multi. Contains the following types of maps: Fun, Challenge, Banger Songs, Intresting Mapping, etc.")
            await message.reply(self, "[https://osustats.ppy.sh/collection/5925/ Stream Consistency Collection] - Collection of Maps for Practicing Streams.")
            await message.reply(self, "[https://osustats.ppy.sh/collection/5927/ Bangers Collection] - A collection all about good music meant to get you hyped or groovin.")
        elif message.content.startswith("!join"):
            args = message.content.split()
            if(len(args) != 2):
                await message.reply(self, "Usage: !join <Multiplayer Room ID> | Find ID from Match History Link NOT Invite Link")
            else:
                print(f"JOIN #mp-{args[1]}")
                await self.joinChannel(f"mp_{args[1]}")
                await self.sendMessage(f"mp_{args[1]}", "Hey there! I am [https://osu.ppy.sh/users/12792332/ Loki's] IRC Bot. !lokihelp for commands. Have fun playing!")
                await message.reply(self, f"I joined your multi room. Have fun playing! (#mp_{args[1]})")
        elif message.content == "%twitch":
            await message.reply(self, 'https://www.twitch.tv/cryceptio')
        elif message.content == "%skin":
            await message.reply(self, "http://www.mediafire.com/file/8eam0d8axrwa4qo/Parasyte_v1.1.osk")
        elif message.content == "%discord":
            await message.reply(self, "https://discord.com/invite/y5UpTHY")
        elif message.content == "$twitch":
            await message.reply(self, 'https://www.twitch.tv/RaptorThumbs')
        elif message.content == "$skin":
            await message.reply(self, "https://www.dropbox.com/s/rb2qt885uj4z4lb/Nyxa%20v3.2.osk?dl=0")
        elif message.content == "$discord":
            await message.reply(self, "https://discord.com/invite/Na3zhJM")
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
        elif message.content == "@kippzstats":
            await message.reply(self, 'PP: 8.6K')
            await message.reply(self, 'ACC: 98.47%')
            await message.reply(self, 'Highest PP Play: 492')
            await message.reply(self, 'Highest Ranked Pass: 9.64*')
            await message.reply(self, 'Notable Scores:')
            await message.reply(self, '[https://www.youtube.com/watch?v=I7R3uzbUNL4&ab_channel=MudKippz/ Astrid HDHR FC #6 Global]')
            await message.reply(self, '[https://www.youtube.com/watch?v=w9pWF6iS_8U/ Cory in the House 4th DT Fc Global]')
            await message.reply(self, '[https://www.youtube.com/watch?v=Kz5IlKSbRps/ Horizon Blue NM FC #22 Global]')


x = LokiIRC(token="XXXXXX", nickname="fantastic_loki",reconnect=True, request_limit=15)

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
