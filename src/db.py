import sqlite3


class Database:
    def __init__(self, path: str = "data.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS allocations (
                user_id INTEGER PRIMARY KEY,
                role_id INTEGER NOT NULL
            )
            """)
        self.conn.commit()

    def get_allocations(self) -> dict[int, int]:
        rows = self.conn.execute("SELECT user_id, role_id FROM allocations")
        return dict(rows.fetchall())

    def add_allocation(self, user_id: int, role_id: int) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO allocations (user_id, role_id) VALUES (?, ?)",
                (user_id, role_id),
            )

    def close(self) -> None:
        self.conn.close()
