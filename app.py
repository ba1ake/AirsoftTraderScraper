import beautifulsoup4 as bs4
import requests








url = "https://airsofttrader.co.nz/nz-airsoft-sales/"
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())