import feedparser
import requests
import bs4
import re

# RSS feed URL
url = "https://airsofttrader.co.nz/feed/?post_type=ad_listing"

def write_to_file(content, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(content))
    return True

def append_to_file(content, filename):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(str(content))
    return True

def read_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        file_contents_array = []
        file_contents = file.readlines()
        for line in file_contents:
            parts = line.split(",")
            title, description = parts[0], parts[1]
            file_contents_array.append([title, description])
    if len(file_contents_array) == 0:
        return False
    return file_contents_array

def replace_special_tag(text):
    special_tags = ["&#8217;", "&amp;", "\n", "\t", "\r", "<p>", "</p>", "<br>", "</br>", "<br />","\x84"]
    replacements = ["'", "&", "", "", "", "", "", "", "", "", "", ""]
    cleaned_text = text
    for tag, replacement in zip(special_tags, replacements):
        cleaned_text = re.sub(tag, replacement, cleaned_text)
    return cleaned_text

def fetch_rss(url):
    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            raise Exception(feed.bozo_exception)
        return feed
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def parse_rss_feed(feed):
    listings = []
    links = []
    for entry in feed.entries:
        link = entry.link
        title = entry.title
        description = replace_special_tag(entry.description)
        listings.append([title, description])
        links.append(link)
    return listings, links

def generate_listings_all(url):
    rss = fetch_rss(url)
    listing_urls = []
    sorted_listings, listing_urls = parse_rss_feed(rss)
    complete_listings = []
    plain_text = ""
    for item in sorted_listings:
        title = item[0]
        description = item[1]
        complete_listings.append([title, description])
        plain_text += str(complete_listings[len(complete_listings)-1]) + "\n"
    write_to_file(plain_text, "newlistings.txt")
    return complete