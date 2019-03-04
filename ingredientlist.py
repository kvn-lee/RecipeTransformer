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

aproductop1= Ingredient(Trans(None, None, "almond milk", None, "almond milk", "cream", None, None), "animal product")
ingdict["milk"] = aproductop1

templateop= Ingredient(Trans(None, None, None, None, None, None, None, None), "j")




