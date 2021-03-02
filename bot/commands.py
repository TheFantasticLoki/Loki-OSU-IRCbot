import PP_Calculator
from pppredict.predict import predict

from util import str_to_dict, mod_convert, add_spaces
from re import findall
from lang_init import Initialization
from get_local import get_sample
import users
import maps


class Commands:
    def __init__(self):
        pass

    ''' +====-----------==--------=----------- ------------   ------- -- ---   -
    |
    | PP Calculation
    |
    | Use /np before command*
    |
    | Syntax: {prefix}pp mods='nomod' acc=[95, 100] miss=[0, 0] combo='max'
    | 
    | If force_miss num are not equals to force_acc,
    | for every force_acc with index > len(force_miss) will use force_miss[-1]
    |
    | *NOTE: kwargs must to be after args
    |
    | Returns message to send in format: For {title} [{dif_name}] ({OD}, {AR}, {CS}, {Stars}, {Len_in_minutes}) you'll get *[{i[PP]} for {i[ACC]}]
    |
    \==---=--------------------------- -------  ----   -   -'''

    @staticmethod
    def calc(*args) -> str:
        nick: str = args[-1]

        try:
            Action: str = args[1][0][args[2]]
        except:
            return get_sample("ERROR_NP_NEED", nick)

        PPs: str = ''
        args: list = args[0]
        beatmap_ID: str = findall(r'\d+', Action[Action.find('/b/')+3:])[0]

        # If +MOD_NAME in Action, collect them to mods parameter
        if '+' in Action:
            mods = mod_convert(Action)
        else:
            mods = 'nomod'

        # if there are args
        if args:
            acc = [0.95, 1]
            miss = [0, 0]
            combo = 'max'
            arg_list = {'mods': [],
                        'acc': acc,
                        'miss': miss,
                        'combo': combo}

            # if there are keyword args
            if any('=' in i for i in args):
                kwargs: list = list()

                for i in range(len(args)):
                    [(kwargs.append(i), args.remove(i)) if '=' in i else '' for i in args]

                for i in kwargs:
                    if 'mods=' in i:
                        ind =  kwargs.index(i)
                        kwargs[ind] =  kwargs[ind][:5] + '"' + kwargs[ind][5:] + '"'

                # bruh
                kwargs = eval('str_to_dict({})'.format(', '.join(kwargs)))

                # some ifs, maybe better solution soon
                if 'mods' in kwargs:
                    arg_list['mods'] = [i.lower() for i in [kwargs['mods'][i:i+2] for i in range(0, len(kwargs['mods']), 2)]]

                if 'acc' in kwargs:
                    arg_list['acc'].insert(0, kwargs['acc']/100)

                if 'miss' in kwargs:
                    arg_list['miss'].insert(0, kwargs['miss'])

                if 'combo' in kwargs:
                    arg_list['combo'] = kwargs['combo']

            # if there are non-keyword args
            if args:
                # all non-keyword args type is str. For acc and miss it should be int
                for i in range(len(args)):
                    if type(arg_list[list(arg_list.keys())[i]])  == 'str':
                        arg_list[list(arg_list.keys())[i]] = args[i]
                    elif list(arg_list.keys())[i] == 'mods':
                        arg_list[list(arg_list.keys())[i]] = [x.lower() for x in [args[i][x:x+2] for x in range(0, len(args[i]), 2)]]
                    elif list(arg_list.keys())[i] == 'acc':
                        arg_list[list(arg_list.keys())[i]].insert(0, float(args[i])/100)
                    else:
                        arg_list[list(arg_list.keys())[i]].insert(0, int(args[i]))

            # If user sets acc but not misses or vise versa we should equalize arrays
            if len(arg_list['acc']) != len(arg_list['miss']):

                dif =  abs(len(arg_list['acc']) - len(arg_list['miss']))

                if len(arg_list['acc']) > len(arg_list['miss']):

                    for i in range(dif):
                        arg_list['miss'].append(arg_list['miss'][-1])
                else:
                    for i in range(dif):
                        arg_list['acc'].append(arg_list['acc'][-1])

            if arg_list['mods'] is False:
                arg_list['mods'] = mods

        else:
            arg_list = {
                'mods': mods,
                'acc': [0.95, 1],
                'miss': [0, 0],
                'combo': 'max'
                }

        res: list = PP_Calculator.PP_Calculator(arg_list['combo'],
                                                   beatmap_ID,
                                                   arg_list ['mods'],
                                                   1,
                                                   arg_list['acc'],
                                                   arg_list['miss'])

        for i in range(len(res[1])):
            PPs += get_sample("PP_FOR", nick).format(res[1][i], arg_list['acc'][i]*100)

        message = get_sample("PP", nick).format(
                                                beatmap_ID,   # Beatmap ID
                                                res[2][0],  # Title
                                                res[2][1],  # Diff_name
                                                ' +{}'.format(''.join(arg_list['mods']).upper()) if arg_list['mods'] != 'nomod' else '',  # If mods used
                                                *[round(i, 2) for i in res[0]],  # AR and etc
                                                *[int(i) for i in divmod(int(res[2][2]), 60)],  # True Seconds
                                                PPs,  # PPs
                                                '({}x)'.format(arg_list['combo']) if arg_list['combo'] != 'max' else '')  # If combo param used

        return message


    # Actually a copy of calc function but with prediction.
    @staticmethod
    def calcPred(*args) -> str:
        nick: str = args[-1]

        try:
            Action: str = args[1][0][args[2]]
        except:
            return get_sample("ERROR_NP_NEED", nick)

        PPs: str = ''
        args: list = args[0]
        beatmap_ID: str = findall(r'\d+', Action[Action.find('/b/')+3:])[0]

        # If +MOD_NAME in Action, collect them to mods parameter
        if '+' in Action:
            mods = mod_convert(Action)
        else:
            mods = 'nomod'

        # if there are args
        if args:
            acc = [0.95, 1]
            miss = [0, 0]
            combo = 'max'
            arg_list = {'mods': [],
                        'acc': acc,
                        'miss': miss,
                        'combo': combo}

            # if there are keyword args
            if any('=' in i for i in args):
                kwargs: list = list()

                for i in range(len(args)):
                    [(kwargs.append(i), args.remove(i)) if '=' in i else '' for i in args]

                for i in kwargs:
                    if 'mods=' in i:
                        ind =  kwargs.index(i)
                        kwargs[ind] = kwargs[ind][:5] + '"' + kwargs[ind][5:] + '"'

                # bruh
                kwargs = eval('str_to_dict({})'.format(', '.join(kwargs)))

                # some ifs, maybe better solution soon
                if 'mods' in kwargs:
                    arg_list['mods'] = [i.lower() for i in [kwargs['mods'][i:i+2] for i in range(0, len(kwargs['mods']), 2)]]

                if 'acc' in kwargs:
                    arg_list['acc'].insert(0, kwargs['acc']/100)

                if 'miss' in kwargs:
                    arg_list['miss'].insert(0, kwargs['miss'])

                if 'combo' in kwargs:
                    arg_list['combo'] = kwargs['combo']

            # if there are non-keyword args
            if args:
                # all non-keyword args type is str. For acc and miss it should be int
                for i in range(len(args)):
                    if type(arg_list[list(arg_list.keys())[i]])  == 'str':
                        arg_list[list(arg_list.keys())[i]] = args[i]
                    elif list(arg_list.keys())[i] == 'mods':
                        arg_list[list(arg_list.keys())[i]] = [x.lower() for x in [args[i][x:x+2] for x in range(0, len(args[i]), 2)]]
                    elif list(arg_list.keys())[i] == 'acc':
                        arg_list[list(arg_list.keys())[i]].insert(0, float(args[i])/100)
                    else:
                        arg_list[list(arg_list.keys())[i]].insert(0, int(args[i]))

            # If user sets acc but not misses or vise versa we should equalize arrays
            if len(arg_list['acc']) != len(arg_list['miss']):

                dif =  abs(len(arg_list['acc']) - len(arg_list['miss']))

                if len(arg_list['acc']) > len(arg_list['miss']):

                    for i in range(dif):
                        arg_list['miss'].append(arg_list['miss'][-1])
                else:
                    for i in range(dif):
                        arg_list['acc'].append(arg_list['acc'][-1])

            if arg_list['mods'] is False:
                arg_list['mods'] = mods

        else:
            arg_list = {
                'mods': mods,
                'acc': [0.95, 1],
                'miss': [0, 0],
                'combo': 'max'
                }

        res: list = PP_Calculator.PP_Calculator(arg_list['combo'],
                                                   beatmap_ID,
                                                   arg_list ['mods'],
                                                   1,
                                                   arg_list['acc'],
                                                   arg_list['miss'])

        for i in range(len(res[1])):
            PPs += get_sample("PP_FOR", nick).format(res[1][i], arg_list['acc'][i]*100)

        Pred: predict.Prediction = predict.Prediction()
        Pred.predict(nick, float(res[0][3]))

        if Pred.predicted == 'Impossible':
            PP_Pred = get_sample("PP_PRED_IMPOSSIBLE", nick)
        else:
            PP_Pred: str = get_sample("PP_PRED_FUTURE",
                                      nick).format(PP_Calculator.PP_Calculator('max',
                                                                               beatmap_ID,
                                                                               arg_list['mods'],
                                                                               1,
                                                                               (Pred.predicted * 0.01,),
                                                                               (0, ))[1][0])

        message = get_sample("PP_PRED", nick).format(beatmap_ID,  # Beatmap ID
                                                     res[2][0],  # Title
                                                     res[2][1],  # Diff_name
                                                     ' +{}'.format(''.join(arg_list['mods']).upper()) if arg_list['mods'] != 'nomod' else '',  # If mods used
                                                     *[round(i, 2) for i in res[0]],  # AR and etc
                                                     *[int(i) for i in divmod(int(res[2][2]), 60)],  # True Seconds
                                                     PPs,  # PPs
                                                     '({}x)'.format(arg_list['combo']) if arg_list['combo'] != 'max' else '', # If combo param used
                                                     PP_Pred)  # Predicted pp
        return message

    # INFO
    @staticmethod
    def info(*args) -> str:
        nick = args[-1]
        mess = get_sample("INFO", nick)

        return mess

    # Set language
    staticmethod
    def setLang(*args) -> str:
        # Converts language to full name
        lang_dict = {
            'ru': 'Russian',
            'en': 'English',
            'de': 'Deutsch'
        }

        nick: str = args[-1]
        language: str = args[0][0]

        if language in lang_dict:
            language = lang_dict[language]
        else:
            return get_sample("ERROR_NO_LANGUAGE", nick)

        init = Initialization()
        init.set(nick, language)

        return get_sample("LANG_CHANGED", nick)

    # Maps - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Push map
    @staticmethod
    def map_push(*args) -> str:
        nick: str = args[-1]

        try:
            Action: str = args[1][0][args[2]]
        except:
            return get_sample("ERROR_NP_NEED", nick)

        beatmap_ID: str = int(findall(r'\d+', Action[Action.find('/b/') + 3:])[0])

        if users.Users.isPushMap(nick, beatmap_ID):
            return get_sample("ERROR_MAP_PUSHED_ALREADY", nick)
        else:
            maps.Maps.addMap(beatmap_ID)
            users.Users.addMapToPushed(nick, beatmap_ID)

        return get_sample("MAP_SUCCESS_PUSH", nick)

    # Drop map
    @staticmethod
    def map_drop(*args) -> str:
        nick: str = args[-1]

        try:
            Action: str = args[1][0][args[2]]
        except:
            return get_sample("ERROR_NP_NEED", nick)

        beatmap_ID: int = int(findall(r'\d+', Action[Action.find('/b/') + 3:])[0])

        if users.Users.isPushMap(nick, beatmap_ID):
            return get_sample("ERROR_MAP_PUSHED_ALREADY", nick)
        else:
            maps.Maps.dropMap(beatmap_ID)
            users.Users.addMapToPushed(nick, beatmap_ID)

        return get_sample("MAP_SUCCESS_DROP", nick)

    # Map top
    @staticmethod
    def map_top(*args) -> str:
        nick: str = args[-1]
        args_l: list = args[0]

        if not(args):
            args: str = 'user'
        else:
            args: str = args_l[0]

        top: list = maps.Maps.getTop(args, limit=5)
        message: str = ''

        for map in top:
            PPs = get_sample("PP_FOR", nick).format(eval(map[2])[3], 100)
            message += get_sample("MAP_TOP", nick).format(map[0],
                                                          map[1],
                                                          eval(map[4])[3],
                                                          PPs,
                                                          map[3])
            message = add_spaces(message)
        return message

    # Get last map in /np
    @staticmethod
    def map_recent(*args) -> str:
        nick: str = args[-1]
        recent: list = maps.Maps.getLastNP()

        accs: list = [0.95, 0.98, 0.99, 1]
        PPs: str = ''

        for i in range(len(accs)):
            PPs += get_sample("PP_FOR", nick).format(eval(recent[2])[i], accs[i] * 100)

        message: str = get_sample("MAP_RECENT", nick).format(recent[0], recent[1], eval(recent[4])[3], PPs)
        return message

    # Maps end - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Users  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Get target's stats. If no target, shows user's stats
    @staticmethod
    def user_getStat(*args) -> str:
        nick: str = args[-1]
        args: list = args[0]

        if args:
            to_see = args[0]
        else:
            to_see = nick

        stats = users.Users.getStat(to_see)

        message = get_sample("USER_STAT_FOR", nick).format(stats[0])
        message = add_spaces(message)

        message += get_sample("USER_STAT_ACC", nick).format(round(stats[1], 2))
        message = add_spaces(message)

        message += get_sample("USER_STAT_PP", nick).format(round(stats[2]))
        message = add_spaces(message)

        message += get_sample("USER_STAT_STARAVG", nick).format(round(stats[3], 2))

        return message


# List of commands and functions
cmd_list = {'pp': (Commands.calc, True),
            'pp_pred': (Commands.calcPred, True),
            'info': (Commands.info, False),
            'lang': (Commands.setLang, False),
            'push': (Commands.map_push, True),
            'drop': (Commands.map_drop, True),
            'top': (Commands.map_top, False),
            'recent': (Commands.map_recent, False),
            'stats': (Commands.user_getStat, False)}
