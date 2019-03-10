import parser
import pprint
#import ingredientlist
#import fooddict


##
class Recipe:
    def __init__(self, title, ingredients, ingredient_components, directions, direction_components, tools, main_cooking_method):
        self.title = title
        self.ingredient_names = ingredients
        self.ingredient_components = ingredient_components
        self.directions = directions
        self.direction_components = direction_components
        self.tools = tools
        self.main_cooking_method = main_cooking_method

    def print_recipe(self, detailed=False):
        print("Title:", self.title)

        print("\nIngredients:")
        for ingredient in self.ingredient_components:
            print(ingredient["original"])
            if detailed:
                print("\t> Ingredient:", ingredient["name"])
                print("\t> Quantity:", ingredient["quantity"])
                print("\t> Unit:", ingredient["unit"])

                description = None
                if ingredient["description"]:
                    description = ingredient["description"]
                elif ingredient["prep"]:
                    description = ingredient["prep"]
                print("\t> Description:", description, "\n")

        print("\nDirections:")
        for idx, direction in enumerate(self.direction_components):
            print(str(idx+1) + ". " + direction["direction"])
            if detailed:
                print("\t> Ingredients:", ", ".join(direction["ingredients"]))
                print("\t> Tools:", ", ".join(direction["tools"]))
                print("\t> Methods:", ", ".join(direction["methods"]))
                if direction["time"]:
                    print("\t> Time:", ", ".join(direction["time"]), "\n")
                else:
                    print("\t> Time:", None, "\n")

        print("\nTools:", ", ".join(self.tools))

        print("\nMain cooking method:", self.main_cooking_method, "\n")


if __name__ == '__main__':
    r = parser.parse_recipe("https://www.allrecipes.com/recipe/26655")
    r.print_recipe()
    a = 1
