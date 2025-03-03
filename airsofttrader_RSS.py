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
        file.write(str(content)+ '["void","void"]')
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
    special_tags = ["&#8217;", "&amp;", "\n", "\t", "\r", "<p>", "</p>", "<br>", "</br>", "<br />""<a/>","\x84"]
    replacements = ["'", "&", "", "", "", "", "", "", "", "", "", "",""]
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
    return complete_listings, listing_urls

def check_new_listings(current_listing_item, old_listings):
    
    for old_listing_item in old_listings:
        old_listing_item_str = str(old_listing_item[0])
        old_listing_item_str = old_listing_item_str[2:-1]
        if current_listing_item == old_listing_item_str:
            print("duplicate listing found")
            return False
    return True

def get_listing_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image['content']:
            return og_image['content']
        images = soup.find_all('img')
        if not images:
            return "https://airsofttrader.co.nz/wp-content/uploads/2024/02/AS2024BannerOD.png"
        main_image_url = None
        max_area = 0
        for img in images:
            try:
                width = int(img.get('width', 0))
                height = int(img.get('height', 0))
                area = width * height
                if area > max_area:
                    max_area = area
                    main_image_url = img['src']
            except (ValueError, TypeError):
                continue
        return main_image_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def get_new_listings():
    used_urls = []
    all_urls = []
    current_listings, all_urls = generate_listings_all(url)
    old_listings = read_from_file("oldlistings.txt")
    print("listings checked correctly, there are ", current_listings, " current listings")
    if old_listings == False:
        write_to_file('["void","void"]' + "\n", "oldlistings.txt")
        print("empty file")
        old_listings = read_from_file("oldlistings.txt")

    new_listings = ""
    x = -1
    for item in current_listings:
        x += 1
        if check_new_listings(item[0], old_listings):
            new_listings += str(item) + "\n"
            used_urls.append(all_urls[x])
            print(all_urls[x])
    if len(current_listings) == 0:
        return False, False

    append_to_file(new_listings, "oldlistings.txt")
    return str(new_listings), used_urls

# Uncomment this line to debug
get_new_listings()
