import math

def applyMods(bm: dict, mods='nomod') -> list:

    od = float(bm['diff_overall'])
    ar = float(bm['diff_approach'])
    cs = float(bm['diff_size'])

    # If nomod return beatmaps default params
    if mods == 'nomod' or not(any(i in ['dt', 'hf', 'hr', 'ez'] for i in mods)):
        return od, ar, cs

    OD_0_MS = 79.5
    OD_10_MS = 19.5
    AR_0_MS = 1800
    AR_5_MS = 1200
    AR_10_MS = 450

    OD_MS_STEP = 6
    AR_MS_STEP_05 = 150
    AR_MS_STEP_510 = 150
    
    OD_Multi = 1
    AR_Multi = 1
    CS_Multi = 1

    #OD

    if 'hr' in mods:
        OD_Multi *= 1.4
    elif 'ez' in mods:
        OD_Multi *= 0.5

    od *= OD_Multi
    OD_Millis = OD_0_MS - math.ceil(OD_MS_STEP * od)

    #AR

    if 'hr' in mods:
        AR_Multi *= 1.4
    elif 'ez' in mods:
        AR_Multi *= 0.5

    ar *= AR_Multi
    AR_Millis = (AR_0_MS - AR_MS_STEP_05 * ar) if ar <= 5 else (AR_5_MS - AR_MS_STEP_510 * (ar - 5))
                
    #CS

    if 'hr' in mods:
        CS_Multi *= 1.3
    if 'ez' in mods:
        CS_Multi *= 0.5

    cs *= CS_Multi

    OD_Millis = min(OD_0_MS, max(OD_10_MS, OD_Millis))
    AR_Millis = min(AR_0_MS, max(AR_10_MS, AR_Millis))

    # SpeeeeeeeeeeD

    speed = 1

    if 'dt' in mods:
        speed *= 1.5
    elif 'ht' in mods:
        speed *= 0.75

    InvSpeed = 1 / speed

    OD_Millis *= InvSpeed
    AR_Millis *= InvSpeed

    od = (OD_0_MS - OD_Millis) / OD_MS_STEP
    ar = ((AR_0_MS - AR_Millis) / AR_MS_STEP_05) if ar <= 5 else (5 + (AR_5_MS - AR_Millis) / AR_MS_STEP_510)

    return od, ar, cs
