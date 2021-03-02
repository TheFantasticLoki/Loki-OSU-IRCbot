import os
import sqlite3

from time import time
from pppredict.userApi import user as us
from sql import Executor


class Users:
    db_name = "users.db"

    def __init__(self):
        pass

    # Adds map to pushed list
    @classmethod
    def addMapToPushed(cls, user: str, beatmap: int) -> None:
        if cls.exists(user):
            pushed = cls.getPushedMaps(user)
            pushed.append(beatmap)

            cls.execute(Executor.update("user", f"pushed='{pushed}'"))
        else:
            cls.addStat(user)
            cls.addMapToPushed(user, beatmap)

    # Gets user's pushed maps list
    @classmethod
    def getPushedMaps(cls, user: str) -> list:
        pushed = cls.execute(Executor.select("pushed", "user", f"name='{user}'"))[0][0]

        if pushed:
            pushed = eval(pushed)
        else:
            pushed = list()

        return pushed

    # is map pushed by user ???
    @classmethod
    def isPushMap(cls, user: str, beatmap: int) -> bool:
        if beatmap in cls.getPushedMaps(user):
            return True
        return False

    # Adds user's stat to table. Used to prevent long commands processing
    @classmethod
    def addStat(cls, user: str) -> None:
        if cls.exists(user):
            return

        user_data = us.User()
        user_data.setUser(user)

        acc = user_data.acc
        pp = user_data.pp

        star_avg = user_data.calcAvgStar()

        now = round(time())

        cls.execute(Executor.insert("user",
                                    ("name", "acc", "pp", "star_avg", "pushed", "last_use"),
                                    (user, acc, pp, star_avg, '[]', now)))

    # Gets user's stats. Used to prevent long commands processing
    @classmethod
    def getStat(cls, user: str) -> list:
        if not(cls.exists(user)):
            cls.addStat(user)

        stat = cls.execute(Executor.select("*", "user", f"name='{user}'"))

        stat = stat[0]

        return stat

    # Get last user's stat update.
    @classmethod
    def getLastUpdate(cls, user: str) -> int:
        last = cls.getStat(user)[5]

        return last

    # If there are more than 24h from last update, we should get stats again
    @classmethod
    def dailyUpdate(cls, user: str, debug: bool = False) -> None:
        now = round(time())

        if debug:
            now = 999999999999999

        if round((now - cls.getLastUpdate(user))/60/60) > 24:
            user_data = us.User()
            user_data.setUser(user)

            acc = user_data.acc
            pp = user_data.pp

            star_avg = user_data.calcAvgStar()

            now = round(time())

            cls.execute(Executor.update("user", f"acc={acc}, pp={pp}, star_avg={star_avg}, last_use={now}",
                                        f"name='{user}'"))

    # Execute sql query
    @classmethod
    def execute(cls, sql: str) -> list:
        if not (os.path.exists(f"./{cls.db_name}")):
            db = sqlite3.connect(cls.db_name)
            cur = db.cursor()

            # Let's create tables for users

            cur.execute("CREATE TABLE user (name NVARCHAR(20), acc FLOAT, pp FLOAT, star_avg FLOAT, pushed NVARCHAR(1000), last_use INT(20))")

            db.commit()

        else:
            db = sqlite3.connect(cls.db_name)
            cur = db.cursor()

        cur.execute(sql)
        db.commit()
        res = cur.fetchall()

        cur.close()
        db.close()

        return res

    # Check for user in db
    @classmethod
    def exists(cls, user: str) -> bool:
        try:
            if cls.execute(Executor.select("*", "user", f"name='{user}'")):
                return True
        except:
            return False

        return False
