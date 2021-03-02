import sqlite3


# Executor class. Uses for creating sql-query
class Executor:
    def __init__(self):
        pass

    @staticmethod
    def select(to: str, frm: str, where: str = None, order: str = None, limit: int = None) -> str:
        sql = f"select {to} from {frm}"

        if where:
            sql += f" where {where}"

        if order:
            sql += f" order by {order}"

        if limit:
            sql += f" limit {limit}"

        return sql

    @staticmethod
    def insert(into: str, columns: tuple, values: tuple):
        sql = f"insert into {into} {columns} values {values}"

        return sql

    @staticmethod
    def delete(frm: str, where: str = None):
        sql = f"delete from {frm}"

        if where:
            sql += f" where {where}"

        return sql

    @staticmethod
    def update(to: str, to_set: str, where: str = None):
        sql = f"update {to} set {to_set}"

        if where:
            sql += f" where {where}"

        return sql

    @staticmethod
    def execute(db, sql):
        db = sqlite3.connect(db)
        cur = db.cursor()

        cur.execute(sql)
        db.commit()
        res = cur.fetchall()

        cur.close()
        db.close()

        return res