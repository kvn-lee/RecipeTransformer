import requests
from bs4 import BeautifulSoup
import re
import reciperegex
from Recipe import Recipe


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

    return items


def parse_directions(soup):
    pg_list = soup.find(class_="list-numbers recipe-directions__list")
    dir_list = pg_list.find_all(class_="step")

    steps = []

    for step in dir_list:
        step_text = str(step.find(class_="recipe-directions__list--item").get_text())
        individual_steps = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', step_text)
        individual_steps = [s.strip() for s in individual_steps]
        steps.extend(individual_steps)

    return steps


def get_ingredient_components(ingredients):
    ingredient_components = []
    for ingredient in ingredients:
        if "salt and " in ingredient:
            ingredient, _, other = ingredient.partition(" and ")
            ingredients.append(other)
        original_ingredient = ingredient
        ingredient = re.sub(r'\([^)]*\)', '', ingredient)
        quantity = next(iter(regex.num.findall(ingredient)), None)
        unit = next(iter(regex.units.findall(ingredient)), None)
        preparation = next(iter(regex.prep.findall(ingredient)), None)

        ing_name = ""
        if quantity is None:
            ing_name = ingredient
        elif unit is None:
            ing_name = ingredient.split(quantity, 1)[1].strip()
        elif unit is not None:
            ing_name = ingredient.split(unit, 1)[1].strip()
        if preparation and preparation in ing_name and ing_name.startswith(preparation):
            ing_name = ing_name.split(preparation, 1)[1]
            ing_name = ing_name.strip()
        if ing_name.startswith(", "):
            ing_name = ing_name.replace(", ", "", 1)

        ing_name = ing_name.strip()
        ing_name = ing_name.replace(" - ", ",")
        ing_name = ing_name.replace(" to ", ", to ")
        ing_name = ing_name.replace(" for ", ", for ")
        ing_name = ing_name.replace(" to taste", "")
        ing_name, sep, description = ing_name.partition(",")

        additional_prep = next(iter(regex.prep.findall(ing_name)), None)
        if additional_prep:
            ing_name = ing_name.replace(additional_prep, "")
            ing_name = ing_name.strip()
        
        if ing_name.endswith("s"):
            ing_name = ing_name.replace("s", "")

        description = description.strip()
        if preparation is not None and additional_prep is not None and description == "":
            description = ", ".join([preparation, additional_prep])
        elif description == "" and additional_prep is None:
            description = None
        elif description == "" and additional_prep is not None:
            description = additional_prep
        elif description != "" and additional_prep is not None:
            description = ", ".join([description, additional_prep])

        ing_props = {
            "original": original_ingredient,
            "quantity": quantity,
            "unit": unit,
            "name": ing_name,
            "description": description,
            "prep": preparation
             }
        ingredient_components.append(ing_props)

    return ingredient_components


def get_direction_components(directions, ingredients):
    direction_components = []
    for dir in directions:
        time = []
        methods = []
        tools = []
        dir_ingredients = []

        duration = regex.time.findall(dir)
        if duration:
            if isinstance(duration, list):
                time.extend(duration)
            else:
                time.append(duration)

        cooking_methods = regex.cook.findall(dir)
        if cooking_methods:
            if isinstance(cooking_methods, list):
                methods.extend(cooking_methods)
            else:
                methods.append(cooking_methods)

        cooking_tools = regex.tools.findall(dir)
        if cooking_tools:
            if isinstance(cooking_tools, list):
                tools.extend(cooking_tools)
            else:
                tools.append(cooking_tools)

        for ing in ingredients:
            ing_search = re.search(ing, dir)
            if ing_search:
                dir_ingredients.append(ing)
                continue
            for word in ing.split():
                if " " + word in dir:
                    dir_ingredients.append(ing)
                    break

        dir_ingredients = list(set(map(str.lower, dir_ingredients)))
        methods = list(set(map(str.lower, methods)))
        tools = list(set(map(str.lower, tools)))

        if "stir" in tools:
            tools = [tool.replace("stir", "wooden spoon") for tool in tools]

        dir_components = {
            "direction": dir, "ingredients": dir_ingredients, "methods": methods,
            "tools": tools, "time": time
            }
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

    title = soup.find(id="recipe-main-content").get_text()
    print("Parsing the directions necessary for", title, "\n")

    ingredients = parse_ingredients(soup)
    directions = parse_directions(soup)

    ingredient_components = get_ingredient_components(ingredients)
    ing_names = [d['name'] for d in ingredient_components if 'name' in d]
    direction_components = get_direction_components(directions, ing_names)
    tool_lists = [d['tools'] for d in direction_components if 'tools' in d]
    tools = [tool for tlist in tool_lists for tool in tlist]
    tools = list(set(tools))
    main_cooking_method = parse_cooking_method(title, directions).lower()

    return Recipe(title, ingredients, ingredient_components, directions, direction_components, tools, main_cooking_method)


if __name__ == "__main__":
    b = get_ingredient_components(["1 pound andouille sausage, sliced"])
    #title, ing, ing_c, directions, dir_c, main_method = parse_recipe("https://www.allrecipes.com/recipe/12719")
    a = 1