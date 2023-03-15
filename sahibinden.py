from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import requests
import pandas as pd
from time import sleep
import io

headers = {
    'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept-Language' : 'en-US, en;q=0.5'
}
arama = input("Aramak istediğiniz şey nedir?:")
search_query = arama.replace(' ', '+')
url = 'https://www.sahibinden.com/kelime-ile-arama?query_text={0}'.format(search_query)
response = requests.get(url, headers = headers, allow_redirects=False)
my_soup = BeautifulSoup(response.content, 'html.parser')
results = str(my_soup.find_all('title'))

items = []
def deneme(url):
    num_pages = 100
    for page in range(0, num_pages + 1):
        url_3 = f'https://www.sahibinden.com' + url + "&pagingOffset={0}".format(str(page * 20))
        print(url_3)
        response_2 = requests.get(url_3, headers=headers)
        print(response_2.status_code)
        if(response_2.status_code==429):
            print("fazla istek")
            sleep(10)
            print("timeout")
            continue
        my_soup_1 = BeautifulSoup(response_2.content, 'html.parser')

        listings = my_soup_1.find_all('tr', {'class': 'searchResultsItem'})
        denek2 = my_soup_1.find("tbody",{"class":"searchResultsRowClass"})
        denek3 = denek2.find_all("tr",{"class":"searchResultsItem"})
        def my_arr(data):
            return data.text
        for dene in denek3 :
            try:
                no = dene["data-id"]
                price_elem = dene.find('td', {'class': 'searchResultsPriceValue'}).find("span").text
                print(price_elem)
                product_elem = dene.find('a', {'class': 'classifiedTitle'}).text.strip()
                date_elem = dene.find('td', {'class': 'searchResultsDateValue'}).find_all("span")
                arr_map = list(map(my_arr,date_elem))
                arr_join =(" ").join(arr_map)
                location_elem = dene.find('td', {'class': 'searchResultsLocationValue'}).text.strip() # buraya bak
                row = {
                   'Price': price_elem,
                   'Product Name': product_elem,
                    'Date': arr_join,
                    'Location': location_elem,
                    'ID': no
                }
                items.append(row)
                print(row)

                df = pd.DataFrame(items, columns=['Price', 'Product Name', 'Date', 'Location', 'ID'])
                df.to_csv('{0}.csv'.format(search_query), index=False, encoding='utf-8-sig')

            except AttributeError:
                continue
            except KeyError:
                continue

print(response.status_code)
if (response.status_code==200):


    my_soup1 = my_soup.find_all('div',class_= 'category-top-level')

    for category in my_soup1:
        name = category.a.text.strip()
        count = int(category.a.strong.span.text.strip().replace(',', ''))
        my_list = category.a['href'].split("&")
        try:
            category_id = list(filter(lambda x: x.startswith('category='), my_list))[0].split('=')[1]
            print(name.replace(str(count),"").replace("ilan"," "), count,"...tane ilan var." , "ID: " , category_id)

        except IndexError:
            print("hata")
    Id = input("Kategori ID seç:")

    url_2 = 'https://www.sahibinden.com/kelime-ile-arama-yonlendir?disableEstimation=false&category={0}&query_text={1}'.format(str(Id),search_query)

    response_2 = requests.get(url_2, headers=headers, allow_redirects=False)
    redirect = response_2.headers['Location']
    print(redirect)
    my_soup_1 = BeautifulSoup(response_2.content, 'html.parser')

    listings = my_soup_1.find_all('tr', {'class': 'searchResultsItem'})

    deneme(redirect)

elif(response.status_code==301):
    print(response)
    redirect = response.headers['Location']
    deneme(redirect)

else:
    print("hata",response.status_code)



#with io.open('{0}.csv'.format(search_query), mode='w', newline='', encoding='utf-8') as file:

#    writer = csv.DictWriter(file, fieldnames=['Price', 'Product Name', 'Date', 'Location', 'ID'])
 #   writer.writeheader()
  #  writer.writerows(items)



