import sqlite3 as sq

def create_db() -> None:
    global db, cur
    db = sq.connect(r'database.db')
    cur = db.cursor()

    # Table Profiles
    cur.execute('''CREATE TABLE IF NOT EXISTS code_snippets  (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            prompt TEXT NOT NULL,
                            gpt_code TEXT NOT NULL
                        )''')
    db.commit()


def add_code_to_db(prompt: str, code: str) -> None:
    cur.execute(f"INSERT INTO code_snippets (prompt, gpt_codes) VALUES ('{prompt}, {code}')")
    db.commit()
