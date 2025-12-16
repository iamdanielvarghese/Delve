# database_manager.py
import sqlite3
import datetime


class DatabaseManager:
    def __init__(self, db_name="miner_scores.sqlite"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Creates the high_scores table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Updated Schema for Chapter 4.3 of your report
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level_num INTEGER,
                seed INTEGER,
                time_taken REAL,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_score(self, level_num, seed, time_taken):
        """Saves a completed run to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO high_scores (level_num, seed, time_taken, timestamp) VALUES (?, ?, ?, ?)",
                       (level_num, seed, time_taken, timestamp))

        conn.commit()
        conn.close()
        print(f"[DB] Score Saved: Level {level_num} in {time_taken:.2f}s")

    def get_top_scores(self, limit=5):
        """Fetches the top 5 fastest times across all levels."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Order by time_taken ASC (Ascending) because lower time is better
        cursor.execute(
            "SELECT level_num, time_taken, timestamp FROM high_scores ORDER BY time_taken ASC LIMIT ?", (limit,))
        results = cursor.fetchall()
        conn.close()
        return results
