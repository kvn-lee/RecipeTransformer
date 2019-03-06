import pandas as pd

class Ingredient:
    def __init__(self, trans, categoryName):
        self.trans = trans
        self.categoryName = categoryName


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

##Sausages and Luncheon Meats
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



#templateop= Ingredient(Trans(None, None, None, None, None, None, None, None), 'j')


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
    return name.lstrip()

if __name__ == "__main__":
    a = getIngredientType("chicken")
    print(a)
    desc = "Cheese, cottage, lowfat, 1% milkfat"
    n = generateIngredientName(desc)
    print(n)