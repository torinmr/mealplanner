import json
import sys

DEFAULT_NUM_SERVINGS = 2
INGREDIENTS_LOCATION = 'data/ingredients.json'
RECIPES_LOCATION = 'data/recipes.json'

def input_meal_plan():
    meal_plan = []
    day = 1
    while True:
        print('Input day %s meal plan.' % day)
        if day == 1:
            print('Day 1 should be the day you go shopping.')
        dish_num = 1
        while True:
            dish_name = input('Dish %s (enter to finish day %s): '
                              % (dish_num, day))
            if not dish_name:
                break
            else:
                dish = {'name': dish_name,
                        'day': day,
                        'servings': DEFAULT_NUM_SERVINGS}
                meal_plan.append(dish)
        more_days = ''
        while True:
            more_days = input('Any more days? (y/n) ')
            if more_days == 'y' or more_days == 'yes':
                break
            elif more_days == 'n' or more_days == 'no':
                break
        if more_days == 'n' or more_days == 'no':
            break
        else:
            day += 1
    return meal_plan


def generate_shopping_list(meal_plan):
    ingredients = None
    recipes = None
    with open(INGREDIENTS_LOCATION) as f:
        ingredients = json.load(f)
    with open(RECIPES_LOCATION) as f:
        recipes = json.load(f)

    shopping_list = {}
    warnings = []
    for meal in meal_plan:
        recipe_name = meal["name"]
        try:
            recipe = recipes[recipe_name]
        except KeyError:
            warnings.append("Couldn't find recipe %s, skipping." % recipe_name)
            continue

        for ingredient in recipe["ingredients_per_serving"]:
            ingredient_name = ingredient["name"]
            try:
                ingredient_info = ingredients[ingredient_name]
            except KeyError:
                warnings.append("Couldn't find ingredient %s, skipping."
                                % ingredient_name)
                continue

            ingredient_freshness = ingredient_info["freshness"]
            meal_day = meal["day"]
            if ingredient_freshness < meal_day:
                warnings.append("Ingredient %s is being used on day %s, "
                                "but it goes bad after %s days." %
                                (ingredient_name, meal_day,
                                 ingredient_freshness))

            amount = ingredient["amount"] * meal["servings"]
            ingredient_unit = ingredient["unit"]
            if ingredient_name in shopping_list:
                existing_info = shopping_list[ingredient_name]
                if existing_info["unit"] != ingredient_unit:
                    warnings.append("Units did not match for ingredient %s: "
                                    "%s vs %s, skipping." %
                                    (ingredient_name,
                                     existing_info["unit"],
                                     ingredient["unit"]));
                    continue
                existing_info["amount"] += amount
            else:
                shopping_list[ingredient_name] = {
                    "amount": amount,
                    "unit": ingredient_unit
                }
    return (shopping_list, warnings)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            meal_plan = json.load(f)
    else:
        meal_plan = input_meal_plan()
    print("Parsed meal plan:")
    print(json.dumps(meal_plan, indent=4))

    (shopping_list, warnings) = generate_shopping_list(meal_plan)
    print()
    print("Shopping list:")
    for (item_name, quantity) in shopping_list.items():
        print("%s %s %s" % (quantity["amount"], quantity["unit"], item_name))
    print()
    print("Warnings:")
    for warning in warnings:
        print(warning)
