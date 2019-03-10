import pandas as pd
import fooddict
import transformationdict
import Recipe
import math
from fractions import Fraction
from difflib import SequenceMatcher
from fuzzywuzzy import process

choices = list(fooddict.master_dict)
translatedingredients = {}
lstofincludedingredients = []

def maintransformation(recipe, trans):
    newingredientlst = []
    global translatedingredients
    translatedingredients.clear()
    for ingredient in recipe.ingredient_components:
        bestmatch = ingredienttodict(ingredient['name'])
        transingredient = dicttotrans(bestmatch, trans)
        translation = translatetrans(ingredient, transingredient)
        if translation == None: 
            newingredientlst.append(ingredient)
            lstofincludedingredients = lstofincludedingredients.append(bestmatch)
        else: 
            newingredientlst.append(translation)
            lstofincludedingredients =lstofincludedingredients.append(translation['name'])
    recipe.ingredient_components = newingredientlst
    return recipe


##returns the best name that matches the dictionary for the ingredient
def ingredienttodict(name):
   global choices
   if name in fooddict.master_dict:
       return name
   else:
       bestmatch = process.extractOne(name, choices)
       if bestmatch: return bestmatch[0]
       else: return None

#using best match in fooddict, find transformation in the transformationdict
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

#check results of transformationdictionary, 
#depending on result return substitution ingredients, else return none
def translatetrans(original, trans):
   if trans == None:
       return None   
   if type(trans) == int:
        return scale(original, trans)
   elif trans == 'mexherbs' or trans == 'mexspices':
       return mextrans(original, trans)
   #if it starts or ends with a + add the words
   elif trans == 'remove': 
       return 'remove'
   else: transinstructions[trans]

def scale(original, trans):
    #check measurement
    nmeasure = {}
    nmeasure['name'] = original['name']
    nmeasure['unit'] = original['unit']
    nmeasure['description'] = None
    nmeasure['prep'] = None
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


def mextrans(original, trans):
    replacement = {}
    replacement['unit'] = original['unit']
    replacement['quantity'] = original['quantity']
    replacement['description'] = None
    replacement['prep'] = None
    if trans == 'mexherbs':
        replacement['name'] = lstmexherbs[0]
        del lstmexherbs[0]
    else:
        replacement['name'] = lstmexspices[0]
        del lstmexherbs[0]
    return replacement
        
lstmexherbs = ["garlic", "oregano", "cilantro", "epazote"]
lstmexspices = ["cumin", "chile powder", "adobo seasoning", "chipotle chile powder"]

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