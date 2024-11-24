import sqlite3 as sq

def create_db() -> None:
    with sq.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS code_snippets  (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            prompt TEXT NOT NULL,
                            gpt_code TEXT NOT NULL, 
                            mark BOOL NOT NULL
                        )''')
        conn.commit()


def add_code_to_db(prompt: str, code: str, mark: bool) -> None:
    with sq.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO code_snippets (prompt, gpt_code, mark) VALUES (?, ?, ?)", (prompt, code, mark))
        conn.commit()