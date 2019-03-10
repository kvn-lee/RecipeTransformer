import pandas as pd
import fooddict
import transformationdict
import Recipe
import math
from fractions import Fraction
from difflib import SequenceMatcher
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

choices = list(fooddict.master_dict)
translatedingredients = {}
lstofincludedingredients = []

def maintransformation(recipe, trans):
    newingredientlst = []
    newdirectionlst = []
    global translatedingredients
    global lstofincludedingredients
    translatedingredients.clear()
    for ingredient in recipe.ingredient_components:
        bestmatch = ingredienttodict(ingredient['name'])
        transingredient = dicttotrans(bestmatch, trans)
        translation = translatetrans(ingredient, transingredient)
        if translation == None: 
            newingredientlst.append(ingredient)
            if lstofincludedingredients:
                lstofincludedingredients = lstofincludedingredients.append(bestmatch)
        else: 
            newingredientlst.append(translation)
            if lstofincludedingredients:
                lstofincludedingredients =lstofincludedingredients.append(translation['name'])

    new_direction_components = recipe.direction_components
    for idx, direction in enumerate(recipe.direction_components):
        new_direction = []
        if any(ing in direction["ingredients"] for ing in translatedingredients):
            for ing in direction["ingredients"]:
                if ing in translatedingredients:
                    ingredient_match = process.extractOne(ing, direction["direction"].split())
                    component = recipe.direction_components[idx]
                    new_direction = component["direction"].replace(ingredient_match[0], ing)
                    component["direction"] = new_direction
                new_direction_components[idx] = component

        #newdirectionlst.append(new_direction)

    recipe.ingredient_components = newingredientlst
    recipe.direction_components = new_direction_components
    return recipe


##returns the best name that matches the dictionary for the ingredient
def ingredienttodict(name):
   global choices
   if name in fooddict.master_dict:
       return name
   else:
       best_match_choices = process.extractOne(name, choices, scorer=fuzz.token_set_ratio)
       return best_match_choices[0]
       # best_match_pct = 0.0
       # best_match = ""
       # for choice in best_match_choices:
       #     choice = choice[0]
       #     similarity = SequenceMatcher(None, name, choice).ratio()
       #     if similarity > best_match_pct:
       #         best_match_pct = similarity
       #         best_match = choice
       # if best_match: return best_match
       # else: return None

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
   elif maincategory in transformationdict.transformdict:
       transops = transformationdict.transformdict[maincategory]
   else: return None
   t = transops.trans.toVegetarian
   return t

#check results of transformationdictionary, 
#depending on result return substitution ingredients, else return none
def translatetrans(original, trans):
   global translatedingredients
   if trans == None:
       return None   
   if type(trans) == int:
        return scale(original, trans)
   elif trans == 'mexherbs' or trans == 'mexspices':
       return mextrans(original, trans)
   #if it starts or ends with a + add the words
   elif trans == 'remove': 
       return 'remove'
   else:
       #transinstructions[trans]
       nmeasure = {}
       #newfull = original['original'].replace(original['name'], trans)
       if original["quantity"] and original["unit"]:
           newfull = " ".join([original["quantity"], original["unit"], trans])
       nmeasure["original"] = newfull
       nmeasure['name'] = trans
       nmeasure['unit'] = original['unit']
       nmeasure['description'] = None
       nmeasure['prep'] = None
       nmeasure["quantity"] = None
       translatedingredients[original['name']] = trans
       return nmeasure

def scale(original, trans):
    #check measurement
    global translatedingredients
    nmeasure = {}
    nmeasure["original"] = "hi"
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
    global translatedingredients
    replacement = {}
    replacement["original"] = "hi"
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
    translatedingredients[original['name']]= replacement['name']
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

if __name__ == '__main__':
    # test = ingredienttodict("chicken broth")
    # print(test)
    # print(fooddict.master_dict[test])
    # print(dicttotrans(test, "toVegetarian"))
    ingredent = "campbell's condensed french onion soup"
    direction = "Stir in the onion soup"
    match = process.extractOne(ingredent, direction.split())
    print(match)