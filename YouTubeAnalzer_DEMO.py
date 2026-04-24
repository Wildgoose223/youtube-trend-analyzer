import os
import re
from collections import Counter

import psycopg2
from googleapiclient.discovery import build

from game_library import GAME_LIBRARY

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("YOUTUBE_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

YOUTUBE = build("youtube", "v3", developerKey=API_KEY)


# =========================
# HELPERS
# =========================
def clean_text(text):
    """
    Lowercases text and removes most punctuation
    so matching is easier.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_gaming_titles():
    """
    Pull the top US gaming videos from YouTube.
    Gaming category = 20
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
    Match game names from your custom library
    against YouTube video titles.
    """
    matches = Counter()
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