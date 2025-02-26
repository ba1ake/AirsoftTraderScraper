import bs4
import requests
from lxml import etree
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# RSS feed URL
url = "https://airsofttrader.co.nz/feed/?post_type=ad_listing"

# Fetches the RSS feed from chosen URL and returns the content using XML parser
def fetch_rss(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "xml") # Changed parser to XML
    return soup

# Parses the RSS feed and returns the title and description of each item into an array
def parse_rss_feed(content):
    items = content.find_all("item")
    listings = [] #need to turn into multi layer array
    for item in items:
        title = item.find("title").text
        description = item.find("description").text
        listings.append({"title": title, "description": description}) #appends as single layer array

    return listings

rss = fetch_rss(url)
sorted_listings = parse_rss_feed(rss)

print(sorted_listings[1])
