import sqlite3

from config import DATABASE_PATH

STARTING_SNOWBALLS = 20

def initialize():
    sqlconn = sqlite3.connect(DATABASE_PATH)
    sqlconn.execute("CREATE TABLE IF NOT EXISTS members (uid INT PRIMARY KEY, snowballs INT, hits INT);")
    sqlconn.commit()
    sqlconn.close()

def _db_read(query):
    sqlconn = sqlite3.connect(DATABASE_PATH)
    results = sqlconn.execute(*query).fetchall()
    sqlconn.close()
    return results

def _db_write(query):
    sqlconn = sqlite3.connect(DATABASE_PATH)
    sqlconn.execute(*query)
    sqlconn.commit()
    sqlconn.close()

def get_hits(uid: int) -> int:
    if not user_exists(uid):
        return 0
    query = ("SELECT hits FROM members WHERE uid=?", [uid])
    results = _db_read(query)
    return results[0][0]

def user_exists(uid: int) -> bool:
    query = ("SELECT * FROM members WHERE uid=?", [uid])
    results = _db_read(query)
    return len(results) != 0

def get_snowballs(uid: int) -> int:
    if not user_exists(uid):
        return STARTING_SNOWBALLS
    query = ("SELECT snowballs FROM members WHERE uid=?", [uid])
    results = _db_read(query)
    return results[0][0]

# Returns if a snowball was successfully used. Will return false if user has none left
def use_snowball(uid: int) -> bool:
    cnt = get_snowballs(uid)
    if cnt > 0:
        if user_exists(uid):
            query = ("UPDATE members SET snowballs=? WHERE uid=?", [cnt - 1, uid])
        else:
            query = ("INSERT INTO members (uid, snowballs, hits) VALUES (?, ?, ?)", [uid, cnt - 1, 0])
        _db_write(query)
        return True
    return False

def snowball_hit(uid: int, num: int = 1):
    if user_exists(uid):
        hits = get_hits(uid)
        query = ("UPDATE members SET hits=? WHERE uid=?", [hits + num, uid])
        _db_write(query)
    else:
        query = ("INSERT INTO members (uid, snowballs, hits) VALUES (?, ?, ?)", [uid, STARTING_SNOWBALLS, num])
        _db_write(query)

def get_leaders() -> list[tuple[str, int]]:
    query = ("SELECT uid, hits FROM members ORDER BY hits DESC LIMIT 10",)
    results = _db_read(query)
    return results
