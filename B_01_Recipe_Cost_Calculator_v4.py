from tabulate import tabulate

# -------------------- Constants and Unit Conversions --------------------

# Base unit conversions:
# All weights to grams, all volumes to milliliters, spoons to milliliters, counted items to 1:1
UNIT_CONVERSIONS = {
    'g': 1, 'gram': 1, 'grams': 1,
    'kg': 1000, 'kilogram': 1000, 'kilograms': 1000,
    'ml': 1, 'milliliter': 1, 'milliliters': 1,
    'l': 1000, 'liter': 1000, 'litre': 1000, 'liters': 1000, 'litres': 1000,
    'tbsp': 15, 'tablespoon': 15, 'tablespoons': 15,
    'tsp': 5, 'teaspoon': 5, 'teaspoons': 5,
    'unit': 1, 'units': 1, 'count': 1, 'piece': 1, 'pieces': 1
}

# Group units into categories to ensure logical conversions
WEIGHT_UNITS = {'g', 'gram', 'grams', 'kg', 'kilogram', 'kilograms'}
VOLUME_UNITS = {'ml', 'milliliter', 'milliliters', 'l', 'liter', 'litre', 'liters', 'litres'}
SPOON_UNITS = {'tbsp', 'tablespoon', 'tablespoons', 'tsp', 'teaspoon', 'teaspoons'}
COUNT_UNITS = {'unit', 'units', 'count', 'piece', 'pieces'}

# -------------------- Functions --------------------

def make_statement(statement, decoration):
    # """Prints a statement with decoration for headings"""
    print(f"{decoration * 3} {statement} {decoration * 3}\n")

def string_check(question, valid_answers=('yes', 'no'), num_letters=1):
    # Confirms a user input is a valid choice (yes/no by default)
    while True:
        response = input(question + " ").lower().strip()
        print()
        for item in valid_answers:
            if response == item or response == item[:num_letters]:
                return item
        print(f"Please choose an option from {valid_answers}\n")

def instructions():
    # """Shows instructions for the recipe cost calculator"""
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

    # Converts a given amount and unit to its base unit amount.
    # For example, 1 kg -> 1000 g

    unit = unit.lower().strip()
    if unit in UNIT_CONVERSIONS:
        return amount * UNIT_CONVERSIONS[unit], unit
    return None, unit  # Return None if unit is not recognized

def get_unit_input(prompt, valid_set=None):

    # Prompts user for a unit.
    # If valid_set is provided, only allows units in that category.

    while True:
        unit = input(prompt + " ").strip().lower()
        print()
        if unit in UNIT_CONVERSIONS:
            if valid_set and unit not in valid_set:
                # User picked valid unit, but wrong category → reject
                print(f"❌ Invalid unit for this context. Must be one of: {', '.join(sorted(valid_set))}\n")
                continue
            return unit
        print("❌ Unknown unit. Try g, ml, kg, l, tbsp, tsp, or unit.\n")

def get_unit_category(unit):

    # Returns the category set for a given unit.
    # Used to restrict purchased unit to same logical group.

    if unit in WEIGHT_UNITS:
        return WEIGHT_UNITS
    elif unit in VOLUME_UNITS:
        return VOLUME_UNITS
    elif unit in SPOON_UNITS:
        return SPOON_UNITS
    elif unit in COUNT_UNITS:
        return COUNT_UNITS
    else:
        return None

def get_amount_input(prompt):

    # Prompts user for a numeric input.
    # Supports fractions like 1/2 via eval().

    while True:
        response = input(prompt + " ").strip()
        print()
        try:
            value = float(eval(response))  # Allows fractions like 1/2
            if value > 0:
                return value
            print("❌ Amount must be greater than zero.\n")
        except:
            print("❌ Invalid number. Use numbers or fractions like 1/2.\n")

def positive_int(prompt):

    # Gets a positive whole number input (for servings).
    while True:
        response = input(prompt + " ").strip()
        print()
        if response.isdigit() and int(response) >= 1:
            return int(response)
        print("❌ Enter a whole number (1 or more).\n")

def calculate_cost_with_units():
#
# Main loop:
# - Get ingredient name
# - Get unit for used amount
# - Get unit for purchased amount (must match category)
# - Get amounts and cost
# - Convert to base units and calculate cost for portion used
# Stores all data in ingredient_list.
    total_cost = 0
    ingredient_list = []
    ingredient_num = 1

    while True:
        # Ingredient name
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

        # Get used unit
        used_unit = get_unit_input(f"📐 Enter the unit for {ingredient} used (e.g., g, kg, ml, tbsp, unit):")

        # Limit purchased unit to same category
        allowed_units = get_unit_category(used_unit)

        # Get purchased unit
        purchased_unit = get_unit_input(
            f"📐 Enter the unit for {ingredient} purchased (must match type):",
            valid_set=allowed_units
        )

        # Amounts and cost
        amount_used = get_amount_input(f"📏 Amount of {ingredient} used (in {used_unit}):")
        amount_purchased = get_amount_input(f"📦 Amount of {ingredient} purchased (in {purchased_unit}):")
        cost_purchased = get_amount_input(f"💵 Cost of purchased amount ($):")

        # Convert both to base units for fair comparison
        converted_used, _ = convert_to_base(amount_used, used_unit)
        converted_purchased, _ = convert_to_base(amount_purchased, purchased_unit)

        # Calculate cost for amount used
        cost_used = (converted_used / converted_purchased) * cost_purchased

        # Save info for summary table
        total_cost += cost_used
        ingredient_list.append({
            "name": ingredient,
            "amount_used": f"{amount_used:.2f} {used_unit}",
            "total_cost": cost_used,
            "cost_per_serving": 0  # Placeholder, updated later
        })

        ingredient_num += 1

def display_summary(recipe_name, servings, total_cost, ingredients):

    # Displays the final results:
    # - Recipe name, servings, total cost, cost per serving
    # - Table with ingredient name, amount used, total cost, cost per serving

    cost_per_serving = total_cost / servings if servings else 0

    print("\n" + "=" * 60)
    print(f"🍰 Recipe: {recipe_name}")
    print(f"👥 Servings: {servings}")
    print(f"💰 Total Cost: ${total_cost:.2f}")
    print(f"🧾 Cost per Serving: ${cost_per_serving:.2f}")
    print("=" * 60)

    # Update each ingredient's cost per serving
    for item in ingredients:
        item['cost_per_serving'] = item['total_cost'] / servings

    # Format data for table
    table_data = [
        [item["name"], item["amount_used"], f"${item['total_cost']:.2f}", f"${item['cost_per_serving']:.2f}"]
        for item in ingredients
    ]

    # Print formatted table with tabulate
    print(tabulate(
        table_data,
        headers=["Ingredient", "Amount Used", "Total Cost", "Cost/Serving"],
        tablefmt="fancy_grid"
    ))

# -------------------- Main Routine --------------------

# Display heading
make_statement("Recipe Cost Calculator", "💲")

# Ask user if they want instructions
if string_check("Do you want to see the instructions? ") == "yes":
    instructions()

# Get recipe name (cannot be blank)
while True:
    recipe_name = input("🍳 Enter the recipe name: ").strip()
    print()
    if recipe_name:
        break
    print("❌ Recipe name cannot be blank.\n")

# Get servings (must be whole number)
servings = positive_int("🍽️ How many servings does this recipe make?")
print()

# Run main ingredient loop
total_cost, ingredients = calculate_cost_with_units()

# Show final results
display_summary(recipe_name, servings, total_cost, ingredients)