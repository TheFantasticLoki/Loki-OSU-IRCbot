import requests
from Mods import mods_dict


def black_magic(nobjs, acc, misses):
    n100 = round(-3.0 * ((acc - 1.0) * nobjs + misses) * 0.5)

    return n100


def str_to_dict(**kwargs) -> dict:
    return kwargs


def getBeatmap(key, id_, mods='nomod'):
    url = 'https://osu.ppy.sh/api/get_beatmaps'
    params = {'k': key, 'b': id_}

    if mods != 'nomod' and type(mods) != int:
        appble_mods = []
        [((appble_mods.append(i)) if i in ['dt', 'ht', 'hr', 'ez'] else '') for i in mods]
        params['mods'] = 0

        for i in appble_mods:
            params['mods'] += mods_dict[i]

    if type(mods) == int:
        mods = bit_analys(mods)
        for i in mods:
            if i not in [2, 16, 64, 256, 512]:
                mods.remove(i)
        params['mods'] = mods

    c = requests.get(url, params).text   

    return c


def add_spaces(message):
    message += ' <ENTER> '

    return message


def bit_analys(x):
    binary = bin(x)
    iterable = list(str(binary)[2:])
    iterable.reverse()
    lenght = len(iterable)
    res = list()
    for i in range(lenght):
        if int(iterable[i]) == 1:
            res.append(2**i)
    return res
        

def mod_convert(mods: str):
    mod_list = {
        'hardrock': 'hr',
        'doubletime': 'dt',
        'hidden': 'hd',
        'easy': 'ez',
        'flashlight': 'fl',
        'halftime': 'ht'
        }

    res = list()
    mods = mods[mods.index('+')+1:].strip('+').split()
    for i in mods:
        try:
            res.append(mod_list[i.lower()])
        except:
            continue

    return res
