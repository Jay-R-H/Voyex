import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://ai.meta.com/blog/?page=1"
r = requests.get(URL)

dates = []
links = []
titles = []

soup = BeautifulSoup(r.content, 'html5lib')

with open("ai_google.html", 'w', encoding="utf-8") as f:
    f.write(str(soup))

div_blocks = soup.find_all('div', class_='_amdc')

for div_block in div_blocks:
    a_tag = div_block.find('a')

    link = a_tag.get('href')
    links.append(link)

    title = a_tag.get('aria-label')
    title = title.split("Read ")[1]
    titles.append(title)

    date_div = div_block.find_all('div', class_='_amdj')
    date = date_div[-1].text.strip()
    dates.append(date)

data = {
    'Title':titles,
    'Link':links,
    'Date':dates
}

df = pd.DataFrame(data)

df.to_csv("Meta_ai_latest.csv", index=False)