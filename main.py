import osu_irc

class LokiIRC(osu_irc.Client):

    async def onReady(self):
        print("Connected")

    async def onMessage(self, message):
        print(message.content)
        if message.content == "!lhelp":
            await message.reply(self, 'Welcome to Lokis IRC Bot')
            await message.reply(self, 'Current List of Commands:')
            await message.reply(self, '!twitch - Sends my Twitch link')
            await message.reply(self, '!skin - Sends link to my skins')
            await message.reply(self, '!discord - Sends permanent Discord Invite Link')
            await message.reply(self, '!vc - Sends Permanent Discord VC Invite Link that will join OSU! VC automatically')
            await message.reply(self, 'Thanks to minisbett for helping with the code')
        elif message.content == "!twitch":
            await message.reply(self, 'https://twitch.tv/TheFantasticLoki')
        elif message.content == "!skin":
            await message.reply(self, 'https://drive.google.com/drive/folders/1Kz2ag71kdRZ6Guy5WSxzQHl_2C9p5uHm?usp=sharing')
        elif message.content == "!discord":
            await message.reply(self, 'https://discord.gg/rNMeVdsw4e')
        elif message.content == "!vc":
            await message.reply(self, 'https://discord.gg/PjaCQyefHu')
        elif message.content.startswith("!join"):
            args = message.content.split()
            if(len(args) != 2):
                await message.reply(self, "Usage: !join <Multiplayer Room ID>")
            else:
                print(f"Joining mp room {args[1]}")
                await self.joinChannel(f"mp_{args[1]}")
                await self.sendMessage(f"mp_{args[1]}", "Hey there! I am Lokis IRC Bot. !lhelp for commands. Have fun playing!")
                await message.reply(self, f"I joined your multi room. Have fun playing! (#mp_{args[1]})")

x = LokiIRC(token="34f2f6cc", nickname="fantastic_loki",reconnect=True, request_limit=15)
x.run()