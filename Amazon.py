from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import requests
import pandas as pd
from time import sleep
import os
headers = {
    'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept-Language' : 'en-US, en;q=0.5'
}
arama = input("Aramak istediğiniz şey nedir?:")
search_query = arama.replace(' ', '+')
url = 'https://www.amazon.com/s?k={0}'.format(search_query)


items = []
for i in range (1,5):
    print('Yükleniyor {0}...'.format(url + '&page = {0}'.format(i)))
    response = requests.get(url + '&page = {0}'.format(i), headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text
        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find('span', {'class': 'a-size-base'}).text
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            try:
                price = float(price1 + price2)
            except ValueError:
                price = float(price.replace('%',''))
            product_url= 'http://amazon.com' + result.h2.a['href']
            items.append([product_name, rating, rating_count, price, product_url])

        except AttributeError:
            continue

df = pd.DataFrame(items, columns = ['product', 'rating', 'rating count', 'price', 'product url'])
df.to_csv('{0}.csv'.format(search_query), index = False)

#rows = [ ]
#with open(arama + '.csv', 'r') as csvfile:
#    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#    for row in reader:
#    data = ', '.join(row)
#        rows.append(data)
#print(rows)

