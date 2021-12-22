import configparser

# Config creation
config = configparser.ConfigParser()
config['TOKENDATA'] = {'client_id': '', 'client_secret': ''}
config["IRCTOKEN"] = {'token': '', 'nick': ''}
with open('config.ini', 'w') as configfile:
    config.write(configfile)