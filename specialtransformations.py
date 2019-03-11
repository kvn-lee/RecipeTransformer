class TransSteps:
   ##keep refers to merely replacing ingredient names, not removing original instructions
   ##ie replacing margarine with butter
   ##steps- if keep is True steps can be added for example to add additional steps (like mixing the two
   # ingredients that replace one). If keep is false this is used to replace original steps
   def __init__(self, acceptedactions, steps):
       self.acceptedactions = acceptedactions
       self.steps = steps

transinstructions = {}

#dictionary of subsitution steps
transinstructions['veganeggsub'] = TransSteps(True, "mix ")
transinstructions['buttermilksub'] = TransSteps(True, None)
transinstructions['seitan'] = TransSteps(True, None)
transinstructions['mock duck'] = TransSteps(True, None)
transinstructions['tofu'] = TransSteps(True, None)
transinstructions['tempah'] = TransSteps(True, None)
transinstructions['jackfruit'] = TransSteps(True, None)
transinstructions['lobster mushrooms'] = TransSteps(True, None)
transinstructions['king oyster mushrooms'] = TransSteps(True, None)


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