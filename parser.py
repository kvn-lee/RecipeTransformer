import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import regex


def parseIngredients(soup):
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


def parseDirections(soup):
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
        original_ingredient = ingredient
        ingredient = re.sub(r'\([^)]*\)', '', ingredient)
        quantity = next(iter(regex.num.findall(ingredient)), None)
        unit = next(iter(regex.units.findall(ingredient)), None)
        preparation = next(iter(regex.prep.findall(ingredient)), None)

        ing_name = ""
        if quantity is None:
            ing_name = ingredient
        elif unit is None:
            ing_name = ingredient.split(quantity, 1)[1]
        elif unit is not None:
            ing_name = ingredient.split(unit, 1)[1]
        if preparation and preparation in ing_name and ing_name.startswith(preparation):
            ing_name = ing_name.split(preparation, 1)[1]

        ing_name = ing_name.lstrip().rstrip()
        ing_name = ing_name.replace(" - ", ",")
        ing_name = ing_name.replace(" to ", ", to ")
        ing_name = ing_name.replace(" for ", ", for ")
        ing_name, sep, description = ing_name.partition(",")
        description = description.lstrip()
        ingredient_components[original_ingredient] = {"quantity": quantity,
                                                      "unit": unit,
                                                      "name": ing_name,
                                                      "description": description,
                                                      "prep": preparation}

    print(ingredient_components)
    return ingredient_components


def parseRecipe(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    dish = soup.find(id="recipe-main-content").get_text()
    print("Parsing the directions necessary for " + dish)

    ing = parseIngredients(soup)
    directions = parseDirections(soup)

    return dish, ing, directions


if __name__ == "__main__":
    title, ing, directions = parseRecipe("https://www.allrecipes.com/recipe/12719")
    components = getIngredientComponents(ing)
