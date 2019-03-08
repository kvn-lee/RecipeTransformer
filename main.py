def main():
    url = ""
    while "allrecipes.com/recipe" not in url:
        url = input("Please enter a valid recipe URL from allrecipes.com: ")

    # RETURN ORIGINAL RECIPE #

    # ASK HOW TO CHANGE RECIPE #

    transformation = 0
    while int(transformation) not in range(1, 4):
        transformation = input("Please enter a number for how to change your recipe:\n1: Vegetarian\n2: Vegan\n3: Healthy\n4: Mexican")

    # TRANSFORM RECIPE #

    # OUTPUT THE NEW RECIPE POST TRANSFORMATION #

if __name__ == "__main__":
    main()