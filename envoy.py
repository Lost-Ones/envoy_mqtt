import requests
from bs4 import BeautifulSoup
import re


response = requests.get('http://192.168.50.60/production?locale=en')
soup = BeautifulSoup(response.content, 'html.parser')
#print(soup)

td = soup.find_all('td')

#for tag in soup.find_all('td'):
#        if 'Currently' in tag:
#            print(tag.text)

soup_td_list = list(soup.find_all('td'))

power_status = {}
for index, tag in enumerate(soup_td_list):
  if 'Currently' in tag:
    #print(tag.text, soup_td_list[index + 1].text)
    temp = soup_td_list[index + 1].text
    if ' kW' in temp:
      multiplyer = 1000
    if ' W' in temp:
      multiplyer = 1
    power = soup_td_list[index + 1].text.replace(' kWh','').replace(' kW','').replace(' W','')
    power = float(power)
    power = power * multiplyer 

    power_status['Currently'] = power #soup_td_list[index + 1].text.replace(' kW','')

for index, tag in enumerate(soup_td_list):
  if 'Today' in tag:
    temp = soup_td_list[index + 1].text
    if ' kWh' in temp:
      multiplyer = 1000
    if ' Wh' in temp:
      multiplyer = 1
    power = soup_td_list[index + 1].text.replace(' kWh','').replace(' Wh','')
    power = float(power)
    power = power * multiplyer 
    #print(tag.text, soup_td_list[index + 1].text)
    power_status['Today'] = power #soup_td_list[index + 1].text.replace(' kWh','').replace(' Wh','')

for k,v in power_status.items():
    print(f'{k} - {v}')

#current_wattage = get_current_wattage(soup)

# Print the current wattage value
#print(current_wattage)