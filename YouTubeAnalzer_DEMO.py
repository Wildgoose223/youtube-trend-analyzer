import re
from collections import Counter
import psycopg2
from googleapiclient.discovery import build

# =========================
# CONFIG
# =========================
API_KEY = "INSERT_YOUR_API_HERE"

DB_CONFIG = {
    "host": "YOUR_HOST",
    "database": "YOUR_DB",
    "user": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}

YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

# =========================
# HELPERS
# =========================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_game_library(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.game_name, a.alias
        FROM games g
        JOIN game_aliases a ON g.id = a.game_id;
    """)

    rows = cursor.fetchall()
    cursor.close()

    game_library = {}

    for game_name, alias in rows:
        if game_name not in game_library:
            game_library[game_name] = []

        game_library[game_name].append(alias)

    return game_library


def fetch_gaming_titles():
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
        titles.append(item["snippet"]["title"])

    return titles


def match_games(video_titles, game_library):
    matches = Counter()

    for title in video_titles:
        cleaned_title = clean_text(title)

        for game_name, aliases in game_library.items():
            for alias in aliases:
                if alias in cleaned_title:
                    matches[game_name] += 1
                    break

    return matches


def save_unknown_terms(video_titles, game_library, conn):
    cursor = conn.cursor()

    stop_words = {
        "this", "that", "with", "from", "your", "game", "games",
        "best", "new", "update", "live", "stream", "insane",
        "playing", "official", "trailer", "part", "full",
        "what", "when", "where", "they", "them", "have",
        "just", "like", "more", "most", "into", "over",
        "after", "before", "first", "last", "only", "will",
        "can", "how", "why", "the", "and", "for", "you"
    }

    for title in video_titles:
        cleaned_title = clean_text(title)
        words = cleaned_title.split()

        for word in words:
            if len(word) < 4:
                continue

            if word in stop_words:
                continue

            already_known = False

            for aliases in game_library.values():
                if word in aliases:
                    already_known = True
                    break

            if already_known:
                continue

            cursor.execute(
                """
                INSERT INTO unknown_terms (term, count)
                VALUES (%s, 1)
                ON CONFLICT (term)
                DO UPDATE SET
                    count = unknown_terms.count + 1,
                    last_seen = CURRENT_TIMESTAMP
                """,
                (word,)
            )

    conn.commit()
    cursor.close()
    print("Unknown terms saved successfully!")


def save_to_db(game_matches, conn):
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
    cursor.close()
    print("Data saved to PostgreSQL successfully!")


def main():
    conn = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)

        game_library = load_game_library(conn)

        video_titles = fetch_gaming_titles()

        print("\nYouTube Gaming Titles:")
        for title in video_titles:
            print(f"- {title}")

        game_matches = match_games(video_titles, game_library)

        save_unknown_terms(video_titles, game_library, conn)

        print("\nMatched Games:")
        if game_matches:
            for game, count in game_matches.most_common(25):
                print(f"{game}: {count}")
        else:
            print("No matches found.")

        save_to_db(game_matches, conn)

    except Exception as e:
        print(f"Script error: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
