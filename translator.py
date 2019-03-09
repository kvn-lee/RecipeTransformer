import pandas as pd
import fooddict
import transformationdict
import Recipe
import math
from fractions import Fraction

##returns the best name that matches the dictionary for the ingredient
def ingredienttodict(name):
   if name in fooddict.master_dict:
       return name
   ## add addtional matching later

def dicttotrans(name, trans):
   entry = fooddict.master_dict[name]
   grouping = entry[0] #example, milk
   maincategory = entry[1] #ex baking products
   #check if sub category is in dictionary
   if grouping in transformationdict.transformdict:
       transops = transformationdict.transformdict[grouping]
       if type(transops) is dict:
           oname = name.replace(grouping, "").strip()
           if oname in transops:
               transops = transops[oname]
           else:
               transops = transops['else']
   elif maincategory in transops:
       transops = transformationdict.transformdict[maincategory]
   else: return None
   return transops.trans

def translate(original, trans):
   if trans == None: print('hi')
       #do nothing   
   if type(trans) == int:
        scale(original, trans)
   elif type(trans) == list:
       spicedict() ## change this later
   #if it starts or ends with a + add the words
   elif trans == 'remove': print('hi')
   else: transinstructions[trans]

def scale(original, trans):
    #check measurement
    nmeasure = {}
    nmeasure['name'] = original['name']
    nmeasure['unit'] = original['unit']
    oldquantity= float(sum(Fraction(i) for i in original['quantity'].split()))
    if original['unit'] == None:
        nmeasure['quantity'] = math.ceil(oldquantity* trans)
        if original['quantity'] == 1:
            nmeasure['name'] = original['name'] + 's'
    else: 
        nmeasure['quantity'] = oldquantity * trans
        if original['quantity'] == 1:
            nmeasure['unit'] = original['unit'] + 's'
    return nmeasure

    #depending on this scale

class TransSteps:
   ##keep refers to merely replacing ingredient names, not removing original instructions
   ##ie replacing margarine with butter
   ##steps- if keep is True steps can be added for example to add additional steps (like mixing the two
   # ingredients that replace one). If keep is false this is used to replace original steps
   def __init__(self, keep, steps):
       self.keep = keep
       self.steps = steps

transinstructions = {}

#dictionary of subsitution steps
transinstructions['margarine'] = TransSteps(True, None)
transinstructions['softened butter'] = TransSteps(True, None)
transinstructions['tofu'] = TransSteps(True, None)
transinstructions['Tofutti Milk Free Better Than Sour Cream'] = TransSteps(True, None)
transinstructions['non-dairy almond milk whipped cream'] = TransSteps(True, None)
transinstructions['tofu'] = TransSteps(True, None)
transinstructions['tofu'] = TransSteps(True, None)
transinstructions['cream substitute'] = TransSteps(True, None) ##change