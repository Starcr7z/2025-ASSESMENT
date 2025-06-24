# --- Recipe Name and Servings Input (Validation Test Section) ---

def get_positive_int(prompt):
    while True:
        response = input(prompt + " ").strip()
        print()

        if response == "":
            print("❌ This can't be blank, please try again.\n")
            continue

        # Check if response is a whole number (integer only)
        try:
            # Check if it's a float first (e.g. 12.5)
            if '.' in response:
                float_value = float(response)
                print("❌ Please enter a whole number.\n")
                continue

            value = int(response)

            if value < 0:
                print("❌ Please enter a positive number.\n")
            elif value == 0:
                print("❌ Please enter an integer greater than 0.\n")
            else:
                return value

        except ValueError:
            print("❌ Please enter a valid integer.\n")

# Loop for multiple test entries
for i in range(5):
    # Get recipe name (must not be blank)
    while True:
        recipe_name = input("🍳 Enter the recipe name: ").strip()
        print()
        if recipe_name:
            break
        print("❌ This can't be blank, please try again.\n")

    # Get servings (must be a positive integer)
    servings = get_positive_int("🍽️ How many servings does this recipe make?")

    # Print result
    print(f"✅ {recipe_name} makes {servings} servings.\n")
