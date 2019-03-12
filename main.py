import rparser
import recipetranslator
import copy

prompt = ("Please enter a number for how to change your recipe:"
          "\n1: To vegetarian"
          "\n2. From vegetarian"
          "\n3: To healthy"
          "\n4: From healthy"
          "\n5: To Vegan"
          "\n6: From Vegan"
          "\n7: To Mexican"
          "\n8: From Mexican\n")


def main():
    url = ""
    while "allrecipes.com/recipe" not in url:
        url = input("\nPlease enter a valid recipe URL from allrecipes.com: ")

    # RETURN ORIGINAL RECIPE #
    recipe = rparser.parse_recipe(url)
    output_recipe(recipe)


    # ASK HOW TO CHANGE RECIPE #
    transformation = 0
    toTransform = True
    while toTransform:
        while int(transformation) not in range(1, 9):
            transformation = input(prompt)

        # TRANSFORM RECIPE #
        newrecipe = recipetranslator.maintransformation(copy.deepcopy(recipe), int(transformation))

        # OUTPUT THE NEW RECIPE POST TRANSFORMATION #
        output_recipe(newrecipe)

        # RESET TRANSFORMATION TO 0 TO REPEAT PROCESS #
        transformation = 0
        toStop = 0
        while int(toStop) not in range(1, 3):
            toStop = input('Enter 1 to transform again, 2 to stop: ')
        if int(toStop) == 2:
            toTransform = False


def output_recipe(rec):
    detailed_recipe = ""
    while detailed_recipe not in ("y", "n", "Y", "N"):
        detailed_recipe = input("View detailed recipe? (y/n): ")
    if detailed_recipe is "y" or "Y":
        detailed = True
    elif detailed_recipe is "n" or "N":
        detailed = False

    if detailed:
        rec.print_recipe(detailed=True)
    else:
        rec.print_recipe()


if __name__ == '__main__':
    main()
