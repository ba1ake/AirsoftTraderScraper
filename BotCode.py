import discord
import asyncio
import time
import airsofttrader  # Custom library for this project
from discord import Embed

# Replace this with your actual bot token
TOKEN = "Hidden" 

# Set up bot permissions
intents = discord.Intents.default()
client = discord.Client(intents=intents)
to_quiet = False # this will se==be used to make the bot say something if it has been quiet for a while and will suggests users to post a listing online
time_quiet = 0
# Clears old listings for debugging

with open("outputlog.txt", "w") as file:
    file.write("Machine started at "+ str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


async def check_airsoft_listings(time_quiet=time_quiet):
    """Fetches new airsoft listings and sends them to a Discord channel."""
    await client.wait_until_ready()  # Ensure bot is connected before running the loop
    channel = client.get_channel(1311228804877914163)

    if channel:
        listing_url = []
        listing, listing_url = airsofttrader.get_new_listings()  # Fetch new listings
        if listing:
            items = listing.strip().split("\n")  # Convert data into a list
            print(items[1])

            x = -1
            for item in items:
                x += 1
                parts = item.split(", ")

                # Extract listing details
                embed_title = str(parts[0])[2:-1]

                # Checks if any formatting issues exist
                if parts[1].endswith("']"):
                    embed_description = str(parts[1])[1:-1]
                else:
                    embed_description = str(parts[1])[1:-0]

                embed_description = str(parts[1]) + "'"
                embed_url = str(listing_url[x])
                embed_author_name = "AirsoftTrader"
                embed_author_icon_url = "https://example.com/icon.png"
                embed_footer_text = "Powered by AirsoftTrader"

                # Create and configure the embed message
                embed = discord.Embed(title=embed_title, description=embed_description, color=0x1ABC9C)
                embed.set_author(name=embed_author_name, icon_url=embed_author_icon_url)
                embed.url = embed_url  # Make the title a clickable link
                embed.set_footer(text=embed_footer_text)
                embed.set_thumbnail(url=embed_author_icon_url)

                # Send the embed message to the Discord channel
                airsofttrader.append_to_file("new listing found and posted @ " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), "outputlog.txt")
                await channel.send(embed=embed)
                time_quiet = 0
                time.sleep(60)  # Prevents discord hating us for spam and if multiple listings are found at once release them steedly


            # if the release takes longer than 5 minutes, the bot will wont 5 minutes before checking again
            if len(items) > 5:
                pass
            if len(items) == 0:
                time.sleep(300) #avoids divison by 0 error
            else:
                time.sleep(300 - (len(items) * 5)) # Check listings every 5 minutes if there are more than 5 listings then It will take away the time taken to print the listings from its 5 minute pause
        else:
            print("no listings found")
            to_quiet = True
            time_quiet += 1
            if time_quiet == 12*2: # 12*2 is 2 hours
                await channel.send("The bot has been quiet for a while, consider posting a listing online!")
                airsofttrader.append_to_file("no new listings @ " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + " lets send some ecourgement!","outputlog.txt")
                time_quiet = 0
            airsofttrader.append_to_file("no new listings @ " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"outputlog.txt")

@client.event
async def on_ready():
    """Executes when the bot successfully connects to Discord."""
    print(f"Logged in as {client.user}")
    
    # Uncomment this if you want the bot to send a startup message
    # channel = client.get_channel(1311227735104028695)
    # if channel:
    #     await channel.send("Hello! The bot is now working")

    # Start the background task to check listings periodically
    client.loop.create_task(check_airsoft_listings())


# Run the bot
client.run(TOKEN)
