import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

url = "https://karjalainen.fi/"
response = requests.get(url)

if response.status_code == 200:
    print("Website fetched successfully!")
    html_content = response.text
else:
    print("Failed to fetch website:", response.status_code)
soup = BeautifulSoup(html_content, "html.parser")
images = soup.find_all("img")  # Finds all <img> tags

print(f"Found {len(images)} images!")
image_urls = []

for img in images:
    src = img.get("src")
    if src:
        if src.startswith("http"):
            image_urls.append(src)
        else:
            # Convert relative URLs to absolute
            from urllib.parse import urljoin

            image_urls.append(urljoin(url, src))

image_urls_set = set(image_urls)  # Removes duplicates automatically

folder_name = "downloaded_images"
os.makedirs(folder_name, exist_ok=True)

for i, img_url in enumerate(tqdm(image_urls_set, desc="Downloading images")):
    try:
        img_data = requests.get(img_url).content
        # Use the original filename if possible
        filename = os.path.basename(img_url.split("?")[0])  # Removes query strings
        if not filename:
            filename = f"image_{i+1}.jpg"
        file_path = os.path.join(folder_name, filename)

        # Skip if file already exists
        if os.path.exists(file_path):
            continue

        with open(file_path, "wb") as f:
            f.write(img_data)
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
