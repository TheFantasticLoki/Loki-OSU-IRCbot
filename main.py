import sys

sys.path.append('./bot/')
sys.path.append('./pp/')
sys.path.append('./lang/')
sys.path.append('./db/')

import bancho

if __name__ == '__main__':

    print('Lokis-IRC v1.0')
    print('Before running bot connect to channels by using bot.connect({channel_name})\n', '*WITHOUT #')
    print('To run bot use bot.run()')

    bot = bancho.Sur()
    bot.login()
    #bot.connect({multiplayer})
    bot.run()