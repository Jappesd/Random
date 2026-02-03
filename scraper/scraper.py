import requests
import os
from datetime import date
from tqdm import tqdm

# -----------------------------
# Setup folders and files
# -----------------------------
os.makedirs("memes", exist_ok=True)

titles_file_path = "memes/meme_titles.txt"
url_file_path = "memes/downloaded_urls.txt"

# Ensure files exist
open(titles_file_path, "a", encoding="utf-8").close()
open(url_file_path, "a").close()

# Load previously downloaded URLs
with open(url_file_path, "r") as f:
    downloaded_urls = set(line.strip() for line in f)

# -----------------------------
# Scraper settings
# -----------------------------
url = "https://www.reddit.com/r/memes/top/.json?limit=50&t=day"
headers = {"User-Agent": "MemeScraper/0.1"}

response = requests.get(url, headers=headers)
data = response.json()

today = date.today()  # Add date to titles

# -----------------------------
# Start scraping
# -----------------------------
with open(titles_file_path, "a", encoding="utf-8") as title_file:
    for i, post in enumerate(tqdm(data["data"]["children"], desc="Downloading memes")):
        post_data = post["data"]
        if post_data.get("post_hint") != "image":
            continue  # Skip non-image posts

        meme_url = post_data["url"]
        if meme_url in downloaded_urls:
            continue  # Skip duplicates
        downloaded_urls.add(meme_url)

        try:
            # Download image
            img_data = requests.get(meme_url).content
            file_path = f"memes/meme_{i+1}_{(today)}.jpg"
            with open(file_path, "wb") as f:
                f.write(img_data)

            # Save title with date
            title_file.write(f"{file_path} - {post_data['title']}\n")

            # Update URL tracker file
            with open(url_file_path, "a") as f:
                f.write(meme_url + "\n")

        except Exception as e:
            print(f"Failed to download {meme_url}: {e}")

print("Scraping complete!")
