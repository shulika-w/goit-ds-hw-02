import sqlite3


def delete_user(user_id):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        con.commit()


if __name__ == '__main__':
    delete_user(3)
