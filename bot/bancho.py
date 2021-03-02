'''Refactoring soon'''

import socket
import re
import asyncio
import Handler
import configparser
import lang_init
from users import Users as us
from maps import Maps as mp

ERR_DECODE = "Somebody used wrong chars"

# CONFIG ------------------

cfg = configparser.ConfigParser()
cfg.read('config.ini')

# -------------------------


# Some patterns to find
ReUsername: "re.Pattern" = re.compile(r'^:(.+?)!')
ReRoomName: "re.Pattern" = re.compile(r'PRIVMSG (.+?) :')
ReContent: "re.Pattern" = re.compile(r'^:.+? :(.+)')

# Data to login

'''++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Main bot class. Make sure you set PASS & NICK in config file.
|
| *NOTE: There is a limit to traffic.
|
|             Method                          #      Info
|
| login()                                     #  Sets connection to IRC by using cls.NICK and cls.PASS
|
| connect(channel: str)                       #  Adds channel to cls.Channels.
|
| run()                                       #  Starts main loop. If cls.Channels not empty, connects to channels in it
\==---=-------------+------------- -------  ----   -   -'''


class Sur:
    def __init__(self):

        self.running: bool = False

        self.request_limit: int = int(cfg.get('BANCHO', 'REQUEST_LIMIT'))
        self.stored_traffic: list = list()
        self.traffic: int = 0
        self.query_running: bool = False

        self.PASS: str = cfg.get('BANCHO', 'PASS')
        self.NICK: str = cfg.get('BANCHO', 'NICK')
        self.NETWORK: str = 'irc.ppy.sh'
        self.PORT: int = 6667

        self.irc: socket.socket = None

        self.Channels: list = list()
        self.Handler: Handler.Handler = Handler.Handler()
        self.ActDict: dict = {}
        self.Ans: str = ''

    def login(self) -> None:
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((self.NETWORK, self.PORT))
        self.irc.send(bytearray('PASS {}\r\n'.format(self.PASS), encoding='utf-8'))
        self.irc.send(bytearray('NICK {}\r\n'.format(self.NICK), encoding='utf-8'))
        self.irc.send(bytearray('USER {} {} {}\r\n'.format(self.NICK, self.NICK, self.NICK), encoding='utf-8'))

    def connect(self, channel: str) -> None:
        self.Channels.append(channel)

    # Starts main loop
    def run(self) -> None:
        loop: asyncio.new_event_loop = asyncio.new_event_loop()
        loop.run_until_complete(self.start())

    # Main loop
    async def start(self) -> None:
        print("start")
        self.running = 1

        print('Starting...')

        if self.Channels != ():
            for channel in self.Channels:
                print(f"Joining {channel}")
                await self.send_content(f"JOIN #{channel}\r\n")
                print(channel)
        while self.running:

            self.traffic = 0
            self.query_running = True

            # lets listen...
            asyncio.ensure_future(trafficQuery(self))
            await self.eventListener()

    # Listener
    async def eventListener(self) -> None:
        while self.running:
            self.Ans = self.getAnswer().split(str('\n'))

            for line in self.Ans:
                # just ignore quit messages
                if 'cho@ppy.sh QUIT' in line:
                    continue

                # On action
                elif 'ACTION' in line:
                    try:
                        self.content = re.findall(ReContent, line)[0]
                        self.user = re.findall(ReUsername, line)[0]
                        self.channel = re.findall(ReRoomName, line)[0]

                        await self.action(self.user, self.content)
                    except Exception as e:
                        print('Error in ACTION', str(e))
                        continue

                # On private message
                elif 'PRIVMSG' in line:
                    self.content = re.findall(ReContent, line)[0]
                    self.user = re.findall(ReUsername, line)[0]
                    self.channel = re.findall(ReRoomName, line)[0]

                    try:
                        if self.user != 'BanchoBot':
                            # set language to a new user
                            lang = lang_init.Initialization()
                            lang.new(self.user)

                            # Update user's stats if there are 24h since last update
                            us.dailyUpdate(self.user)
                    except Exception as e:
                        print('Error in PRIVMSG', str(e))
                        continue

                    await self.private(self.user, self.content, self.channel)
                elif 'PING' in line:
                    await self.send_content("PONG :cho.ppy.sh\r\n")

                await asyncio.sleep(0)

    async def private(self, nick: str, message: str, channel: str) -> None:
        asyncio.ensure_future(self.onPrivate(nick, message, channel))

    # Calls on PRIVMSG
    async def onPrivate(self, user: str, msg: str, channel: str):
        if channel == self.NICK:
            channel = user

        msg = self.Handler.handle(user, msg, self.ActDict)

        if msg:
            asyncio.ensure_future(self.send_content('PRIVMSG {} {}\r\n'.format(channel, msg)))

    async def action(self, user: str, msg: str) -> None:
        asyncio.ensure_future(self.onAction(user, msg))

    # Calls on action
    async def onAction(self, user: str, msg: str) -> None:
        # Add action in action dict
        self.ActDict[user] = msg

        # Add to base last used /np
        beatmap = re.findall(r'\d+', msg[msg.find('/b/') + 3:])[0]
        mp.addLastNP(beatmap)

    # Sends to Bancho
    async def send_content(self, req: str) -> None:
        if self.traffic <= self.request_limit:
            # Multiline support
            if '<ENTER>' in req:
                splitted_req = req.split('<ENTER>')
                channel = splitted_req[0].split()[1]

                for message in splitted_req:
                    if message == '':
                        continue
                    if 'PRIVMSG' in message:
                        self.irc.send(bytearray(message, encoding='utf-8'))
                        continue
                    message = f'\r\nPRIVMSG {channel} {message}'
                    self.irc.send(bytearray(message, encoding='utf-8'))
            else:
                self.irc.send(bytearray(req, encoding='utf-8'))

            asyncio.ensure_future(addTraffic(self))
        else:
            self.stored_traffic.append(req)

    # Reads from socket.
    def getAnswer(self, debug=False) -> str:
        try:
            if debug:
                data = self.irc.recv(4096)
                print(data.decode('utf-8'))
                return

            data = self.irc.recv(4096)
            return data.decode('utf-8')
        except:
            print(ERR_DECODE)
            return


# Adds traffic for 30 seconds.
async def addTraffic(cls: Sur) -> None:
    cls.traffic += 1
    await asyncio.sleep(30)
    cls.traffic -= 1

# If traffic more than limit, adds request to storage.
async def trafficQuery(cls: Sur) -> None:
    while cls.running and cls.query_running:
        if cls.traffic <= (cls.request_limit-1) and len(cls.stored_traffic) > 0:
            req = cls.stored_traffic.pop(0)
            await cls.send_content(req)
        else:
            await asyncio.sleep(0.05)
