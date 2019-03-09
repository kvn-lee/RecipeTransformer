import pandas as pd
import fooddict
import transformationdict


##returns the best name that matches the dictionary for the ingredient
def ingredienttodict(name):
   if name in fooddict.master_dict:
       return name
   ## add addtional matching later

def dicttotrans(name, trans, originalname):
   entry = fooddict.master_dict[name]
   grouping = entry[0] #example, milk
   maincategory = entry[1] #ex baking products
   #check if sub category is in dictionary
   if grouping in ingredientlist.transformdict:
       transops = ingredientlist.transformdict[grouping]
       if type(transops) is dict:
           name.replace(grouping, "").strip()
           if transops[name] in transops:
               transops = transops[name]
           else:
               transops = transops['else']
   elif maincategory in transops:
       transops = ingredientlist.transformdict[maincategory]
   else: return None
   return transops.trans

def translate(trans):
   if trans == None: print('hi')
       #do nothing   
   if type(trans) == int: print('hi') #scale
        #scale
   elif type(trans) == list:
       spicedict() ## change this later
   #if it starts or ends with a + add the words
   elif trans == 'remove': print('hi')
   else: ingredientlist.transinstructions[trans]