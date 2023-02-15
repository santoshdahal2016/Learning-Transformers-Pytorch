import requests
from bs4 import BeautifulSoup

url = 'https://www.traveldrafts.com/what-is-nepal-famous-for/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
text = soup.get_text()

if "WPX.net" in text :
    print("no data")
else :
    print(text)

