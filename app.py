import bs4
import requests
from lxml import etree
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)





### Functions:


# RSS feed URL
url = "https://airsofttrader.co.nz/feed/?post_type=ad_listing"

# Fetches the RSS feed from chosen URL and returns the content using XML parser
def fetch_rss(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "xml") # Changed parser to XML
    return soup

def cleanup(text):
    for char in ["\n", "\t", "\r", "<p>", "</p>", "<br>", "</br>", "<br />"]: #removes HTML tags and newlines from string
        text = text.replace(char, '')
    return text

# Parses the RSS feed and returns the title and description of each item into an array
def parse_rss_feed(content):
    items = content.find_all("item")
    listings = [] # 0 is title and 1 is description
    for item in items:
        title = item.find("title").text
        description = cleanup(item.find("content:encoded").text)
        listings.append([title, description]) #appends as single layer array

    return listings




### Main code


rss = fetch_rss(url)
sorted_listings = parse_rss_feed(rss)





for item in sorted_listings:
    print(item)
    print("\n\n\n")
