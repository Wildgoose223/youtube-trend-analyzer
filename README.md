# YouTube Trend Analyzer

A Python-based data pipeline that extracts trending gaming videos from YouTube, processes the data, identifies popular games, and stores the results in a PostgreSQL database for tracking trends over time.

---

## Overview

This project pulls trending gaming videos using the YouTube Data API, cleans and analyzes titles, matches them against a custom game library, and stores structured results in a PostgreSQL database. Each run captures a snapshot of trending data.

---

## Features

- Pulls trending gaming videos (YouTube Category 20)
- Cleans titles using regex
- Matches game titles using a custom game library with aliases
- Counts mentions of each game
- Stores results in PostgreSQL
- Tracks data over time using timestamps
- Designed to run automatically twice daily

---

## Data Pipeline

1. Extract – Fetch trending gaming videos from YouTube API  
2. Transform – Clean titles and match game names  
3. Load – Store results in PostgreSQL database  

---

## Example Output

```
Roblox: 3
Minecraft: 2
Genshin Impact: 1
GTA: 1
```

---

## Database Output

The processed data is stored in a PostgreSQL table called `trending_games`.

Each run inserts a new snapshot of data:

| game_name       | mentions | collected_at          |
|----------------|----------|----------------------|
| Roblox         | 3        | 2026-04-24 12:32     |
| Minecraft      | 2        | 2026-04-24 12:32     |
| Genshin Impact | 1        | 2026-04-24 12:32     |
| GTA            | 1        | 2026-04-24 12:32     |

![Database Output](images/database_output.png)

---

## Tech Stack

- Python
- YouTube Data API
- PostgreSQL
- psycopg2
- pandas
- regex

---

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in your project folder:
```env
YOUTUBE_API_KEY=your_api_key_here
```

3. Run the script:
```bash
python youtube_trends_to_db.py
```

---

## Automation

This project can be automated using Windows Task Scheduler:

- Runs twice daily (morning and evening)
- Executes the Python script automatically
- Continuously collects trend data

---

## Game Matching System

The project uses a custom `game_library.py` file containing known game titles and aliases.

Examples:
- "Call of Duty" matches "cod", "warzone"
- "Counter Strike" matches "cs2", "csgo"
- "League of Legends" matches "lol"

Process:
- Titles are cleaned and normalized
- Keywords are matched against known aliases
- Mentions are counted and stored

This converts unstructured YouTube titles into structured trend data.

---

## Data Design

The database stores historical data, not just the latest results.

Each run inserts new rows with a timestamp (`collected_at`), allowing:
- Trend tracking over time
- Historical comparisons
- Aggregation and analysis

---

## Future Improvements

- Expand game detection dynamically (API or database)
- Improve matching using NLP techniques
- Store raw video titles separately
- Build dashboard for visualization
- Deploy to cloud (Azure / VM)

---

## Key Takeaway

This project demonstrates a complete data pipeline:

- API integration  
- Data cleaning and transformation  
- Database storage  
- Automation  
- Trend tracking over time



