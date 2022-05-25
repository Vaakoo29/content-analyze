# новые библиотеки: pip install selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import lxml
import requests
import time

# Нужно будет скачать Chrome драйвер: https://chromedriver.chromium.org/home
# Проверь версию Chrome и скачай в соответствие с версией (а то работать не будет)
# Сюда нужно указать путь до драйвера Chrome
path = '/Volumes/Elements/chromedriver 2'

# Ссылка на сайт
url = 'https://ria.ru/location_Arktika/'
driver = webdriver.Chrome(path)
driver.get(url)

more_url = driver.find_element_by_class_name('list-more')
driver.execute_script("arguments[0].click();", more_url)

SCROLL_PAUSE_TIME = 4

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, 'lxml')
content = soup.find('div', {'class': 'content'})
links = content.find_all('a', class_="list-item__title color-font-hover-only")

driver.quit()

# Здесь будут храниться все ссылки (он скроллится до конца, аж до 2009 года, если не ошибаюсь)
links_news = []
for link in links:
    l = link.get('href')
    links_news.append(l)

print(links_news)

for i in range(2011, 2023):

    with open("news_" + str(i) + '.txt', 'w', encoding='utf-8') as f:

        for link in links_news:
            
            begin = link.find('ru')+3
            year = link[begin:begin+4]

            if year == str(i):
                print(link)
                l = requests.get(link)
                soup = BeautifulSoup(l.text, 'lxml')
                for text in soup.findAll('div', class_='article__text'):
                    f.write(text.text)