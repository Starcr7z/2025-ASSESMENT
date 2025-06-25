# Version 3 - Ingredient entry and cost calculation added

def convert_to_base(amount, unit):
    if unit == "kg":
        return amount * 1000
    elif unit == "g":
        return amount
    elif unit == "unit":
        return amount
    else:
        return None

total_cost = 0
ingredient_num = 1

while True:
    ingredient = input(f"Ingredient #{ingredient_num} name: ").strip()
    if ingredient.lower() == "xxx":
        break

    used_amount = float(input(f"Amount of {ingredient} used: "))
    used_unit = input("Unit (g, kg, unit): ").lower()
    converted_used = convert_to_base(used_amount, used_unit)

    bought_amount = float(input("Amount purchased: "))
    bought_unit = input("Unit purchased (must match): ").lower()
    converted_bought = convert_to_base(bought_amount, bought_unit)

    if used_unit != bought_unit:
        print("❌ Units do not match.")
        continue

    price = float(input("Cost of purchased amount ($): "))
    cost = (converted_used / converted_bought) * price
    total_cost += cost

    print(f"{ingredient} cost: ${cost:.2f}\n")
    ingredient_num += 1

print(f"\nTotal recipe cost: ${total_cost:.2f}")