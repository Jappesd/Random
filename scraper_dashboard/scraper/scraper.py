# main scraping logic
import requests
from bs4 import BeautifulSoup

url = "https://reddit.com/"


def fetch_data(url):
    gette = requests.get(url)
    print(gette.text[:1000])
    return gette.text


def parse_data(html):
    soup = BeautifulSoup(html, "html.parser")
    image_tag = soup.find_all("img", id="post-image")
    img_sources = []

    for img in image_tag:
        img_sources.append(img["src"])
    if len(img_sources) > 0:
        print("found")
    else:
        print("not found")
        return
    for i in img_sources:
        print(i)


# return image_url


def save_data(data):
    pass


html = fetch_data(url)
# parse_data(html)
