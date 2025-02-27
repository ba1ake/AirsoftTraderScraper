import bs4 , re, requests
import time 

"""
### TO DO LIST: ###

out put data into text file,
use this text file to determine if there are any new listings



"""


### Functions:


# RSS feed URL
url = "https://airsofttrader.co.nz/feed/?post_type=ad_listing"




def load_files():

    newlistings = open("newlistings.txt", "w")
    oldlistings = open("oldlistings.txt", "w")
    return newlistings, oldlistings


def write_to_file(content, filename): #writes the content to the file

    file = open(filename, "w", encoding="utf-8") #opens the file in write mode
    file.write(str(content)) #content should be the full string ready to appened into datafile
    file.close()
    #print(content)
    return True

def append_to_file(content, filename): #appends the content to the file

    file = open(filename, "a", encoding="utf-8") #opens the file in append mode
    file.write(str(content)) #content should be the full string ready to appened into datafile
    file.close()
    return True

def read_from_file(filename): #reads the content from the file

    file = open(filename, "r")
    file_contents_array = []
    file_contents = file.readlines()

    for line in file_contents:
        parts = line.split(",") #splits the line into parts
        #print(parts)
        title, description = parts[0], parts[1] #assigns the parts to variables
        file_contents_array.append([title, description]) #appends the parts to the array

    if len(file_contents_array) == 0:
        return False #means when compared itll be seen as new
    file.close()
    return file_contents_array

#removes tags that arent plain text

def replace_special_tag(text):
    special_tags = ["&#8217;", "&amp;", "\n", "\t", "\r", "<p>", "</p>", "<br>", "</br>", "<br />","\x84"]  # all the tags that end up in the RSS feed
    replacements = ["'", "&", "", "", "", "", "", "", "", "", "",""]  # replacements for special tags needs to match sister array special_tags
    cleaned_text = text  
    for tag, replacement in zip(special_tags, replacements):
        cleaned_text = re.sub(tag, replacement, cleaned_text)
    
    #print(cleaned_text) #debugging
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
    listings = []  # 0 is title and 1 is description
    links = []

    for item in items:
        link = item.find("link").text
        title = item.find("title").text
        description = replace_special_tag(item.find("content:encoded").text)
        listings.append([title, description])
        links.append(link)  # Append the URL to the links list
        #print(links)
        
    return listings, links


#generates all the listings and will output into a text file to be read by the main program

def generate_listings_all(url): 
    rss = fetch_rss(url)
    listing_urls = []
    sorted_listings, listing_urls = parse_rss_feed(rss) #compiles the listings into a list of lists
    #print(listing_urls)
    complete_listings = [] #list to be written to the file
    plain_text = ""


    for item in sorted_listings: #prints the listings
        title = item[0]
        description = item[1]
        complete_listings.append([title, description])
        plain_text += str(complete_listings[len(complete_listings)-1]) + "\n"
    write_to_file(plain_text, "newlistings.txt") #writes the listings to a file
    #print(plain_text)
    return(complete_listings, listing_urls) #returns the listings and the urls
    
#def check_new_listings():



#this needs to remove the ['' from the string for "current_listing_item"" 

def check_new_listings(current_listing_item, old_listings): 
    #time.sleep(1)
    for old_listing_item in old_listings:

        old_listing_item_str = str(old_listing_item[0])
        old_listing_item_str = old_listing_item_str[2:-1]

        if current_listing_item == old_listing_item_str:
            print("duplicate listing found")
            return False
            
    #print("new listing found")  
    #print(current_listing_item)  
    return True

    

def get_listing_image(url):
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        # Look for the 'og:image' meta tag
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image['content']:
            return og_image['content']

        # If 'og:image' is not found, look for the largest image on the page
        images = soup.find_all('img')
        if not images:
            return "https://airsofttrader.co.nz/wp-content/uploads/2024/02/AS2024BannerOD.png"

        main_image_url = None
        max_area = 0
        for img in images:
            try:
                # Get image dimensions
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
        return 


def get_new_listings():
    used_urls = []
    all_urls = []
    current_listings, all_urls = generate_listings_all(url) #creates the current listings as an array
    old_listings = read_from_file("oldlistings.txt") 

    if old_listings == False: # if not lissings are found in the old listings file
        write_to_file('["void","void"]'+ "\n", "oldlistings.txt") #creates a void listing to be used as a base so that the script doesnt throw an error on line 106
        print("empty file")
        old_listings = read_from_file("oldlistings.txt")

    new_listings = ""
    x = -1
    for item in current_listings:
        x += 1
        #print(used_urls)
        if check_new_listings(item[0], old_listings):
            new_listings += str(item) + "\n"
            used_urls.append(all_urls[x])
            print(all_urls[x])
    if len(current_listings) == 0:
        return False, False #needs to return 2 as other end is expecting 2 values


    x+=1
    #print(new_listings)
    append_to_file(new_listings, "oldlistings.txt") #updates the old listings file with the new listings DO LAST
    return (str(new_listings), used_urls) #returns the new listings as a string and urls as a array becuase I am a terrible programmer


#get_new_listings() #used for debugging