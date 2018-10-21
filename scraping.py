from bs4 import BeautifulSoup as BS
import requests


html = requests.get('https://www.python.org')
# print(html.text)

soup = BS(html.text, 'lxml')

titles = soup.find_all('title')
for title in titles:
    print(title.text)

print('\n##########')

intros = soup.find_all('div', {'class': 'introduction'})
for intro in intros:
    print(intro.text)
