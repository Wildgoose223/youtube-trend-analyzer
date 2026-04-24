# YouTube Trend Analyzer
Python-based data pipeline using the YouTube Data API to extract, clean, and analyze trending gaming video data.

## Features
- Pulls trending gaming videos from YouTube (Category 20)
- Cleans titles using regex
- Extracts keywords from video titles
- Counts most frequent terms using Python collections
- Prepares data for database storage

## Tech Stack
- Python
- YouTube Data API
- pandas
- requests
- regex

## How to Run

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Add your YouTube API key in the script

3. Run:
```
python youtube_trends_to_db.py
```


##  Future Improvements
- Integrate game title matching (Steam/Wikipedia)
- Store results in PostgreSQL
- Build dashboard for trend visualization

## Interpreting Results

The output represents how often specific games appear in trending YouTube gaming videos.

For example:

Fortnite: 5
Minecraft: 3
Call of Duty: 2

This indicates that Fortnite is currently receiving more attention in trending content compared to the other listed games.

Higher mention counts suggest:
- Increased popularity
- Higher content creation activity
- Strong viewer interest

Lower counts may indicate:
- Niche or declining interest
- Less trending content at that moment

This data can be used to identify emerging trends, track game popularity over time, and support content or business decisions.
