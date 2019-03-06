import pandas as pd
import csv

class Ingredient:
    def __init__(self, group, prop):
        self.group = group
        self.property = prop

df = pd.read_csv('FOOD_DES.csv')

master_dict = {}

for group in df['FdGrp_Cd']:
    if group not in master_dict:
        master_dict[group] = []

item = []