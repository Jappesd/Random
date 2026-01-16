import requests
from bs4 import BeautifulSoup as bs

# url to scrape
url = "https://quotes.toscrape.com"
# send a get request
response = requests.get(url)
# check if request was successful
if response.status_code == 200:
    # parse html content
    soup = bs(response.text, "html.parser")
    # find all quote blocks
    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        print(f"{text}-{author}")
else:
    print(f"Failed to retrieve page. status code: {response.status_code}")
