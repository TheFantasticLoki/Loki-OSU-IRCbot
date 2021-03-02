import math

from Mods_mask import applyMods
from Acc import accCalc, accDist

'''
PPV2 Calculator. Returns pp: float

Translation from original OsuScore.cpp:
https://github.com/ppy/osu-performance/blob/a7e98ebea5bcb51c7f3463d8cc45ab15256f636e/src/performance/osu/OsuScore.cpp

Not direct because of idk. Will rewrite to easy comparable with original code soon
'''

def PPCalc(hits: list, combo: int, score_v: int, bm: dict, mods: list='nomod', f_acc: float=None, f_miss: float=None) -> float:
    if f_acc != None:
        if f_miss == None:
            hits = accDist(int(bm['count_normal']) + int(bm['count_slider']) + int(bm['count_spinner']),  0, f_acc)
        else:
            hits = accDist(int(bm['count_normal']) + int(bm['count_slider']) + int(bm['count_spinner']),  f_miss, f_acc)

    h300, h100, h50, miss = hits
    total = sum(hits)

    # If mods apply mods
    if mods != 'nomod':
        od, ar, cs = applyMods(bm, mods=mods)
    else:
        od, ar, cs = applyMods(bm)
    
    #ar = float(bm['diff_approach'])
    #od = float(bm['diff_overall'])
    #cs =  float(bm['diff_size'])

    max_combo = float(bm['max_combo'])

    try:
        if (combo > max_combo) or (combo <= 0) or (combo == 'max'):
            combo = max_combo
    except:
        combo = max_combo
    
    aim = float(bm['diff_aim'])
    speed = float(bm['diff_speed'])
    circles = int(bm['count_normal'])

    acc = accCalc(hits)

    #AIM
    aim_value = pow(5 * max(1, aim / 0.0675) - 4, 3) / 100000

    bonus_hits = total / 2000
    len_bonus = 0.95 + 0.4 * min(1.0, bonus_hits) + ((math.log10(bonus_hits) * 0.5) if total > 2000 else 0)
    miss_penality = pow(0.97, miss)
    combo_break = pow(combo, 0.8) / pow(max_combo, 0.8)

    aim_value *= len_bonus * miss_penality * combo_break

    ar_bonus = 1
    if ar > 10.33:
        ar_bonus += 0.3 * (ar - 10.33)
    elif ar < 8.0:
        low_ar_factor = 0.01 * (8 - ar)
        ar_bonus += low_ar_factor

    aim_value *= ar_bonus

    if mods != 'nomod':
        if 'hd' in mods:
            aim_value *= 1 + 0.04 * (12 - ar)
        if 'fl' in mods:
            aim_value *= 1 + 0.35 * min(1, total / 200) + ((0.3 * min(1, total-200) / 300) if total > 200 else 0) + (((total - 500) / 1200) if total > 500 else 0)

    acc_bonus = 0.5 + acc / 2
    od_bonus = 0.98 + pow(od, 2) / 2500
    od_bonus_speed = 0.96 + pow(od, 2) / 1600

    aim_value *= acc_bonus * od_bonus

    #SPEED
    speed_value = pow(5 * max(1, speed / 0.0675) - 4, 3) / 100000

    speed_value *= len_bonus * miss_penality * combo_break * (0.02 + acc) * od_bonus_speed * ar_bonus

    if mods != 'nomod':
        if 'hd' in mods:
            speed_value *= 1 + 0.04 * (12 - ar)

    accuracy = 0

    if score_v == 2:
        circles = total
        accuracy = acc
    else:
        if circles:
            accuracy = ((h300 - (total - circles)) * 6 + h100 * 2 + h50) / (circles * 6)

        accuracy = max(0, accuracy)

    #ACC
    acc_value = pow(1.52163, od) * pow(accuracy, 24) * 2.83
    acc_value *= min(1.15, pow(circles/1000, 0.3))

    if mods != 'nomod':
        if 'hd' in mods:
            acc_value *= 1.08
        if 'fl' in mods:
            acc_value *= 1.02

    multi = 1.12

    if mods != 'nomod':
        if 'nf' in mods:
            multi *= 0.90
        if 'so' in mods:
            multi *= 0.95

    return pow(pow(aim_value, 1.1) +
               pow(speed_value, 1.1) +
               pow(acc_value, 1.1), 1/1.1) * multi
