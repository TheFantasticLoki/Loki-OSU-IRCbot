import sqlite3
import os
import PP_Calculator

from sql import Executor
from random import randint


class Maps:
    db_name = 'maps.db'

    def __init__(self):
        pass

    # Adds map to table, if already exists, push it.
    @classmethod
    def addMap(cls, beatmap, category='user'):
        if cls.exist(beatmap):
            if category == 'np':
                return
            cls.pushMap(beatmap)
        else:
            # Let's add map to base, but first, we need to calculate some data...

            # PP Calculation initializaion...

            beatmap_data = PP_Calculator.PP_Calculator('max', beatmap, f_accs=[0.95, 0.98, 0.99, 1], f_miss=[0,0,0,0])

            title = f"{beatmap_data[2][0]} [{beatmap_data[2][1]}]"
            pps = beatmap_data[1]
            data = beatmap_data[0]

            # Insert into table

            cls.execute(Executor.insert(category, ("beatmap", "title", "pp", "rating", "data"),
                                        (beatmap, title, str(pps), 1, str(data))))

    # Adds 1 to map's rating
    @classmethod
    def pushMap(cls, beatmap: int) -> None:
        cls.execute(Executor.update('user', 'rating=rating+1', f"beatmap='{beatmap}'"))

    # Takes 1 from map's rating. If not exists, add map to table
    @classmethod
    def dropMap(cls, beatmap: int) -> None:
        if cls.exist(beatmap):
            cls.execute(Executor.update('user', 'rating=rating-1', f"beatmap='{beatmap}'"))
            return

        cls.addMap(beatmap)
        cls.dropMap(beatmap)

    # Gets maps from table ordered by rating
    @classmethod
    def getTop(cls, by: str = 'user', limit: int = 10) -> list:
        if limit == 'max':
            top = cls.execute(Executor.select("*", f"{by}", order="rating desc"))

            return top

        top = cls.execute(Executor.select("*", f"{by}", order="rating desc", limit=limit))

        return top

    # Adds last used /np to table
    @classmethod
    def addLastNP(cls, beatmap: int) -> None:
        # Delete from np last song
        cls.execute(Executor.delete('np'))
        # Insert to np last song
        cls.addMap(beatmap, 'np')

    # Gets last used /np
    @classmethod
    def getLastNP(cls) -> list:
        last = cls.execute(Executor.select('*', 'np'))[0]

        return last

    # Gets random map form user's top
    @classmethod
    def getRandomTopMap(cls) -> list:
        top = cls.getTop(limit='max')
        top = top[randint(0, len(top)-1)]

        return top

    # Deletes all data from table
    @classmethod
    def truncateTable(cls, table: str = 'month') -> None:
        cls.execute(Executor.delete(table))

    # Executes sql query
    @classmethod
    def execute(cls, sql: str) -> list:
        if not(os.path.exists(f"./{cls.db_name}")):
            db = sqlite3.connect(cls.db_name)
            cur = db.cursor()

            # Let's create tables for map top

            # User top
            cur.execute("CREATE TABLE user (beatmap INT(20), title NVARCHAR(1000), pp NVARCHAR(1000), rating INT(10), data NVARCHAR(1000))")

            # Month top
            cur.execute("CREATE TABLE month (beatmap INT(20), title NVARCHAR(1000), pp NVARCHAR(1000), rating INT(10), data NVARCHAR(1000))")

            # Last /np
            cur.execute("CREATE TABLE np (beatmap INT(20), title NVARCHAR(1000), pp NVARCHAR(1000), rating INT(10), data NVARCHAR(1000))")

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

    # Check for map in table
    @classmethod
    def exist(cls, beatmap: int) -> bool:
        try:
            if cls.execute(Executor.select("beatmap", "user", f"beatmap={beatmap}")):
                return True
        except:
            return False

        return False
