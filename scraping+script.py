
# coding: utf-8

# In[2]:

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import ssl
import re

number_of_pages = 50

restaurants = []
infos = []
addresses = []
checks = []

for i in range(1, number_of_pages + 1):
    print("processing page " + str(i) + " ... ")
    url = "https://2gis.kz/almaty/search/%D0%B5%D0%B4%D0%B0/page/{}?queryState=center%2F76.945152%2C43.23845%2Fzoom%2F12"
    source = urllib.request.urlopen(url.format(i), context=ssl.SSLContext()).read()
    soup = BeautifulSoup(source, features="html.parser")

    content = soup.select(".searchResults__list > article > .miniCard__content")

    restaurants.extend([x.text for x in soup.select(".searchResults__list > article > .miniCard__content > header > h3")])

    for d in content:
        info = d.select(".miniCard__micro") 
        if (len(info) == 0):
            infos.append(None)
        else:
            infos.append(info[0].text)
      
    for d in content:
        address = d.select(".miniCard__desc > .miniCard__address") 
        if (len(address) == 0):
            addresses.append(None)
        else:
            addresses.append(address[0].text)
      
    for d in content:
        check = d.select(".miniCard__additional > .miniCard__attrs > .miniCard__attrsItem") 
        if (len(check) == 0 or 'тнг' not in check[0].text):
            checks.append(0)
        else:
            checks.append(int(re.findall("[0-9]+ тнг", check[0].text)[0].split(" тнг")[0]))

    print ("Processed : restaurants({}), infos({}), addresses({}), checks({})"
    .format(len(restaurants), len(infos), len(addresses), len(checks)))

    data = { 'restaurants': restaurants,
   'infos': infos,
   'addresses': addresses,
   'checks': checks}

    print ("Creating data frame ...")
    df = pd.DataFrame(data=data)
    print(df.head())

    print ("Exporting data to excel ...")
    df.to_excel(("output.xlsx"))

