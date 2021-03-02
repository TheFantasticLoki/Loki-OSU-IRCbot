from util import black_magic

# Acc calculation
def accCalc(hits: list) -> float:
    h300, h100, h50, miss = hits
    total: int = sum(hits)

    if total != 0:
        return (h300 * 300 + h100 * 100 + h50 * 50) / (total *300)

    else:
        return 1.0

# Hits calculation
def accDist(objs: int, misses: int, acc: float) -> list:
    best300s = getBest300s(objs, misses, acc)
    best100s = int(getBest100s(objs, misses, acc))

    return best300s, best100s, objs - best300s - best100s - misses, misses

# Calculate 300s
def getBest300s(objs: int, misses: int, acc: float) -> int:
    best300s: int = objs - getBest100s(objs, misses, acc) - misses

    return best300s

# Calculate 100s
def getBest100s(objs: int, misses: int, acc: float) -> int:
    return black_magic(objs, acc, misses)

