import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd

driver_path = "C:\Program Files (x86)\chromedriver.exe"
browser = webdriver.Chrome(driver_path)
veri = input("#Arama:")
browser.get("https://twitter.com/search?q="+veri+"&src=recent_search_click")
browser.maximize_window()
time.sleep(2)

sonuc = []
twit = browser.find_elements("xpath","//div[@data-testid='tweetText']")
time.sleep(2)
print("................\n" + str(len(twit)) + "adet twit çekildi \n ...............")
for i in twit:
    sonuc.append(i.text)


sayaç = 0
son = browser.execute_script("return document.documentElement.scrollHeight")
while True:
    if sayaç > 3 :
        break
    browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
    time.sleep(2)

    yeni = browser.execute_script("return document.documentElement.scrollHeight")
    if son == yeni :
        break
    son = yeni
    sayaç += 1
    twit = browser.find_elements("xpath", "//div[@data-testid='tweetText']")
    time.sleep(2)

    print("................\n" + str(len(twit)) + "adet twit çekildi \n ...............")
    for i in twit:
        sonuc.append(i.text)

adet = 1
with open("Tiwitler.txt","w", encoding= "UTF-8") as file:    ## "w" formatı o isimde dosya yoksa olusturur.
    for a in sonuc:
        file.write(f"{adet} - {a}\n")
        adet += 1
print("dosya oluşturuldu.")

