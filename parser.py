import requests
from bs4 import BeautifulSoup
import re
import regex


def parse_ingredients(soup):
    page_list1 = soup.find(id="lst_ingredients_1")
    page_list2 = soup.find(id="lst_ingredients_2")
    check_list1 = page_list1.find_all(class_="checkList__line")
    check_list2 = page_list2.find_all(class_="checkList__line")

    items = []

    for item1 in check_list1:
        items.append(
            str(item1.find(class_="recipe-ingred_txt added").get_text().lower()))
    for item2 in check_list2:
        temp = item2.find(class_="recipe-ingred_txt added")
        if temp:
            items.append(
                str(item2.find(class_="recipe-ingred_txt added").get_text().lower()))

    print(items)
    return items


def parse_directions(soup):
    pg_list = soup.find(class_="list-numbers recipe-directions__list")
    dir_list = pg_list.find_all(class_="step")

    steps = []

    for step in dir_list:
        steps.append(
            str(step.find(class_="recipe-directions__list--item").get_text().rstrip().lower()))

    print(steps)
    return steps


def get_ingredient_components(ingredients):
    ingredient_components = []
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

        ing_name = ing_name.strip()
        ing_name = ing_name.replace(" - ", ",")
        ing_name = ing_name.replace(" to ", ", to ")
        ing_name = ing_name.replace(" for ", ", for ")
        ing_name, sep, description = ing_name.partition(",")
        description = description.strip()
        ing_props = {
            "original": original_ingredient,
            "quantity": quantity,
            "unit": unit,
            "name": ing_name,
            "description": description,
            "prep": preparation
             }
        ingredient_components.append(ing_props)

    print(ingredient_components)
    return ingredient_components


def get_direction_components(directions, ingredients):
    direction_components = []
    for dir in directions:
        time = []
        methods = []
        tools = []
        dir_ingredients = []
        #individual_directions = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', dir)

        duration = next(iter(regex.time.findall(dir)), None)
        if duration:
            if isinstance(duration, list):
                time.extend(duration)
            else:
                time.append(duration)

        cooking_methods = next(iter(regex.cook.findall(dir)), None)
        if cooking_methods:
            if isinstance(cooking_methods, list):
                methods.extend(cooking_methods)
            else:
                methods.append(cooking_methods)

        cooking_tools = next(iter(regex.tools.findall(dir)), None)
        if cooking_tools:
            if isinstance(cooking_tools, list):
                tools.extend(cooking_tools)
            else:
                tools.append(cooking_tools)

        for ing in ingredients:
            ing_search = re.search(ing, dir)
            if ing_search:
                dir_ingredients.append(ing)

        if "stir" in tools:
            tools = [tool.replace("stir", "wooden spoon") for tool in tools]

        dir_components = {"ingredients": dir_ingredients, "methods": methods, "tools": tools, "time": time}
        direction_components.append(dir_components)

    return direction_components


def parse_cooking_method(title, directions):
    potential_methods = {}
    title_cooking_method = next(iter(regex.cook.findall(title)), None)

    if title_cooking_method:
        if title_cooking_method.endswith("ed"):
            if title_cooking_method.endswith("fried"):
                return title_cooking_method.replace("fried", "fry")
            elif title_cooking_method == "baked":
                return "bake"
            else:
                return title_cooking_method.replace("ed", "")
        else:
            return title_cooking_method

    for idx, step in enumerate(directions):
        cooking_methods = regex.cook.findall(step)
        if cooking_methods:
            for method in cooking_methods:
                potential_methods[method] = idx

    if len(potential_methods) == 1:
        return next(iter(potential_methods))
    elif len(potential_methods) > 1:
        return max(potential_methods, key=potential_methods.get)
    else:
        return "cook (default)"


def parse_recipe(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    dish = soup.find(id="recipe-main-content").get_text()
    print("Parsing the directions necessary for " + dish)

    ing = parse_ingredients(soup)
    directions = parse_directions(soup)

    return dish.lower(), ing, directions


if __name__ == "__main__":
    title, ing, directions = parse_recipe("https://www.allrecipes.com/recipe/12719")
    ing_components = get_ingredient_components(ing)
    ing_names = [d['name'] for d in ing_components if 'name' in d]
    dir_components = get_direction_components(directions, ing_names)
    main_cooking_method = parse_cooking_method(title, directions)
    print(main_cooking_method)