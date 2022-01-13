#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:31:14 2020

@author: sank
"""
import json
import requests
import secrets
import time
#from bs4 import BeautifulSoup
#import pandas as pd
import csv 
from datetime import date

### Specify temporary PATH!
path_to_folder = r'B:\path\to\folder\\'


city_codes = ['WAW']
class glovo_extractor:
    
    def __init__(self, city_codes):
        self.city_codes = city_codes
        self.resto_info = [['cityCode', 'address', 'highestMinBasketSurcharge', 'marketplace', 'name', 'phoneNumber', 'serviceFee',  'suggestionKeywords']]
        finale = self.final_job(city_codes)
        

        
    def get_response(self, city_code):
        headers = {
            'authority': 'api.glovoapp.com',
            'glovo-api-version': '13',
            'glovo-app-version': '7',
            'glovo-app-platform': 'web',
            'glovo-language-code': 'pl',
            'accept': 'application/json',
            'glovo-location-city-code': f'{city_code}',
            'glovo-app-type': 'customer',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'glovo-device-id': '115218552',
            'origin': 'https://glovoapp.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        
        params = (
            ('category', 'RESTAURANT'),
        )
        time.sleep(secrets.choice(range(1,5)))
        response = requests.get('https://api.glovoapp.com/v3/stores', headers=headers, params=params)

        return response.text

    def get_json(self, response_text):
        #soup = BeautifulSoup(response_text, 'html.parser')
        json_content = json.loads(response_text)
        print(json_content)
        return json_content
    
    def get_infos(self, json_content):
        temporary_list = []
        for resto in json_content['stores']:
            highestMinBasketSurcharge = resto['highestMinBasketSurcharge']
            if len(highestMinBasketSurcharge) == 0:
                highestMinBasketSurcharge = 0
            else:
                highestMinBasketSurcharge = float(resto['highestMinBasketSurcharge'].replace(',','.').split()[0])
    
        
            temporary_list.append([resto['cityCode'], resto['address'], highestMinBasketSurcharge, resto['marketplace'], resto['name'], resto['phoneNumber'], resto['serviceFee'], resto['suggestionKeywords']])
        return temporary_list
    
    def append_restos(self, temporary_list):
        return self.resto_info.append(temporary_list)
    
    def final_job(self, city_codes):
        for city_code in city_codes:
            response_text = self.get_response(city_code)
            json_content = self.get_json(response_text)
            temporary_list = self.get_infos(json_content)
            self.resto_info.append(temporary_list)
        return self.resto_info

list_of_resto = glovo_extractor(city_codes)

lol = list_of_resto.resto_info
all_datas = [lol[0]]

for item_1 in lol[1:]:
    for item in item_1:
        all_datas.append(item)
        print(item)

today = date.today()

date_st = str(today.strftime("%m_%Y"))

output_filename = 'output_glovo_'
whole_filepath = path_to_folder + output_filename+date_st +'.csv'
with open(whole_filepath,'w', encoding='utf-8') as file:
    wr = csv.writer(file)
    wr.writerows(all_datas)
