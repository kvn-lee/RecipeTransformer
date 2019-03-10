import parser
import sys

prompt = ("Please enter a number for how to change your recipe:"
          "\n1: To vegetarian"
          "\n2. From vegetarian"
          "\n3: To vegan"
          "\n4: From vegan"
          "\n5: To healthy"
          "\n6: From Healthy"
          "\n7: To Mexican"
          "\n8: From Mexican\n")


def main():
    url = ""
    while "allrecipes.com/recipe" not in url:
        url = input("\nPlease enter a valid recipe URL from allrecipes.com: ")

    # RETURN ORIGINAL RECIPE #
    recipe = parser.parse_recipe(url)
    output_recipe(recipe)

    # ASK HOW TO CHANGE RECIPE #
    transformation = 0
    while True:
        while int(transformation) not in range(1, 9):
            transformation = input(prompt)

        # TRANSFORM RECIPE #

        # OUTPUT THE NEW RECIPE POST TRANSFORMATION #

        # RESET TRANSFORMATION TO 0 TO REPEAT PROCESS #
        transformation = 0


def output_recipe(rec):
    detailed_recipe = input("View detailed recipe? (y/n): ")
    if detailed_recipe is "y":
        detailed = True
    elif detailed_recipe is "n":
        detailed = False

    if detailed:
        rec.print_recipe(detailed=True)
    else:
        rec.print_recipe()


if __name__ == '__main__':
    main()
