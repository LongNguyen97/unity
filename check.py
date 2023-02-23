import asyncio
import logging

import requests
from retry import retry

BAD_WORDS_FILE = "bad_words.txt"

# Define your Zendesk API credentials and endpoint here
ZENDESK_API_EMAIL = "your-email"
ZENDESK_API_TOKEN = "your-token"
ZENDESK_API_ENDPOINT = "https://your-domain.zendesk.com/api/v2"

# Define the email address to receive notifications for manually approved posts
NOTIFICATION_EMAIL = "notification-email"

# Load bad words from file
with open(BAD_WORDS_FILE, "r") as f:
    BAD_WORDS = {word.strip().lower() for word in f.readlines()}

# Configure logging
logging.basicConfig(filename='zendesk.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@retry(delay=2, tries=5)
async def get_all_posts():
    try:
        headers = {"Content-Type": "application/json"}
        url = f"{ZENDESK_API_ENDPOINT}/community/posts.json?sort_by=created_at&sort_order=desc"
        response = requests.get(url, auth=(ZENDESK_API_EMAIL, ZENDESK_API_TOKEN), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error getting posts: {e}")
        raise

@retry(delay=2, tries=5)
async def approve_post(post_id):
    try:
        headers = {"Content-Type": "application/json"}
        url = f"{ZENDESK_API_ENDPOINT}/community/posts/{post_id}/approve.json"
        response = requests.put(url, auth=(ZENDESK_API_EMAIL, ZENDESK_API_TOKEN), headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error approving post {post_id}: {e}")
        raise


def is_valid_post(post):
    """
    Check if a given post is valid based on its content and sentiment analysis.

    Returns True if the post is valid and should be automatically approved, False otherwise.
    """
    # Load bad words and payment-related words from file
    with open('bad_words.txt', 'r') as f:
        bad_words = [line.strip() for line in f.readlines()]

    # Check for bad words in post content
    content = post['content']
    for word in bad_words:
        if word in content:
            logging.warning(f"Post {post['id']} contains bad word '{word}': {content}")
            return False

    # Perform sentiment analysis on post content
    blob = TextBlob(content)
    sentiment = blob.sentiment.polarity
    if sentiment < 0:
        logging.warning(f"Post {post['id']} has negative sentiment: {content}")
        return False
    return True

async def process_post(post):
    is_bad = is_valid_post(post)
    # otherwise, approve the post automatically
    if not is_bad:
        await approve_post(post["id"])
        logging.info(f"Post {post['id']} has been approved.")

async def main():
    try:
        posts = await get_all_posts()
        tasks = [asyncio.ensure_future(process_post(post)) for post in posts["posts"]]
        await asyncio.gather(*tasks)
        logging.info(f"{len(posts['posts'])} posts processed.")
    except Exception as e:
        logging.error(f"Error processing posts: {e}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
