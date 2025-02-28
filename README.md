# AirsoftTraderScraper



This is an open source project to bring Discord intergration to Airsoft trader, one of new zealands best markets for airsoft replicas


requirements can be found in requirements.txt


How it works:

program broken up into 2 different parts:

first part handles all the RSS feed calls and requests, and then puts the title, and description of the listing in an Array which is then pasted into newlistings.txt

this is then compared to prevoius listings to ensure no duplicates, and then any "new" listings are returned but the airsofttrader.get_new_listings function. which currently returns 2 parts, first being a string of data, ineffeicent currently but works, and then an array of Urls for the images.


this is then handled by the second part (BotCode.py)

this handles discord connection, then will check ~ 5 mins for new listings, if it finds them itll slowly send them to the channel (you will need to configure this)

if a listing does not happen in ~ 2 hours, the program will post a meassage in the chat saying something untill it gets a new listing.

# things to note
all txt files are optional to download, when you first delopy this bot I recomend deleteing them, that way on your first go you will get outputs into your discord. 


# known issues:

currently the embed.thumbnail(url="") is not workig and isnt correctly embeding images in

the process of checking if a listing has already been posted is ineffeicnt, on the website there are ID's for the listings which I should be using. 




# how to run:

make sure you goto discord dashboard and make your API 

generate a token (it isnt made upon creation you need to do this seperately)

put the token in the Var in BotCode.py

go into discord and turn on devloper settings, right click the channel you want your bot to post in and past into the Channel Var on line(24)

once youve done that all you need to do is install the requirments, and run the BotCode.py file, and itll do the rest.
