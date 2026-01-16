import sqlite3
import time
import requests
import schedule
import os
from datetime import datetime

# Configuration
DB_NAME = os.getenv("DB_FILE", "health_monitor.db")
WEBSITES = [
    "https://www.google.com",
    "https://github.com",
    "https://www.python.org",
    "https://stackoverflow.com",
    "https://www.wikipedia.org"
]

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uptracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            url TEXT NOT NULL,
            latency_ms REAL,
            status_code INTEGER,
            error TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized.")

def check_website(url):
    """Check a single website and return stats."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        latency = (time.time() - start_time) * 1000 # to ms
        return {
            "status_code": response.status_code,
            "latency": latency,
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": None,
            "latency": None,
            "error": str(e)
        }

def job():
    """The job to run every interval."""
    print(f"[{datetime.now()}] Starting health check...")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    for url in WEBSITES:
        result = check_website(url)
        c.execute('''
            INSERT INTO uptracking (timestamp, url, latency_ms, status_code, error)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, url, result["latency"], result["status_code"], result["error"]))
        
        status = result["status_code"] if result["status_code"] else "ERROR"
        latency = f"{result['latency']:.2f}ms" if result["latency"] else "N/A"
        print(f"  - {url}: {status} ({latency})")
        
    conn.commit()
    conn.close()
    print("Health check complete.\n")

def main():
    print("Starting Home Lab Health Monitor...")
    init_db()
    
    # Run once immediately
    job()
    
    # Schedule
    schedule.every(60).seconds.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
