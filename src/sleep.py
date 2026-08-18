import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "data/garmin.db"
SLEEP_DIR = BASE_DIR / "data/DI_CONNECT/DI-Connect-Wellness"


def sleep():
    with sqlite3.connect(DATABASE_DIR) as conn:

        conn.execute("""
            DROP TABLE IF EXISTS "sleep"
        """)
        
        conn.execute("""
        CREATE TABLE IF NOT EXISTS "sleep" (
            "date" TEXT PRIMARY KEY,
            "stress" REAL,
            "score" INTEGER
        );
        """)

        for file_path in SLEEP_DIR.glob("*sleepData.json"):

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    for sleep in data:
                        date = sleep.get("calendarDate")
                        stress = sleep.get("avgSleepStress")
                        sleep_scores = sleep.get("sleepScores")
                        score = (
                            sleep_scores.get("overallScore") if sleep_scores else None
                        )

                        query_insert = """
                        INSERT OR IGNORE INTO "sleep" ("date", "stress", "score")
                        VALUES (?, ?, ?)
                        """
                        conn.execute(query_insert, (date, stress, score))

                print(f"{file_path.name} loaded")

            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
