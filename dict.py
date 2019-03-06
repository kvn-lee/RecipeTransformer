import pandas as pd
import csv

df = pd.read_csv('FOOD_DES.csv')

master_dict = {}

for desc in df['Long_Desc']:
    desc = desc.lower()
    prod = desc.split(',')
    if prod[0] in master_dict:
        for item in prod[1:]:
            master_dict[prod[0]].append(item[1:])
    else:
        master_dict[prod[0]] = prod[2:]

print(master_dict)