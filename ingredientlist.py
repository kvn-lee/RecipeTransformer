import pandas as pd
import fooddict

class Ingredient:
   def __init__(self, trans, categoryName):
       self.trans = trans
       self.categoryName = categoryName

class TransSteps:
   ##keep refers to merely replacing ingredient names, not removing original instructions
   ##ie replacing margarine with butter
   ##steps- if keep is True steps can be added for example to add additional steps (like mixing the two
   # ingredients that replace one). If keep is false this is used to replace original steps
   def __init__(self, keep, steps):
       self.keep = keep
       self.steps = steps

class Trans:
   def __init__(self, toVegetarian, fromVegetarian, toVegan, fromVegan, toHealthy, fromHealthy, toMexican, fromMexican):
       self.toVegetarian = toVegetarian
       self.fromVegetarian = fromVegetarian
       self.toVegan = toVegan
       self.fromVegan = fromVegan
       self.toHealthy = toHealthy
       self.fromHealthy = fromHealthy
       self.toMexican = toMexican
       self.fromMexican = fromMexican

ingdict={}
transformdict={}
transinstructions={}

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
   if grouping in transops:
       transops = transformdict[grouping]
       if type(transops) is dict:
           name.replace(grouping, "").strip()
           if transops[name] in transops:
               transops = transops[name]
           else:
               transops = transops['else']
   elif maincategory in transops:
       transops = transformdict[maincategory]
   else: return None
   return transops.trans

def translate(trans):
   if trans == None:
       #do nothing   
   elif trans == 'spice':
       spicedict() ## change this later
   #if it starts or ends with a + add the words
   elif trans == 'remove'
   else transinstructions[trans]

###Dairy and egg products
transformdict['butter'] = Ingredient(Trans(None, None, 'margarine', None, 'margarine', None, None, None), 'Dairy and Egg Products')
transformdict['cheese'] = Ingredient(Trans(None, None, 'tofu', None, 'tofu', None, None, None), 'Dairy and Egg Products')
transformdict['cream'] = {'sour cream':Ingredient(Trans(None, None, 'Tofutti Milk Free Better Than Sour Cream', None, 'Tofutti Milk Free Better Than Sour Cream', None, None, None), 'Dairy and Egg Products') ,
'whipped cream':Ingredient(Trans(None, None, 'non-dairy almond milk whipped cream', None, 'almond milk whipped cream', None, None, None), 'Dairy and Egg Products') ,
'else':Ingredient(Trans(None, None, {'softened butter':'1/2' , 'plain milk substitute': '1/2'}, None, {'softened butter':'1/5' , 'milk': '4/5'}, None, None, None), 'Dairy and Egg Products')}
transformdict['eggnog'] = Ingredient(Trans(None, None, 'coconut milk', None, 'coconut milk', None, None, None), 'Dairy and Egg Products')
transformdict['sour cream'] = Ingredient(Trans(None, None, 'Tofutti Milk Free Better Than Sour Cream', None, 'plain non-fat yogurt', None, None, None), 'Dairy and Egg Products')
transformdict['whey'] = Ingredient(Trans(None, None, 'brown rice protein powder', None, 'brown rice protein powder', None, None, None), 'Dairy and Egg Products')
transformdict['yogurt'] = Ingredient(Trans(None, None, 'vegan yogurt', None, 'greek yogurt', None, None, None), 'Dairy and Egg Products')
transformdict['egg'] = {'white':Ingredient(Trans(None, None, 'egg white substitute', None, None, None, None, None), 'Dairy and Egg Products'),
'yoke':Ingredient(Trans(None, None, {'water' : '1/4 cup', 'chickpea flour' :'1/4 cup'}, None, 'egg white', None, None, None), 'Dairy and Egg Products'),
'else':Ingredient(Trans(None, None, {'water' : '1/4 cup', 'chickpea flour' :'1/4 cup'}, None, 'egg white', None, None, None), 'Dairy and Egg Products')}
transformdict['butter'] = Ingredient(Trans(None, None, 'margarine', None, 'margarine', None, None, None), 'Dairy and Egg Products')
transformdict['cream substitute'] = Ingredient(Trans(None, None, None, None, None, None, None, None), 'Dairy and Egg Products')
transformdict['ice cream'] = Ingredient(Trans(None, None, 'vegan gelato', None, 'frozen yogurt', None, None, None), 'Dairy and Egg Products')
transformdict['cheese spread'] = Ingredient(Trans(None, None, 'vegan cream cheese', None, 'hummus', None, None, None), 'Dairy and Egg Products')
transformdict['milk'] = {'else': Ingredient(Trans(None, None, 'almond milk', None, 'almond milk', None, None, None), 'Dairy and Egg Products'),
'buttermilk' : Ingredient(Trans(None, None, {'soy milk': '1', 'lemon juice':'1 tablespoon'}, None, {'soy milk': '1', 'lemon juice':'1 tablespoon'}, None, None, None), 'Dairy and Egg Products'),
'chocolate milk' : Ingredient(Trans(None, None, 'dairy-free chocolate milk', None, 'soy milk', None, None, None), 'Dairy and Egg Products'),
'condensed' : Ingredient(Trans(None, None, 'condensed coconut milk', None, 'condensed coconut milk', None, None, None), 'Dairy and Egg Products'),
'evaporated' : Ingredient(Trans(None, None, 'condensed coconut milk', None, 'condensed coconut milk', None, None, None), 'Dairy and Egg Products')}

##Poultry products
transformdict['chicken'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Poultry Products')
transformdict['duck'] = Ingredient(Trans('mock duck', None, 'mock duck', None, None, None, None, None), 'Poultry Products')
transformdict['goose'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Poultry Products')
transformdict['pheasant'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Poultry Products')
transformdict['quail'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Poultry Products')
transformdict['turkey'] = Ingredient(Trans('tofu', None, 'tofu', None, None, None, None, None), 'Poultry Products')

##Sausages and Luncheon Meats// add healthy
transformdict['bologna'] = Ingredient(Trans('meatless bologna', None, 'meatless bologna', None, None, None, None, None), 'Sausages and Luncheon Meats')
transformdict['bratwurst'] = Ingredient(Trans('vegan beer brats', None, 'vegan beer brats', None, None, None, None, None), 'Sausages and Luncheon Meats')
transformdict['frankfurter'] = Ingredient(Trans('vegan beer brats', None, 'vegan beer brats', None, None, None, None, None), 'Sausages and Luncheon Meats')
#transformdict['ham'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Sausages and Luncheon Meats')
transformdict['salami'] = Ingredient(Trans('vegan veggie salami slices', None, 'vegan veggie salami slices', None, None, None, None, None), 'Sausages and Luncheon Meats')
transformdict['sausage'] = Ingredient(Trans('tofurky sausage', None, 'tofurky sausage', None, None, None, None, None), 'Sausages and Luncheon Meats')
transformdict['turkey breast'] = Ingredient(Trans('tofurky deli slices', None, 'tofurky deli slices', None, None, None, None, None), 'Sausages and Luncheon Meats')

##Pork Products
transformdict['pork'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Pork Products')
transformdict['ham'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Pork Products')

##Beef Products
transformdict['beef'] = Ingredient(Trans('tempah', None, 'tempah', None, 'lean beef', None, None, None), 'Beef Products')

##Finfish and Shellfish Products
transformdict['fish'] = Ingredient(Trans('tofu', None, 'tofu', None, None, None, None, None), 'Finfish and Shellfish Products')
transformdict['crustaceans'] = {'crab': Ingredient(Trans('jackfruit', None, 'jackfruit', None, None, None, None, None), 'Finfish and Shellfish Products'),
'crayfish': Ingredient(Trans('tofu', None, 'tofu', None, None, None, None, None), 'Finfish and Shellfish Products'),
'lobster': Ingredient(Trans('lobster mushrooms', None, 'lobster mushrooms', None, None, None, None, None), 'Finfish and Shellfish Products'),
'shrimp': Ingredient(Trans('tofu', None, 'tofu', None, None, None, None, None), 'Finfish and Shellfish Products')}
transformdict['mollusks'] = Ingredient(Trans('king oyster mushrooms', None, 'king oyster mushrooms', None, None, None, None, None), 'Finfish and Shellfish Products')
transformdict['salmon'] = Ingredient(Trans('tofu', None, 'tofu', None, None, None, None, None), 'Finfish and Shellfish Products')

##Lamb, Veal, and Game Products
transformdict['lamb'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Lamb, Veal, and Game Products')
transformdict['veal'] = Ingredient(Trans('seitan', None, 'seitan', None, None, None, None, None), 'Lamb, Veal, and Game Products')

#Fats and Oils  ##COMPLETE
transformdict['shortening'] = Ingredient(Trans('vegetable shortening', None, 'vegetable shortening', None, 'vegetable shortening', None, None, None), 'Fats and Oils')
transformdict['oil'] = Ingredient(Trans(None, None, None, None, 'canola oil', 'palm oil', None, None), 'Fats and Oils')
transformdict['margarine'] = Ingredient(Trans(None, None, None, None, None, 'softened butter', None, None), 'Fats and Oils')
transformdict['fat'] = Ingredient(Trans('remove', None, 'remove', None, None, 'remove', None, None), 'Fats and Oils')
transformdict['fish oil'] = Ingredient(Trans(None, None, 'canola oil', None, 'canola oil', None, None, None), 'Fats and Oils')
transformdict['margarine-like'] = Ingredient(Trans(None, None, None, None, None, 'butter', None, None), 'Fats and Oils')
transformdict['mayonnaise'] = Ingredient(Trans(None, None, 'Whole Foods’ Vegan Mayo', None, None, 'remove', None, None), 'Fats and Oils')

###Spices and Herbs ## to Mexican only


#Soups, Sauces, and Gravies
#vegan options in this category
transformdict['v2Soups, Sauces, and Gravies'] = Ingredient(Trans(None, None, None, None, 'low-sodium+', 'high-sodium+' , None, None), 'v2Soups, Sauces, and Gravies')
#vegetarian options
transformdict['v1Soups, Sauces, and Gravies'] = Ingredient(Trans(None, '+with beef', 'vegan vegetable soup', None, 'low-sodium+', 'high-sodium+' , None, None), 'v1Soups, Sauces, and Gravies')
#meat broths
transformdict['Broth'] = Ingredient(Trans('vegetable broth', None, 'vegetable broth', None, 'low-sodium+', 'high-sodium+' , None, None), 'Soups, Sauces, and Gravies')
transformdict['Gravy'] = Ingredient(Trans('remove', None, 'remove', None, 'remove', 'beef gravy' , None, None), 'Soups, Sauces, and Gravies')
transformdict['Soup'] = Ingredient(Trans('vegetable soup', None, 'vegetable soup', None, 'low-sodium+', 'high-sodium+' , None, None), 'Soups, Sauces, and Gravies')


#Fruits and Fruit Juices are okay? maybe append fresh for healthy?
transformdict['Fruits and Fruit Juices'] = Ingredient(Trans(None, None, None, None, 'fresh+' , 'canned+' , None, None), 'Fruits and Fruit Juices')
transformdict['Juices'] = Ingredient(Trans(None, None, None, None, 'fresh+' , 'canned+' , None, None), 'Fruits and Fruit Juices')
#Vegetables and Vegetable Products okay? maybe for unhealthy add meat? or sauces?

#Nut and Seed Products are okay?

#Beverages
transformdict['carbonated beverage'] = Ingredient(Trans(None, None, None, None, 'remove', None, None, None), 'Beverages')


##add rule if original recipe has ingredients with "meatless", "vegan", "vegetarian" remove to make unvegetarian/unvegan
#Legumes and Legume Products okay?
transformdict['peanut butter'] = Ingredient(Trans(None, None, None, None, 'almond butter', None, None, None), 'Legumes and Legume Products')
transformdict['tofu'] = Ingredient(Trans(None, 'beef', None, 'beef', None, 'beef', None, None), 'Legumes and Legume Products')

#Cereal Grains and Pasta
transformdict['flour'] = Ingredient(Trans(None, None, None, None, 'whole wheat flour', 'white flour', None, None), 'Cereal Grains and Pasta')
transformdict['rice'] = Ingredient(Trans(None, None, None, None, 'brown rice', 'white rice', None, None), 'Cereal Grains and Pasta')
transformdict['wheat flour'] = Ingredient(Trans(None, None, None, None, 'whole wheat flour', 'white flour', None, None), 'Cereal Grains and Pasta')
transformdict['wheat flour'] = Ingredient(Trans(None, None, None, None, 'quinoa pasta', 'white flour', None, None), 'Cereal Grains and Pasta')

#Baked Products/// for these add an append vegan function?
transformdict['baked products'] = Ingredient(Trans(None, None, 'vegan+', None, 'sugar-free+', None, None, None), 'Baked Products')

#Sweets- for healthy reduce them by ratio, for unhealthy increase them
transformdict['sweets'] = Ingredient(Trans(None, None, None, None, .8 , 1.2 , None, None), 'Sweets')
transformdict['honey'] = Ingredient(Trans(None, None, None, None, .8 , 1.2 , None, None), 'Sweets')

#Snacks- for healthy reduce them by ratio, for unhealthy increase them
transformdict['snacks'] = Ingredient(Trans(None, None, None, None, .8 , 1.2 , None, None), 'Snacks')

#Breakfast Cereals ^^
transformdict['breakfast cereals'] = Ingredient(Trans(None, None, None, None, .8 , 1.2 , None, None), 'Breakfast Cereals')

def makeBakedProductsVegan(name):
   return 'vegan' + name

# determine the type of an ingredient
def getIngredientType(ingredient):
   df = pd.read_csv('FOOD_DES.csv')
   filteredDF = df[df['Shrt_Desc'].str.contains(ingredient, case=False)]
   return filteredDF['FdGrp_Cd'].value_counts().idxmax()


# generate formatted ingredient name
def generateIngredientName(desc):
   desc = desc.lower()
   name = desc.split(',')
   name = name[0:2]
   name = name[::-1]
   name = ' '.join(name)
   return name.strip()

#dictionary of subsitution steps
transinstructions['margarine'] = TransSteps(True, None)
transinstructions['softened butter'] = TransSteps(True, None)
transinstructions['tofu'] = TransSteps(True, None)
transinstructions['Tofutti Milk Free Better Than Sour Cream'] = TransSteps(True, None)
transinstructions['non-dairy almond milk whipped cream'] = TransSteps(True, None)
transinstructions['tofu'] = TransSteps(True, None)
transinstructions['tofu'] = TransSteps(True, None)
transinstructions['cream substitute'] = TransSteps(True, None) ##change


if __name__ == "__main__":
   a = getIngredientType("chicken")
   print(a)
   desc = "Cheese, cottage, lowfat, 1% milkfat"
   n = generateIngredientName(desc)
   print(n)




###Spices and Herbs ## to Mexican only
transformdict['herbs'] = Ingredient(Trans(None, None, None, None, None, None, ["garlic", "oregano", "cilantro", "epazote"], None), 'Spices and Herbs')
transformdict['spices'] = Ingredient(Trans(None, None, None, None, None, None, ["cumin", "chile powder", "adobo seasoning", "chipotle chile powder"], None), 'Spices and Herbs')



