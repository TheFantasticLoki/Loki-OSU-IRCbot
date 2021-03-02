from commands import cmd_list
from get_local import get_sample


PREFIX = '.'


# Handler class. Use cls.handle to process message
class Handler:
    def __init__(self):
        self.command: str = None
        self.answer: str = None

    def handle(self, user, msg, *args):
        if  'sotarks' in msg:       #Some
            return 'bruh'           #F
        elif 'bruh' in msg:         #U
            return 'sotarks'        #N
    
        if msg[0] == PREFIX:
            # Remove prefix
            msg = msg[len(PREFIX):].split()

            for command in cmd_list:
                if msg[0] == command:
                    msg.pop(0)
                    # Command list values looks like (command: func, need_action: bool)
                    if cmd_list[command][1] is True:
                        try:
                            res = cmd_list[command][0](msg, args, user)
                        except Exception as e:
                            print('Error in Handler.ActionIsTrue', str(e))
                            return get_sample("ERROR_SYNTAX", user)
                    else:
                        try:
                            res = cmd_list[command][0](msg, user)
                        except Exception as e:
                            print('Error in Handler.ActionIsFalse', str(e))
                            return get_sample("ERROR_SYNTAX", user)
                        
                    return res
