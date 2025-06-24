# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""
    print(f"{decoration * 3} {statement} {decoration * 3}")


def string_check(question, valid_answers=('yes', 'no'),
                 num_letters=1):
    """Checks that users enter the full word
    or the 'n' letter/s of a word from a range of valid responses"""
    while True:
        response = input(question).lower()

        for item in valid_answers:
            # check if the response is the entire word
            if response == item:
                return item
            # check if it's the 'n' letters
            elif response == item[:num_letters]:
                return item

        print(f"Please choose an option from {valid_answers}")


def instructions():
    make_statement("Instructions", "ℹ️")

    print('''

This program helps you calculate the total cost of a recipe.

For each ingredient, enter:
- The name of the ingredient
- The amount required for the recipe (in grams, ml, or units)
- The amount purchased and its cost (e.g., 500g for $4.00)

The program will calculate the cost of the amount used
in the recipe, and at the end, it will total the cost
of all ingredients.

To stop adding ingredients, enter the exit code ('xxx') 
when prompted for the ingredient name.

    ''')


# Main routine goes here

make_statement("Recipe Cost Calculator", "💲")

print()
want_instructions = string_check("Do you want to see the instructions? ")

if want_instructions == "yes":
    instructions()

print()
print("Program continues...")
