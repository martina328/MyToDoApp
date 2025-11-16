todo_list = []

# Loads the to-do list from a file
try:
    with open("todo_list.txt", "r") as file:
        for line in file:
            todo_list.append(line.strip())
except FileNotFoundError:
    print("No saved items found")

# Continues to loop and display menu until the user selects to exit the program
while True:
    print() # Adds two blank lines
    print()
    print("To-do list: ") # Prints the title of the list
    item_number = 1
    for todo in todo_list: # Loops through existing to-do items
        print(f"{item_number}: {todo}")
        item_number += 1

    # Prints the menu
    print() # Adds a blank line
    print("Actions:")
    print("A - Add to-do item")
    print("R - Remove to-do item") 
    print("X - Exit")
    choice = input("Enter your choice (A, R, or X): ")
    choice = choice.upper() # Converts the choice to uppercase

    # User selected 'a' or 'A' to add an item to the list
    if choice == "A":
        todo = input("Enter the to-do item: ") 
        todo_list.append(todo)
        continue  # Tells the program to go back to the start of the loop

    # User selected 'r' or 'R' to remove an item from the list
    if choice == "R":
        item_number = int(input("Enter the number of the item to remove: "))
        if item_number > 0 and item_number <= len(todo_list):
            todo_list.pop(item_number - 1)
        else:
            print("Invalid item number")
        continue
    

    # User selected 'x' or 'X' to exit the program
    if choice == "X":
        # Saves the to-do list to a file
        with open("todo_list.txt", "w") as file:
            for todo in todo_list:
                file.write(f"{todo}\n")
            break

    # User selected something else
    print("Invalid choice")