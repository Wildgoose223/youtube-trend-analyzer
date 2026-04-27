# YouTube Gaming Trend Analyzer

A Python-based data pipeline that extracts trending gaming videos from YouTube, processes the data, identifies popular games, and stores the results in a PostgreSQL database for tracking trends over time.

---

## Overview

This project pulls trending gaming videos using the YouTube Data API, cleans and analyzes titles, matches them against a **database-driven game library**, and stores structured results in PostgreSQL.

Each run captures a snapshot of trending data and continuously improves accuracy by tracking unknown terms.

---

## Features

* Pulls trending gaming videos (YouTube Category 20)
* Cleans titles using regex
* Matches game titles using a **database-driven alias system**
* Supports **multi-word game detection** (e.g., "Call of Duty", "Grand Theft Auto")
* Counts mentions of each game
* Stores results in PostgreSQL
* Tracks unknown terms for discovering new games
* Tracks data over time using timestamps
* Designed to run automatically (Task Scheduler)

---

## Data Pipeline

1. Extract – Fetch trending gaming videos from YouTube API
2. Transform – Clean titles and match game names using database aliases
3. Load – Store results in PostgreSQL database

---

## Example Output

```
Roblox: 4
Minecraft: 2
Call of Duty: 2
Among Us: 1
```

---

## Database Output

The processed data is stored in PostgreSQL across multiple tables:

### trending_games

Stores matched game results per run:

| game_name    | mentions | collected_at     |
| ------------ | -------- | ---------------- |
| Roblox       | 4        | 2026-04-27 10:44 |
| Minecraft    | 2        | 2026-04-27 10:44 |
| Call of Duty | 2        | 2026-04-27 10:44 |

---

### games

Stores official game names.

### game_aliases

Maps aliases to real games.

Examples:

* "cod", "warzone" → Call of Duty
* "gta" → Grand Theft Auto
* "impostor" → Among Us

---

### unknown_terms

Stores words the system does not recognize.

Used to:

* Discover new games
* Improve matching accuracy
* Build a feedback loop

---

## Tech Stack

* Python
* YouTube Data API
* PostgreSQL
* psycopg2
* regex

---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure your API key and database connection:

```python
API_KEY = "your_api_key"
DB_CONFIG = {
    "host": "localhost",
    "database": "your_db",
    "user": "your_user",
    "password": "your_password"
}
```

3. Run the script:

```bash
python youtube_trends_to_db.py
```

---

## Automation

This project can be automated using Windows Task Scheduler:

* Runs daily or multiple times per day
* Executes the Python script automatically
* Continuously collects trend data

---

## Game Matching System

The project uses a **database-driven game and alias system** instead of hardcoded values.

Process:

* Titles are cleaned and normalized
* Words and phrases are matched against known aliases
* Matches are grouped under official game names
* Results are stored and tracked

Unknown terms are stored separately and reviewed to improve the system over time.

---

## Data Design

The database stores **historical data**, not just the latest results.

Each run inserts new rows with timestamps (`collected_at`), allowing:

* Trend tracking over time
* Historical comparisons
* Aggregation and analysis

---

## Future Improvements

* Azure cloud backup and failover
* Trend comparison across time windows
* AI-powered query system ("What’s trending now?")
* Automated game discovery from unknown terms
* Dashboard for visualization

---

## Key Takeaway

This project demonstrates a complete data pipeline:

* API integration
* Data cleaning and transformation
* Relational database design
* Automation and scheduling
* Feedback-based system improvement

It is designed to evolve into a scalable data and AI-driven analytics system.
