import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
for i in range(1,2):
  print("HI")
  url = "https://2gis.kz/almaty/search/%D0%B5%D0%B4%D0%B0/page/{}?queryState=center%2F76.945152%2C43.23845%2Fzoom%2F12"
  source = urllib.request.urlopen(url.format(i)).read()
  soup = BeautifulSoup(source)
  content = soup.find_all("div",class_="searchResults__content")

  titles_of_restaurants = [i.get('alt', None) for i in soup.find_all('img')]
  info = [i.text for i in soup.find_all('div',class_ = 'miniCard__micro')]

  address = [i.text for i in soup.find_all('div',class_ = 'miniCard__desc _address')]
  additional = soup.find_all("li","miniCard__attrsItem")
  average_check = []
  for i in additional:
    if(i.text[0:7] == 'Средний'):
      average_check.append(i.text)


  len_restaurants = len(titles_of_restaurants)
  while(len(address) < len_restaurants):
    address.append('none')

  while(len(average_check) < len_restaurants):
    average_check.append('none')
  
  print(len(titles_of_restaurants))
  print(len(info))
  print(len(address))
  print(len(average_check))
  
  print(titles_of_restaurants)
  print(info)
  print(address)
  print(average_check)

  data = {'title_of_restaurant': titles_of_restaurants, 'description': info,'address':address,'average check':average_check}
  print(data)
  df = pd.DataFrame(data=data)
  print(df.head())
  df.to_excel(("output%d.xlsx")%(i))