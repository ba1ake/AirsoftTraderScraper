# AirsoftTraderScraper
A scraper designed to scrap through the New Zealand Airsoft trader website and Gather results, 


scraper is desigend, or will be, to sraper the webpage and dump new listings into a text file, 

currently uses an old project of mine which uses the HTML praser rather than a needed XML praser


I want to intergate in discord bot 


will use text files in order to only post new listings up and later down the track will enable checking price changes




"""
        for title, description, url in zip(titles, descriptions, urls):
            print("attemptable embed")
            print(title, description)
            await asyncio.sleep(5)  # Non-blocking sleep

            embed = discord.Embed(title=title, description=description, color=0x1abc9c)
            embed.set_author(name="New Airsoft Listing", icon_url="https://example.com/icon.png")
            if url:
                embed.url = url  # Make the title a clickable link
            embed.set_footer(text="Powered by AirsoftTraderBot")

            await channel.send(embed=embed)

            # Optionally add an image if available

            await asyncio.sleep(5)  # 3600 seconds = 1 hour
        """

"""
            if len(parts) >= 3:
                # Append title, description, and URL to their respective arrays
                titles.append(parts[0].strip())
                descriptions.append(parts[1].strip())
                urls.append(parts[2].strip())
            elif len(parts) == 2:
                titles.append(parts[0].strip())
                descriptions.append(parts[1].strip())
                #urls.append(None)  # No URL provided
            else:
                continue  # Skip if data is insufficient
            print(item)
            """

        