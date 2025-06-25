# Input validation for recipe name and servings

def get_positive_int(prompt):
    while True:
        response = input(prompt).strip()
        if response == "":
            print("❌ This can't be blank, please try again.\n")
        elif response.isdigit():
            val = int(response)
            if val > 0:
                return val
            else:
                print("❌ Please enter an integer greater than 0.\n")
        else:
            print("❌ Please enter a valid integer.\n")


while True:
    recipe_name = input("Enter the recipe name: ").strip()
    if recipe_name:
        break
    print("❌ This can't be blank, please try again.\n")

servings = get_positive_int("How many servings does this recipe make? ")
print(f"{recipe_name} makes {servings} servings.")