#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:30:28 2020

@author: steveyyp
"""
import time
import json
import requests
import pandas as pd

# Setup API Key
APIKEY = 'removed'

# Setup filenames and dataframes with dish data
fileName = '/Data/whats-on-the-menu/Menu_Data/'

dish = fileName + 'Dish.csv'
menu = fileName + 'Menu.csv'
item = fileName + 'MenuItem.csv'
page = fileName + 'MenuPage.csv'

df_dish = pd.read_csv(dish)
df_menu = pd.read_csv(menu)
df_item = pd.read_csv(item)
df_page = pd.read_csv(page)

# Generate URL List for API calls
menu_id_list = df_page['menu_id'].unique().tolist()
menu_id_list[:5]

id_len = len(menu_id_list)
urlList = []
for i in range(id_len):
    url = "http://api.menus.nypl.org/menus/" + str(menu_id_list[i]) + "/dishes?token=" + APIKEY
    urlList.append(url)


# API Call
json_data_list_dish = []
start_index = 15000
end_index = 19816

for i in range(start_index,end_index,1):
  time.sleep(0.5)
  r = requests.get(urlList[i])
  if r.status_code == 200:
    json_data_list_dish.append(r.json())
  else:
    print(r.status_code, ' At Iteration ', i)
    break
  print('Completed Iteration ',i,' of ',id_len)

# Save data to .txt file for processing later
with open('/Data/Dishes_Menus_Data/whats-on-the-menu/json_dish_menu_4.txt', 'w') as f:
    json.dump(json_data_list_dish, f)
    
# Setup filename for reading in .txt file to .json 
fileName = '/Data/Dishes_Menus_Data/whats-on-the-menu/json_dish_menu_4.txt'

with open(fileName, 'r') as json_file:
  json_menu = json_file.read()
  
# Load menu data into json
menus = json.loads(json_menu)

# Create Pandas DataFrame
dishes_df = pd.DataFrame()

# Create Pandas DataFrame with all menu data
for i in range(len(menus)):
    load_data = menus[i]['dishes']
    dish_tmp = pd.DataFrame(load_data)
    dishes_df = dishes_df.append(dish_tmp)
    print('Completed Iteration ', i, ' of ', len(menus))

# Save Pandas DF to .csv file to read in for later
dishes_df.to_csv('/Data/Dishes_Menus_Data/whats-on-the-menu/dishes_location_4.csv')