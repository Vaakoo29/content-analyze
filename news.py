import requests
from bs4 import BeautifulSoup

url = 'https://ria.ru/location_Arktika/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

links = []
news = soup.findAll('a', class_="list-item__title color-font-hover-only")
for new in news:
    link = new.get('href')
    links.append(link)

with open("russian_news.txt", 'w', encoding='utf-8') as file:
    for link in links:
        l = requests.get(link)
        soup = BeautifulSoup(l.text, 'lxml')
        for text in soup.findAll('div', class_='article__text'):
            print(text.text)
            file.write(text.text)