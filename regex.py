import re

# regex for integers and fractions
num = re.compile(r"(?x)(?:(?:\d+\s*)? \d+\/\d+|\d+(?:\.\d+)? )")


# generate regex for units of measurement
unit_words = [
    "teaspoon", "tablespoon", "fluid ounce",
    "gill", "cup", "quart",
    "pint", "gallon", "milliliter",
    "liter", "deciliter", "pound",
    "pack", "pinch", "dash",
    "ounce", "package", "container",
    "tub", "can", "stalk",
    "clove", "bunch"
    ]

units = re.compile("|".join(r"\b{}s?\b".format(u) for u in unit_words), re.I)


# generate regex for preparation words
prep_words = [
    "crushed", "minced", "diced",
    "cubed", "julienned", "stripped",
    "sliced", "cracked", "chopped",
    "prepared", "fresh", "grated",
    "skinless", "boneless", "shucked",
    "ground", "melted", "boned"
    ]

prep = re.compile("|".join(r"\b{}\b".format(p) for p in prep_words), re.I)


# generate regex for cooking actions
cooking_actions = [
    "bake", "boil", "fry",
    "deep fry", "sauté",
    "saute", "stir-fry", "grill",
    "roast", "simmer", "steam",
    "stew", "smoke", "deep fried",
    "broil", "fried", "cook",
    ]

cook = re.compile("|".join(r"\b{}i?e?d?\b".format(c) for c in cooking_actions), re.I)


# regex for time and time unit
time = re.compile(r"\d*[.,]?\d* minu?t?e?s?|\d*[.,]?\d* hours?")


if __name__ == '__main__':
    a = time.findall("2 hours")
    b = 1
