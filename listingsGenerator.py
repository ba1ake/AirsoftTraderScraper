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
    try:
        file = open(filename, "w")
        file.write(content) #content should be the full string ready to appened into datafile
        file.close
        return True
    except:
        return False
    

def read_from_file(filename): #reads the content from the file
    file = open(filename, "r")
    file_contents_array = []
    file_contents = file.readlines()
    for line in file_contents:
        parts = line.split(",") #splits the line into parts
        title, description = parts[0], parts[1] #assigns the parts to variables
        file_contents_array.append([title, description]) #appends the parts to the array

    return file_contents_array

#removes tags that arent plain text

def replace_special_tag(text):
    special_tags = ["&#8217;", "&amp;", "\n", "\t", "\r", "<p>", "</p>", "<br>", "</br>", "<br />"]  # all the tags that end up in the RSS feed
    replacements = ["'", "&", "", "", "", "", "", "", "", "", ""]  # replacements for special tags needs to match sister array special_tags
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
    listings = [] # 0 is title and 1 is description
    for item in items:
        title = item.find("title").text
        description = replace_special_tag(item.find("content:encoded").text)
        listings.append([title, description])

    return listings


#generates all the listings and will output into a text file to be read by the main program

def generate_listings_all(url): 
    rss = fetch_rss(url)
    sorted_listings = parse_rss_feed(rss) #compiles the listings into a list of lists
    complete_listings = [] #list to be written to the file
    for item in sorted_listings: #prints the listings
        title = item[0]
        description = item[1]
        complete_listings.append([title, description])
        print(title)
        print("\n\n\n")
        print(description)
    write_to_file(str(complete_listings), "newlistings.txt") #writes the listings to a file
    return(complete_listings)
    
#def check_new_listings():


def check_new_listings(current_listing_item, old_listings):
    time.sleep(3)
    for old_listing_item in old_listings:
        if current_listing_item == old_listing_item[0]:
            print("duplicate listing found")
            return False
    #print("new listing found")  
    print(current_listing_item)  
    return True

    
    


 

### Main Program: ### testig purposes to be removed in final realease
current_listings = generate_listings_all(url) #creates the current listings as an array
old_listings = read_from_file("oldlistings.txt") 

#print(current_listings)




