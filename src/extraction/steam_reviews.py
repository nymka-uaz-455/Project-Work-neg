"""Collect Steam reviews for one game and load them into the staging layer.

Usage (from the project root, with the virtual environment active):
    python src/extraction/steam_reviews.py --app-id 730 --game "Counter-Strike 2" --max-reviews 1000

Steam app ids:  Counter-Strike 2 = 730 | Cyberpunk 2077 = 1091500 | GTA V = 271590
"""
import argparse
import os
import sys
import time

import pyodbc
import requests
from dotenv import load_dotenv

API_URL = "https://store.steampowered.com/appreviews/{app_id}"
PAGE_SIZE = 100          # Steam's maximum per request
PAUSE_SECONDS = 1.0      # be polite to the public endpoint

INSERT_SQL = """
INSERT INTO stg.steam_review (
    load_id, app_id, game_name, recommendation_id,
    author_steamid, author_num_games_owned, author_num_reviews,
    author_playtime_forever, author_playtime_at_review,
    language, review_text, timestamp_created, timestamp_updated,
    voted_up, votes_up, votes_funny, weighted_vote_score, comment_count,
    steam_purchase, received_for_free, written_during_early_access
) VALUES (?,?,?,?, ?,?,?, ?,?, ?,?,?,?, ?,?,?,?,?, ?,?,?)
"""


def to_bit(value):
    return None if value is None else int(bool(value))


def to_row(load_id, app_id, game_name, r):
    a = r.get("author", {})
    return (
        load_id, app_id, game_name, str(r.get("recommendationid")),
        a.get("steamid"), a.get("num_games_owned"), a.get("num_reviews"),
        a.get("playtime_forever"), a.get("playtime_at_review"),
        r.get("language"), r.get("review"),
        r.get("timestamp_created"), r.get("timestamp_updated"),
        to_bit(r.get("voted_up")), r.get("votes_up"), r.get("votes_funny"),
        r.get("weighted_vote_score"), r.get("comment_count"),
        to_bit(r.get("steam_purchase")), to_bit(r.get("received_for_free")),
        to_bit(r.get("written_during_early_access")),
    )


def fetch_page(app_id, cursor):
    params = {
        "json": 1,
        "filter": "recent",       # newest first -> good for incremental loading later
        "language": "all",
        "purchase_type": "all",
        "num_per_page": PAGE_SIZE,
        "cursor": cursor,
    }
    resp = requests.get(API_URL.format(app_id=app_id), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--app-id", type=int, required=True)
    parser.add_argument("--game", required=True, help="Game name, e.g. 'Counter-Strike 2'")
    parser.add_argument("--max-reviews", type=int, default=1000)
    args = parser.parse_args()

    load_dotenv()
    conn_str = os.getenv("DB_CONNECTION_STRING")
    if not conn_str:
        sys.exit("DB_CONNECTION_STRING is not set. Copy .env.example to .env first.")

    conn = pyodbc.connect(conn_str)
    cur = conn.cursor()
    cur.fast_executemany = True

    cur.execute(
        "INSERT INTO stg.load_log (source_name, game_name, source_game_id) "
        "OUTPUT INSERTED.load_id VALUES (?,?,?)",
        "steam", args.game, str(args.app_id),
    )
    load_id = cur.fetchone()[0]
    conn.commit()
    print(f"Load {load_id} started for {args.game} (app {args.app_id})")

    total, cursor_token, seen_cursors = 0, "*", set()
    try:
        while total < args.max_reviews:
            data = fetch_page(args.app_id, cursor_token)
            reviews = data.get("reviews", [])
            if not data.get("success") or not reviews:
                break

            rows = [to_row(load_id, args.app_id, args.game, r) for r in reviews]
            rows = rows[: args.max_reviews - total]
            cur.executemany(INSERT_SQL, rows)
            conn.commit()
            total += len(rows)
            print(f"  loaded {total} reviews")

            cursor_token = data.get("cursor")
            if not cursor_token or cursor_token in seen_cursors:
                break
            seen_cursors.add(cursor_token)
            time.sleep(PAUSE_SECONDS)

        cur.execute(
            "UPDATE stg.load_log SET finished_at = SYSUTCDATETIME(), rows_loaded = ?, status = 'success' "
            "WHERE load_id = ?", total, load_id,
        )
        conn.commit()
        print(f"Done. {total} reviews loaded (load_id {load_id}).")
    except Exception as exc:
        conn.rollback()
        cur.execute(
            "UPDATE stg.load_log SET finished_at = SYSUTCDATETIME(), rows_loaded = ?, status = 'failed' "
            "WHERE load_id = ?", total, load_id,
        )
        conn.commit()
        print(f"FAILED after {total} reviews: {exc}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
