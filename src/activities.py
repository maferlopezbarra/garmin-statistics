import json
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "data/garmin.db"
ACTIVITIES_DIR = next((BASE_DIR / "data/DI_CONNECT/DI-Connect-Fitness").glob("*summarizedActivities.json"))

def running():
    
    with sqlite3.connect(DATABASE_DIR) as conn:

        conn.execute("""
        DROP TABLE IF EXISTS "activities"
        """)

        conn.execute("""
        CREATE TABLE "activities" (
            "id" INTEGER,
            "type" TEXT NOT NULL,
            "date" NUMERIC NOT NULL,
            "distance" REAL,
            "vo2" INTEGER,
            "speed" REAL,
            "avg_hr" INTEGER,
            "max_hr" INTEGER,
            "cadence" INTEGER,
            "stride_length" REAL,
            PRIMARY KEY("id")
        );
        """)

        try:
            with open(ACTIVITIES_DIR, "r", encoding="utf-8") as f:
                data = json.load(f)

            activities = data[0]["summarizedActivitiesExport"]

            for activity in activities:
                act_id = activity.get("activityId")
                act_type = activity.get("activityType", "unknown")
                date = datetime.fromtimestamp(
                    int(activity.get("beginTimestamp")) / 1000
                    ).strftime('%Y-%m-%d')
                distance = activity.get("distance")
                vo2 = activity.get("vO2MaxValue")
                speed = activity.get("avgSpeed")
                avg_hr = activity.get("avgHr")
                max_hr = activity.get("maxHr")
                cadence = activity.get("avgRunCadence")
                stride_length = activity.get("avgStrideLength")

                query_insert = f"""
                INSERT OR IGNORE INTO "activities" (
                    "id", "type", "date", "distance", "vo2", "speed", 
                    "avg_hr", "max_hr", "cadence", "stride_length"
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                conn.execute(query_insert, (
                    act_id, act_type, date, distance, vo2, speed,
                    avg_hr, max_hr, cadence, stride_length
                ))
        except Exception as e:
            print(f"Error processing {ACTIVITIES_DIR.name}: {e}")

        conn.execute("""
        CREATE VIEW IF NOT EXISTS "running" AS
        SELECT 
            "id", 
            "date",
            ROUND("distance" / 100000, 2) AS "distance", 
            ROUND(100 / ("speed" * 60), 2) AS "pace", 
            ROUND("vo2") AS "vo2", 
            ROUND("avg_hr") AS "avg_hr", 
            ROUND("max_hr") AS "max_hr", 
            ROUND("cadence") AS "cadence", 
            ROUND("stride_length", 2) AS "stride_length" 
        FROM "activities" 
        WHERE "type" = 'running';
        """)

    print(f"{ACTIVITIES_DIR.name} loaded")