import pandas as pd
import fooddict
import transformationdict
import Recipe
import math
import re
from fractions import Fraction
from difflib import SequenceMatcher
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import copy

choices = list(fooddict.master_dict)
translatedingredients = {} # list of the dictionaries fro the included ingredients
#lstIncIngNames = list() # list of the ingredient names in the recipe after translation

def maintransformation(recipe, trans):
    global translatedingredients
    translatedingredients.clear()
    recipe.ingredient_components = translate_ingredients(recipe.ingredient_components, trans)
    recipe.direction_components = translate_instructions(recipe.direction_components, translatedingredients, copy.deepcopy(recipe.direction_components))    
    recipe.title = translate_title(recipe.title, translatedingredients)
    return recipe

def translate_instructions(direction_comp, transingredients, new_direction_comp):
    global translatedingredients
    for idx, direction in enumerate(direction_comp):
        new_direction = []
        directioning = direction['ingredients']
        for ing in direction['ingredients']:
            if ing in transingredients:
                potentials = re.sub(",", "",direction["direction"])
                ingredient_match = process.extractOne(ing, potentials.split())
                component = direction_comp[idx]
                new_direction = component["direction"].replace(ingredient_match[0], transingredients[ing])
                component["direction"] = new_direction                
                for i in range (len(directioning)):
                    if directioning[i] == ing:
                        directioning[i] = transingredients[ing]
                component['ingredients'] = directioning
                new_direction_comp[idx] = component
    return new_direction_comp

def translate_title(title, translatedingredients):
    title = title.lower()
    for title_word in title.split():
        if title_word in translatedingredients:
            potentials = re.sub(",", "", title)
            ingredient_match = process.extractOne(title_word, potentials.split())
            title = title.replace(ingredient_match[0], translatedingredients[title_word])

    title = " ".join(w.capitalize() for w in title.split())
    return title

def translate_ingredients(ingredient_comp, trans):
    lstIncIngNames = []
    newingredientlst = [] #new list of ingredients after transformation
    #translatedingredients = {}
    for ingredient in ingredient_comp:
        bestmatch = find_match_in_fooddict(ingredient['name']) #find best match in food dict, return name of best match
        transingredient = return_trans_in_transformationdict(bestmatch, trans) #find right transformation for the best match and transformation wanted
        translation = preform_ingredient_trans(ingredient, transingredient) #return new ingredient object, None, or 'remove'
        #if no translation append old ingredient object ot new ingredient list
        if translation == None: 
            #check if a transformation caused a duplicate ingredient, if so change amount of previous instead of adding
            if bestmatch not in lstIncIngNames:
                lstIncIngNames.append(bestmatch)
                newingredientlst.append(ingredient)
            else:
                i = lstIncIngNames.index(bestmatch)
                oldinstance = newingredientlst[i]
                newingredientlst[i] = addunits(oldinstance, ingredient)
        elif not translation == 'remove': 
            if translation['name'] not in lstIncIngNames:
                lstIncIngNames.append(translation['name'])
                newingredientlst.append(ingredient)
            else:
                i = lstIncIngNames.index(translation['name'])
                oldinstance = newingredientlst[i]
                newingredientlst[i] = addunits(oldinstance, ingredient)
    print('included ingredients')
    print(lstIncIngNames)
    return newingredientlst

def addunits(old, new):
    oldquantitystr = str(old['quantity'])
    oldquantity = convert_to_decimal(oldquantitystr)
    newquantitystr = new['quantity']
    newquantity = convert_to_decimal(newquantitystr)
    
    if new['unit'] == old['unit']:
        old['quantity'] = newquantity + oldquantity
        old['original'] = old['original'].replace(oldquantitystr, str(old['quantity']))
    else: 
        if new['unit'] == None: new['unit'] = ''
        if old['unit'] == None: old['unit'] = ''    
        old['quantity'] = str(oldquantity) + str(newquantity)
        old['unit'] = old['unit'] + ' ' + new['unit']
        newunitmeasurement = str(oldquantity) + ' ' + old['unit'] + ' and ' + str(newquantity) + ' ' + new['unit']
        old['original'] = old['original'].replace(oldquantitystr, newunitmeasurement)
    return old

def convert_to_decimal(strnum):
    if '/' in strnum:
        oldquantity = float(sum(Fraction(i) for i in strnum.split()))
    else:
        oldquantity = float(strnum)
    return oldquantity


##returns the best name that matches the dictionary for the ingredient. Used to categorize ingredients
def find_match_in_fooddict(name):
   global choices
   if name in choices:
       return name
   else:
       best_match_choices = process.extractOne(name, choices, scorer=fuzz.token_set_ratio)
       return best_match_choices[0]

#using best match in fooddict's categories, find transformation in the transformationdict
def return_trans_in_transformationdict(name, trans):
   entry = fooddict.master_dict[name]
   grouping = entry[0] #example, milk
   maincategory = entry[1] #ex baking products
   #check if sub category is in dictionary
   if grouping in transformationdict.transformdict:
       transops = transformationdict.transformdict[grouping]
       if type(transops) is dict: #subcategories within category
           oname = name.replace(grouping, "").strip()
           if oname in transops:
               transops = transops[oname]
           else:
               transops = transops['else']
   elif maincategory in transformationdict.transformdict:
       transops = transformationdict.transformdict[maincategory]
   else: return None
   return return_desired_trans_option(transops.trans, trans)

def return_desired_trans_option(options, trans):
    sub = None
    if trans == 1:
        sub = options.toVegetarian
    elif trans == 2:
        sub = options.fromVegetarian
    elif trans == 3:
        sub = options.toHealthy
    elif trans == 4:
        sub = options.fromHealthy
    elif trans == 5:
        sub = options.toVegan
    elif trans == 6:
        sub = options.fromVegan
    elif trans == 7:
        sub = options.toMexican
    elif trans == 8:
        sub = options.fromMexican
    return sub


#check results of transformationdictionary, 
#depending on result return substitution ingredients, else return none
def preform_ingredient_trans(original, trans):
   global translatedingredients
   if trans == None:
       return None   
   elif type(trans) == int or type(trans) == float:
        return scale(original, trans)
   elif type(trans)== str and trans.startswith('+') or trans.endswith('+'):
       return appenddescriptors(original, trans)
   elif trans == 'remove': 
       return 'remove'
   else:
       #transinstructions[trans]        
        return switchingredients(original,trans)

def switchingredients(original, trans):
    global translatedingredients
    oldingredient = original['name']
    if trans == 'mexherbs' or trans == 'mexspices':
       original = mextrans(original, trans)
       trans = original['name']
    else:
        newfull = None
        if original["quantity"] and original["unit"]:
            newfull = " ".join([original["quantity"], original["unit"], trans])
        elif original['quantity']:
            newfull = " ".join([original["quantity"], trans])
        else: newfull = trans
        original['name'] = trans
        original['original'] = newfull
        original['description'] = 'None'
    translatedingredients[oldingredient] = trans
    return original

def appenddescriptors(original, trans):
    #newfull = None
    if trans.startswith('+'):
        trans = trans[1:]
        if trans not in original['name']:
            name = ' '.join([original['name'], trans])
    else: 
        trans = trans[:-1]
        if trans not in original['name']:
            name = ' '.join([trans,original['name']])
    if original["quantity"] and original["unit"]: 
        newfull = " ".join([original["quantity"], original["unit"], name])
    elif original['quantity']:
        newfull = " ".join([original["quantity"], name])
    else: newfull = name
    original['original'] = newfull
    original['name'] = name
    return original

def scale(original, trans):
    #check measurement
    oldquantitystr = original['quantity']
    oldquantity = convert_to_decimal(oldquantitystr)
    if original['unit'] == None:
        original['quantity'] = math.ceil(oldquantity* trans)
        if original['quantity'] == 1:
            original['name'] = original['name'] + 's'
    else: 
        original['quantity'] = str(oldquantity * trans)
        if original['quantity'] == 1:
            original['unit'] = original['unit'] + 's'
    original['original'] = original['original'].replace(oldquantitystr, original['quantity'])
    return original

def mextrans(original, trans):
    global translatedingredients
    if trans == 'mexherbs':
        trans = lstmexherbs[0]
        del lstmexherbs[0]
    else:
        trans = lstmexspices[0]
        del lstmexherbs[0]
    newfull = None
    if original["quantity"] and original["unit"]:
        newfull = " ".join([original["quantity"], original["unit"], trans])
    elif original['quantity']:
        newfull = " ".join([original["quantity"], trans])
    else: newfull = trans
    original['name'] = trans
    original['original'] = newfull
    #translatedingredients[original['name']]= replacement['name']
    return original
        
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
    # test = find_match_in_fooddict("chicken broth")
    # print(test)
    # print(fooddict.master_dict[test])
    # print(return_trans_in_transformationdict(test, "toVegetarian"))
    ingredent = "campbell's condensed french onion soup"
    direction = "Stir in the onion soup"
    match = process.extractOne(ingredent, direction.split())
    name= find_match_in_fooddict('frozen cooked shrimp without tails')
    print(name)
    print(return_trans_in_transformationdict(name, 5))
    #print(match)