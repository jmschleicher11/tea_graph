#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 07:45:25 2021

@author: Floreana
"""
from bs4 import BeautifulSoup
import requests
import json
import re
import time

from url_file import url_string



def clean_description(json_description):
    """ Just pull the ingredients from the description and ignore the rest"""
    desc_html = BeautifulSoup(json_description, 'html.parser')
    ing_string = desc_html.find_all('strong')[-1].contents[0]
    ing_string = re.sub(r'\xa0', r' ', ing_string)
    ing_string = re.sub(r'(^Ingredients: |\.)', '', ing_string)
    ingredients = [item.lower() for item in ing_string.split(' + ')]
    
    return ingredients

def get_tags(tag_list):
    
    try:
        origin_string = list(filter(lambda x: x.lower().startswith('origin:'), 
                                tag_list))[0]
        origin = re.search(r'(?<=(O|o)rigin:)[\w].*', origin_string)[0].lower()
        tag_list.remove(origin_string)
    except: 
        origin = ''
        
    try:
        looseleaf_string = list(filter(lambda x: 
                                       x.lower().startswith('looseleaf:'), 
                                       tag_list))[0]
        tag_list.remove(looseleaf_string)
    except:
        pass
        
    tags = [item.lower() for item in tag_list]
    
    return origin, tags


def clean_info_json(info_json):
    clean_info = {}
    
    clean_info['id'] = str(info_json['id'])

    ## Pull the name and steep number from the title
    name = re.search(r'[\w].*(?=\s\(.*\))', info_json['title'])
    if name:        
        clean_info['name'] = name[0]
    else:
        clean_info['name'] = info_json['title']
        
    short_id = re.search(r'(?<=Steep No. )[\w\d]{4,6}', info_json['title'])
    if short_id:
        clean_info['short_id'] = short_id[0]
    else:
        clean_info['short_id'] = ''
        
    ## Get the ingredients from the description
    ingredients = clean_description(info_json['description'])
    clean_info['ingredients'] = ingredients
    
    ## Get the tea type
    clean_info['type'] = info_json['type']
    
    ## Get the origin and tags from the tags section
    origin, tags = get_tags(info_json['tags'].copy())
    clean_info['origin'] = origin
    clean_info['tags'] = tags
    
    ## Get the minimum price for the tea
    clean_info['min_price'] = info_json['price_min']
    
    return clean_info


categories = ['pu-erh', 'black-tea', 'green-tea', 'herbal-tea', 'mate-tea', 
             'oolong-tea', 'organic', 'rooibos', 'white-tea']

all_tea_info = []

for category in categories:
    
    ## Some categories have multiple pages (no more than 6)
    sub_pages = [category] + [category+'?page='+str(i) for i in range(1,6)]
    for sub_page in sub_pages:
        print(sub_page)
        time.sleep(10)
        url = url_string+sub_page
        page_info = requests.get(url)
        soup = BeautifulSoup(page_info.content, 'html.parser')
        tea_json = soup.find_all(type='application/json')
        
        ## This will be empty if the page doesn't exit
        if len(tea_json[2:]) == 0:
            break
        else:
            ## First two application/json tags in pages are not relevant
            for item in tea_json[2:]:
                info = json.loads(item.contents[0])  
                tea_dict = clean_info_json(info)
                all_tea_info.append(tea_dict)
            
final_tea_dict = {"items": all_tea_info}
            
with open("./data/all_tea_info.json", "w") as outfile: 
    json.dump(final_tea_dict, outfile)