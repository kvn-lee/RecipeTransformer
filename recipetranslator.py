import fooddict
import transformationdict
import specialtransformations
import math
import re
from fractions import Fraction
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import copy


addspecialsteps = []
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
        potentials = re.sub(",", "",direction["direction"])
        for ing in direction['ingredients']:
            if ing in transingredients:                
                ingredient_match = process.extractOne(ing, potentials.split())
                component = direction_comp[idx]
                new_direction = component["direction"].replace(ingredient_match[0], transingredients[ing])
                new_direction = re.sub(r'\b(.+)\s+\1\b', r'\1', new_direction)
                component["direction"] = new_direction                
                for i in range (len(directioning)):
                    if directioning[i] == ing:
                        directioning[i] = transingredients[ing]
                component['ingredients'] = directioning
                new_direction_comp[idx] = component
    if addspecialsteps:
        addspecialsteps.extend(new_direction_comp)
        new_direction_comp = addspecialsteps
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
        translation = preform_ingredient_trans(ingredient, transingredient) #return new ingredient object, list of them,  None, or 'remove'
        #if no translation append old ingredient object ot new ingredient list
        if translation == None: 
            #check if a transformation caused a duplicate ingredient, if so change amount of previous instead of adding
            check_for_dups(bestmatch, ingredient, lstIncIngNames, newingredientlst)
            '''
            if bestmatch not in lstIncIngNames:
                lstIncIngNames.append(bestmatch)
                newingredientlst.append(ingredient)
            else:
                i = lstIncIngNames.index(bestmatch)
                oldinstance = newingredientlst[i]
                newingredientlst[i] = addunits(oldinstance, ingredient)
            '''
        elif type(translation) == list:
            #not checking if already on list because we want to preferably keep it separate
            for replace in translation:
                lstIncIngNames.append(replace['name'])
                newingredientlst.append(replace)
        elif not translation == 'remove': 
            check_for_dups(translation['name'], ingredient, lstIncIngNames, newingredientlst)
            '''
            if translation['name'] not in lstIncIngNames:
                lstIncIngNames.append(translation['name'])
                newingredientlst.append(ingredient)
            else:
                i = lstIncIngNames.index(translation['name'])
                oldinstance = newingredientlst[i]
                newingredientlst[i] = addunits(oldinstance, ingredient)
            '''
        
    print('included ingredients')
    print(lstIncIngNames)
    return newingredientlst

def check_for_dups(newingname, fullingredient, pastingnames, inglst):
    if newingname not in pastingnames:
        pastingnames.append(newingname)
        inglst.append(fullingredient)
    else:
        i = pastingnames.index(newingname)
        oldinstance = inglst[i]
        inglst[i] = addunits(oldinstance, fullingredient)


def addunits(old, new):
    if old['quantity'] == None and new['quantity'] == None:
        old['quantity'] == None
    elif old['quantity'] == None:
        old['quantity'] = new['quantity']
        old['unit'] = new['unit']
    elif new['quantity'] == None:
        pass
    else:
        oldquantitystr = str(old['quantity'])
        oldquantity = convert_to_decimal(oldquantitystr)
        newquantitystr = new['quantity']
        newquantity = convert_to_decimal(newquantitystr)
        
        if new['unit'].rstrip('s') == old['unit'].rstrip('s'):
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
   elif trans in specialtransformations.specialtrans:
       #print hi
        return special_ingredient_transform(original, trans)
   else:
       #transinstructions[trans]        
        return switchingredients(original,trans)

def special_ingredient_transform(original, trans):
    transsteps = specialtransformations.specialtrans[trans]
    replacementingredients = transsteps.ingredients
    lstnewingredients = []
    global translatedingredients
    global addspecialsteps
    sub = ''
    ing = []
    for ele in replacementingredients:
        newingredient = copy.deepcopy(original)
        newingredient['name'] = ele.name
        newingredient['unit'] = ele.unit
        newingredient['quantity'] = convert_to_decimal(str(ele.measurement)) * convert_to_decimal(str(original['quantity']))
        newingredient['original'] = str(newingredient['quantity']) + ' ' + ele.unit + ' ' + ele.name
        sub = sub + ' ' + ele.name
        ing.append(ele.name)
        lstnewingredients.append(newingredient)
    sub = sub + ' mixture'
    translatedingredients[original['name']] = sub.strip()
    newdirection = {}
    newdirection['ingredients'] = ing
    newdirection['methods'] = ['mix']
    newdirection['time'] = None
    newdirection['tools'] = ''
    newdirection['direction'] = transsteps.addsteps
    addspecialsteps.append(newdirection)
    return lstnewingredients


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

def init_spices():
    global lstmexspices
    if not lstmexspices:
        lstmexspices = ["cumin", "chile powder", "adobo seasoning", "chipotle chile powder", "oregano", "cilantro",
                        "epazote", "garlic"]

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
    global lstmexspices
    init_spices()
    trans = lstmexspices[0]
    del lstmexspices[0]
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
        
lstmexspices = ["cumin", "chile powder", "adobo seasoning", "chipotle chile powder", "oregano", "cilantro", "epazote", "garlic"]



if __name__ == '__main__':
    # test = find_match_in_fooddict("chicken broth")
    # print(test)
    # print(fooddict.master_dict[test])
    # print(return_trans_in_transformationdict(test, "toVegetarian"))
    #ngredent = "campbell's condensed french onion soup"
    #direction = "Stir in the onion soup"
    #match = process.extractOne(ingredent, direction.split())
    name= find_match_in_fooddict('eggs')
    print(name)
    print()
    print(return_trans_in_transformationdict(name, 5))
    #print(match)