import praw
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USER_AGENT = os.getenv('REDDIT_USER_AGENT')

OUTPUT_FILE_NAME = "local_stream.txt"

SUBREDDIT_TO_STREAM = "all"

if __name__ == "__main__":
    print("Starting Reddit stream producer...")

    if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
        print("Error: Make sure you have set up your .env file with REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT.")

    else:
        try:
            reddit = praw.Reddit(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                user_agent=USER_AGENT
            )

            subreddit = reddit.subreddit(SUBREDDIT_TO_STREAM)

            print(f"Successfully connected to Reddit. Starting to stream comments from r/{SUBREDDIT_TO_STREAM}...")

            for comment in subreddit.stream.comments(skip_existing=True):
                try:
                    comment_data = {
                        "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(comment.created_utc)),
                        "text": comment.body
                    }

                    with open(OUTPUT_FILE_NAME, "a", encoding="utf-8") as fp:
                        json_string = json.dumps(comment_data).replace("\n", " ")

                        fp.write(json_string + "\n")

                    print(f"Comment received and saved: {comment.body[:60]}...")
                
                except Exception as e:
                    print(f"Error processing comment: {e}")

        except KeyboardInterrupt:
            print("Stream interrupted by user. Shutting down...")

        except Exception as e:
            print(f"Unexpected error occurred: {e}")