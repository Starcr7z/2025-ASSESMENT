from tabulate import tabulate

# -------------------- Constants and Unit Conversions --------------------

UNIT_CONVERSIONS = {
    'g': 1, 'gram': 1, 'grams': 1,
    'kg': 1000, 'kilogram': 1000, 'kilograms': 1000,
    'ml': 1, 'milliliter': 1, 'milliliters': 1,
    'l': 1000, 'liter': 1000, 'litre': 1000, 'liters': 1000, 'litres': 1000,
    'tbsp': 15, 'tablespoon': 15, 'tablespoons': 15,
    'tsp': 5, 'teaspoon': 5, 'teaspoons': 5,
    'unit': 1, 'units': 1, 'count': 1, 'piece': 1, 'pieces': 1
}


# -------------------- Functions --------------------

def make_statement(statement, decoration):
    print(f"{decoration * 3} {statement} {decoration * 3}\n")


def string_check(question, valid_answers=('yes', 'no'), num_letters=1):
    while True:
        response = input(question + " ").lower().strip()
        print()
        for item in valid_answers:
            if response == item or response == item[:num_letters]:
                return item
        print(f"Please choose an option from {valid_answers}\n")


def instructions():
    make_statement("Instructions", "ℹ️")
    print('''
This program calculates the total cost of a recipe.

For each ingredient, enter:
- Name
- Unit (e.g., g, ml, kg, unit)
- Amount used in the recipe
- Amount purchased and its cost (e.g., 1 kg for $4.00)

Valid units:
- Weight: g, kg
- Volume: ml, l
- Spoons: tbsp, tsp
- Counted items: unit, piece

Enter 'xxx' to stop adding ingredients.
''')


def convert_to_base(amount, unit):
    unit = unit.lower().strip()
    if unit in UNIT_CONVERSIONS:
        return amount * UNIT_CONVERSIONS[unit], unit
    return None, unit


def get_unit_input(prompt):
    while True:
        unit = input(prompt + " ").strip().lower()
        print()
        if unit in UNIT_CONVERSIONS:
            return unit
        print("❌ Unknown unit. Try g, ml, kg, l, tbsp, tsp, or unit.\n")


def get_amount_input(prompt):
    while True:
        response = input(prompt + " ").strip()
        print()
        try:
            value = float(eval(response))  # Supports fractions like 1/2
            if value > 0:
                return value
            print("❌ Amount must be greater than zero.\n")
        except:
            print("❌ Invalid number. Use digits or fractions like 1/2.\n")


def positive_int(prompt):
    while True:
        response = input(prompt + " ").strip()
        print()
        if response.isdigit() and int(response) >= 1:
            return int(response)
        print("❌ Enter a whole number (1 or more).\n")


def calculate_cost_with_units():
    total_cost = 0
    ingredient_list = []
    ingredient_num = 1

    while True:
        while True:
            ingredient = input(f"📝 Ingredient #{ingredient_num} name: ").strip()
            print()
            if ingredient.lower() == 'xxx' and ingredient_num == 1:
                print("❌ Oops - you have not entered anything. You need at least one ingredient.\n")
            elif ingredient.lower() == 'xxx':
                return total_cost, ingredient_list
            elif ingredient == "":
                print("❌ Ingredient name can't be blank. Please enter something.\n")
            else:
                break

        unit = get_unit_input(f"📐 Enter the unit for {ingredient} (e.g., g, ml, kg, tbsp, unit):")
        amount_used = get_amount_input(f"📏 Amount of {ingredient} used (in {unit}):")
        amount_purchased = get_amount_input(f"📦 Amount of {ingredient} purchased (in {unit}):")
        cost_purchased = get_amount_input(f"💵 Cost of purchased amount ($):")

        converted_used, _ = convert_to_base(amount_used, unit)
        converted_purchase, _ = convert_to_base(amount_purchased, unit)
        cost_used = (converted_used / converted_purchase) * cost_purchased
        cost_per_serving = 0  # Will calculate later

        total_cost += cost_used
        ingredient_list.append({
            "name": ingredient,
            "amount_used": f"{amount_used:.2f} {unit}",
            "total_cost": cost_used,
            "cost_per_serving": 0  # Will calculate later
        })

        ingredient_num += 1


def display_summary(recipe_name, servings, total_cost, ingredients):
    cost_per_serving = total_cost / servings if servings else 0
    print("\n" + "=" * 60)
    print(f"🍰 Recipe: {recipe_name}")
    print(f"👥 Servings: {servings}")
    print(f"💰 Total Cost: ${total_cost:.2f}")
    print(f"🧾 Cost per Serving: ${cost_per_serving:.2f}")
    print("=" * 60)

    for item in ingredients:
        item['cost_per_serving'] = item['total_cost'] / servings

    table_data = [
        [item["name"], item["amount_used"], f"${item['total_cost']:.2f}", f"${item['cost_per_serving']:.2f}"]
        for item in ingredients
    ]

    print(tabulate(
        table_data,
        headers=["Ingredient", "Amount Used", "Total Cost", "Cost/Serving"],
        tablefmt="fancy_grid"
    ))


# -------------------- Main Routine --------------------

make_statement("Recipe Cost Calculator", "💲")

if string_check("Do you want to see the instructions? ") == "yes":
    instructions()

while True:
    recipe_name = input("🍳 Enter the recipe name: ").strip()
    print()
    if recipe_name:
        break
    print("❌ Recipe name cannot be blank.\n")

servings = positive_int("🍽️ How many servings does this recipe make?")
print()

total_cost, ingredients = calculate_cost_with_units()
display_summary(recipe_name, servings, total_cost, ingredients)
