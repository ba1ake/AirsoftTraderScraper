import bs4
import requests
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning) #using HTML parser to parse XML so this removes error warning from bs4



#rss feed url

url = "https://airsofttrader.co.nz/feed/?post_type=ad_listing"



#fetchs the rss feed from chosen URL and returns the content using HTML parser
def fetch_rss(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser') #need to change to XML
    return soup

def parse_rss_feed(content): #parses the rss feed and returns the title and description of each item provide no form of cleaning the data
    items = content.find_all('item')
    listings = []
    for item in items:
        title = item.find('title').text
        description = bs4.BeautifulSoup(item.find('description').text, 'html.parser').get_text()
        listings.append({'title': title, 'description': description})

    return listings


rss = fetch_rss(url)
sorted_listings = parse_rss_feed(rss)

print(sorted_listings[1])