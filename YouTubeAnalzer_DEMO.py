import os
import re
from collections import Counter

import psycopg2
from googleapiclient.discovery import build
from dotenv import load_dotenv

from game_library import GAME_LIBRARY

# Load environment variables from .env file
load_dotenv()

# =========================
# CONFIG
# =========================

# Pull API key and DB credentials from environment variables
API_KEY = os.getenv("YOUTUBE_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# Initialize YouTube API client
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)


# =========================
# HELPERS
# =========================

def clean_text(text):
    """
    Normalize text for easier matching:
    - lowercase everything
    - remove punctuation
    - remove extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_gaming_titles():
    """
    Fetch top trending gaming videos from YouTube (US region).
    Category 20 = Gaming
    Returns a list of video titles.
    """
    request = YOUTUBE.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode="US",
        videoCategoryId="20",
        maxResults=25
    )

    response = request.execute()

    titles = []
    for item in response.get("items", []):
        title = item["snippet"]["title"]
        titles.append(title)

    return titles


def match_games(video_titles, game_library):
    """
    Match known game names against video titles.

    Strategy:
    - Clean both titles and game names
    - Check if game name appears in title
    - Count occurrences

    Returns a Counter of matched games.
    """
    matches = Counter()

    # Pre-clean game library for faster comparisons
    cleaned_library = [(game, clean_text(game)) for game in game_library]

    for title in video_titles:
        cleaned_title = clean_text(title)

        for original_game, cleaned_game in cleaned_library:
            if cleaned_game in cleaned_title:
                matches[original_game] += 1

    return matches


def save_to_db(game_matches):
    """
    Save matched game counts into PostgreSQL.

    Each game + count is inserted as a row.
    """
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for game, count in game_matches.items():
            cursor.execute(
                """
                INSERT INTO trending_games (game_name, mentions)
                VALUES (%s, %s)
                """,
                (game, count)
            )

        conn.commit()
        print("Data saved to PostgreSQL successfully!")

    except Exception as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def main():
    """
    Main pipeline flow:
    1. Fetch YouTube titles
    2. Match games from custom library
    3. Print results
    4. Store results in database
    """
    try:
        video_titles = fetch_gaming_titles()

        print("\nYouTube Gaming Titles:")
        for title in video_titles:
            print(f"- {title}")

        game_matches = match_games(video_titles, GAME_LIBRARY)

        print("\nMatched Games:")
        if game_matches:
            for game, count in game_matches.most_common(25):
                print(f"{game}: {count}")
        else:
            print("No matches found.")

        save_to_db(game_matches)

    except Exception as e:
        print(f"Script error: {e}")


if __name__ == "__main__":
    main()
