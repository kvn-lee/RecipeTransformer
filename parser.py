import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

num = re.compile(r"(?x)(?:(?:\d+\s*)? \d+\/\d+|\d+(?:\.\d+)? )")
unit_words = ["teaspoon", "tablespoon", "fluid ounce", "gill", "cup", "quart", "pint", "gallon", "milliliter",
              "liter", "deciliter", "pound", "pack", "pinch", "dash", "ounce", "package", "container", "tub", "can",
              "stalk"]
units = re.compile("|".join(r"\b{}s?\b".format(u) for u in unit_words), re.I)


def parseIngredients(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    dish = soup.find(id="recipe-main-content").get_text()
    print("Parsing the ingredients necessary for " + dish)

    page_list1 = soup.find(id="lst_ingredients_1")
    page_list2 = soup.find(id="lst_ingredients_2")
    check_list1 = page_list1.find_all(class_="checkList__line")
    check_list2 = page_list2.find_all(class_="checkList__line")

    items = []

    for item1 in check_list1:
        items.append(
            str(item1.find(class_="recipe-ingred_txt added").get_text()))
    for item2 in check_list2:
        temp = item2.find(class_="recipe-ingred_txt added")
        if temp:
            items.append(
                str(item2.find(class_="recipe-ingred_txt added").get_text()))

    print(items)
    return items


def parseDirections(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    dish = soup.find(id="recipe-main-content").get_text()
    print("Parsing the directions necessary for " + dish)

    pg_list = soup.find(class_="list-numbers recipe-directions__list")
    dir_list = pg_list.find_all(class_="step")

    steps = []

    for step in dir_list:
        steps.append(
            str(step.find(class_="recipe-directions__list--item").get_text().rstrip()))

    print(steps)
    return steps


def getIngredientComponents(ingredients):
    ingredient_components = {}
    for ingredient in ingredients:
        quantity = next(iter(num.findall(ingredient)), None)
        unit = next(iter(units.findall(ingredient)), None)
        ing_name = ""
        if quantity is None:
            ing_name = ingredient
        elif unit is None:
            ing_name = ingredient.split(quantity, 1)[1]
        elif unit is not None:
            ing_name = ingredient.split(unit, 1)[1]
        ing_name = ing_name.lstrip().rstrip()
        ing_name = ing_name.replace(" - ", ",")
        ing_name, sep, description = ing_name.partition(",")
        description = description.lstrip()
        ingredient_components[ingredient] = {"quantity": quantity,
                                             "unit": unit,
                                             "name": ing_name,
                                             "description": description}
    print(ingredient_components)
    return ingredient_components


if __name__ == "__main__":
    items = parseIngredients("https://www.allrecipes.com/recipe/12719/new-orleans-shrimp/?internalSource=rotd&referringContentType=Homepage&clickId=cardslot%201")
    steps = parseDirections("https://www.allrecipes.com/recipe/12719/new-orleans-shrimp/?internalSource=rotd&referringContentType=Homepage&clickId=cardslot%201")
<<<<<<< HEAD
    components = getIngredientComponents(items)
=======
    components = getIngredientComponents(items)
>>>>>>> efb09e8b0cb0bd217227cec6a7bd8b65f4a2af12
