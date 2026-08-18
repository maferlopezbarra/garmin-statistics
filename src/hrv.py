import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "data/garmin.db"
HEALTH_DIR = BASE_DIR / "data/DI_CONNECT/DI-Connect-Wellness"


def hrv():
    with sqlite3.connect(DATABASE_DIR) as conn:

        conn.execute("""
        DROP TABLE IF EXISTS "hrv"
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS "hrv" (
            "date" TEXT PRIMARY KEY,
            "value" INTEGER,
            "baseline_upper" INTEGER,
            "baseline_lower" INTEGER,
            "status" TEXT,
            "percentage" INTEGER
        );
        """)

        for file_path in HEALTH_DIR.glob("*healthStatusData.json"):

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                for entry in data:
                    date = entry.get("calendarDate")
                    metrics = entry.get("metrics", [])

                    hrv_data = next(
                        (m for m in metrics if m.get("type") == "HRV"), None
                    )

                    if hrv_data:
                        value = hrv_data.get("value")
                        upper = hrv_data.get("baselineUpperLimit")
                        lower = hrv_data.get("baselineLowerLimit")
                        status = hrv_data.get("status")
                        percentage = hrv_data.get("percentage")

                        query_insert = """
                        INSERT OR IGNORE INTO "hrv" ("date", "value", "baseline_upper", "baseline_lower", "status", "percentage")
                        VALUES (?, ?, ?, ?, ?, ?)
                        """
                        conn.execute(
                            query_insert,
                            (date, value, upper, lower, status, percentage),
                        )

                print(f"{file_path.name} loaded")

            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
