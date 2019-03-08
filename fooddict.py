import pandas as pd
import csv

df = pd.read_csv('FOOD_DES.csv')

master_dict = {}
count=0
for item in df['Long_Desc']:
       # print(df['FdGrp_Cd'][1])
      
    desc = item
    desc = desc.lower()
    prod = desc.split(',')
    name = prod[0:2]
    name = name[::-1]
    name = ' '.join(name)
    name.strip()
    if not prod[0] in master_dict:
        master_dict[prod[0]] = [prod[0], df['FdGrp_Cd'][count].lower().strip()]
    if len(prod) >1 and not prod[1] in master_dict:
        master_dict[prod[1].strip()] = [prod[1].strip(), 'unknown']
    #print(prod[1])
    master_dict[name]= [prod[0].strip(), df['FdGrp_Cd'][count].lower().strip()]
    count = count + 1 



'''
    desc = desc.lower()
    prod = desc.split(',')
    if prod[0] in master_dict:
        for item in prod[1:]:
            master_dict[prod[0]].append(item[1:])
    else:
        master_dict[prod[0]] = prod[2:]
'''
print(master_dict)



