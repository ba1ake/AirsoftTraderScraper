import bs4 , re
import requests
from lxml import etree
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


"""
### TO DO LIST: ###

out put data into text file,
use this text file to determine if there are any new listings



"""


### Functions:


# RSS feed URL
url = "https://airsofttrader.co.nz/feed/?post_type=ad_listing"

#seperate function to replace the tag used as a place holder for " ' "

def replace_special_tag(text):
    special_tags = ["&#8217;", "&amp;", "\n", "\t", "\r", "<p>", "</p>", "<br>", "</br>", "<br />"]  # all the tags that end up in the RSS feed
    replacements = ["'", "&", "", "", "", "", "", "", "", "", ""]  # replacements for special tags needs to match sister array special_tags

    cleaned_text = text  
    for tag, replacement in zip(special_tags, replacements):
        cleaned_text = re.sub(tag, replacement, cleaned_text)
    
    print(cleaned_text)
    return cleaned_text


# Fetches the RSS feed from chosen URL and returns the content using XML parser
def fetch_rss(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "xml") # Changed parser to XML
    return soup

#cleans up HTML tags in the description, needs to be intergarted into new replace_special_tag function
#def cleanup(text): 
    for char in ["\n", "\t", "\r", "<p>", "</p>", "<br>", "</br>", "<br>"]: #removes HTML tags and newlines from string
        text = text.replace(char, '')
    return replace_special_tag(text)



# Parses the RSS feed and returns the title and description of each item into an array
def parse_rss_feed(content):
    items = content.find_all("item")
    listings = [] # 0 is title and 1 is description
    for item in items:
        title = item.find("title").text
        description = replace_special_tag(item.find("content:encoded").text)
        listings.append([title, description])

    return listings


#generates all the listings and will output into a text file to be read by the main program

def generate_listings_all(url): 
    rss = fetch_rss(url)
    sorted_listings = parse_rss_feed(rss) #compliles the listings into a list of lists

    for item in sorted_listings: #prints the listings
        print(item)
        print("\n\n\n")
    
