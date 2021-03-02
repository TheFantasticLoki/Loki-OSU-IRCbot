import requests

from json import loads
from PP import PPCalc
from Mods_mask import applyMods
from util import getBeatmap

import configparser

# CONFIG ------------------

cfg = configparser.ConfigParser()
cfg.read('config.ini')

# -------------------------

def PP_Calculator(combo: int, beatmap_id: int=None, mods: list='nomod', score_v: int=1, f_accs: list=[0.90, 0.95, 1], f_miss: list=[0, 0, 0]) -> list:
    
    Beatmap = loads(getBeatmap(cfg['OSUAPI']['KEY'], beatmap_id, mods))[0]
    res = list()

    for i in range(len(f_accs)):
        if f_accs[i] == 1:
            combo = 'max'
        
        res.append(PPCalc(None, combo, score_v, Beatmap, mods, f_acc=f_accs[i], f_miss=f_miss[i]))

    return (*applyMods(Beatmap, mods=mods), round(float(Beatmap['difficultyrating']), 2)), [round(i) for i in res], [Beatmap['title'], Beatmap['version'], Beatmap['hit_length']]
