import urllib.request
import urllib.error
import json
import sqlite3
import time
import re
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "cache.db"

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                data TEXT,
                expires_at REAL
            )
        """)
init_db()

def get_github_metrics(path: str) -> tuple[str, str, str]:
    parts = path.strip("/").split("/")
    if len(parts) != 4 or parts[0] != "api" or parts[1] != "metrics":
        return "400 Bad Request", "application/json", json.dumps({"error": "Invalid format. Use /api/metrics/owner/repo"})
    
    owner, repo = parts[2], parts[3]
    
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", owner) or not re.fullmatch(r"[a-zA-Z0-9_.-]+", repo):
        return "400 Bad Request", "application/json", json.dumps({"error": "Invalid repository characters"})

    cache_key = f"{owner}/{repo}"

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT data, expires_at FROM cache WHERE key = ?", (cache_key,)
        ).fetchone()
        
        if row and row[1] > time.time():
            return "200 OK", "application/json; charset=utf-8", row[0]

    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "MetricsDashboard/1.0",
        "Accept": "application/vnd.github.v3+json"
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            metrics = {
                "name": data.get("full_name"),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "issues": data.get("open_issues_count", 0),
                "language": data.get("language", "Unknown"),
                "description": data.get("description", "No description.")
            }
            json_data = json.dumps(metrics)
            
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO cache (key, data, expires_at) VALUES (?, ?, ?)",
                    (cache_key, json_data, time.time() + 900)
                )
            
            return "200 OK", "application/json; charset=utf-8", json_data

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "404 Not Found", "application/json", json.dumps({"error": "Repository not found"})
        return "500 Internal Server Error", "application/json", json.dumps({"error": f"GitHub API error: {e.code}"})
    except Exception:
        return "503 Service Unavailable", "application/json", json.dumps({"error": "Network error. Check your proxy settings."})
