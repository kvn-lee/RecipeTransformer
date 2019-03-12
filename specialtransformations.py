class TransSteps:
   ##keep refers to merely replacing ingredient names, not removing original instructions
   ##ie replacing margarine with butter
   ##steps- if keep is True steps can be added for example to add additional steps (like mixing the two
   # ingredients that replace one). If keep is false this is used to replace original steps
   def __init__(self, ingredients, replacesteps, addsteps):
       self.ingredients= ingredients
       self.replacesteps = replacesteps
       self.addsteps = addsteps

class ingsubs:
    def __init__(self, measurement, unit, name):
        self.measurement = measurement
        self.unit = unit
        self.name = name

specialtrans = {}

#dictionary of subsitution steps
specialtrans['veganeggsub'] = TransSteps([ingsubs(.25, 'cups', 'water'), ingsubs(.25, 'cups', 'chickpea flour')], None, "Whisk together water and chickpea flour until somewhat firm.")
specialtrans['buttermilksub'] = TransSteps([ingsubs(1, 'cups', 'soy milk'), ingsubs(1, 'tablespoons', 'lemon juice')], None, "Mix lemon juice and soy milk, let sit for a minute.")
'''
specialtrans['seitan'] = TransSteps(True, None)
specialtrans['mock duck'] = TransSteps(True, None)
specialtrans['tofu'] = TransSteps(True, None)
specialtrans['tempah'] = TransSteps(True, None)
specialtrans['jackfruit'] = TransSteps(True, None)
specialtrans['lobster mushrooms'] = TransSteps(True, None)
specialtrans['king oyster mushrooms'] = TransSteps(True, None)
'''

cooking_actions = [
    "bake", "boil", "fry",
    "deep fry", "sauté",
    "saute", "stir-fry", "grill",
    "roast", "simmer", "steam",
    "stew", "smoke", "deep fried",
    "broil", "fried", "cook",
    "melt", "drain", "stir",
    "whisk", "chop", "marinate", 
    "soak", "mix", "season"
    ]