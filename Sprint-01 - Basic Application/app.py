todo_list = []

# load the to-do list from a file
try:
    with open("todo_list.txt", "r") as file:
        for line in file:
            todo_list.append(line.strip())
except FileNotFoundError:
    print("No saved items found")

# continue to loop and display menu until the user selects to exit the program
while True:
    print() # add a couple of blank lines
    print()
    print("To-do list: ") # Print the title of the list
    item_number = 1
    for todo in todo_list: # Loop through existing to-do items
        print(f"{item_number}: {todo}")
        item_number += 1

    # Print the menu
    print() # add a blank line
    print("Actions:")
    print("A - Add to-do item")
    print("R - Remove to-do item") 
    print("X - Exit")
    choice = input("Enter your choice (A, R, or X): ")
    choice = choice.upper() # converts the choice to uppercase

    # user selected 'a' or 'A' to add an item to the list
    if choice == "A":
        todo = input("Enter the to-do item: ") 
        todo_list.append(todo)
        continue  # tells the program to go back to the start of the loop

    # user selected 'r' or 'R' to remove an item from the list
    if choice == "R":
        item_number = int(input("Enter the number of the item to remove: "))
        if item_number > 0 and item_number <= len(todo_list):
            todo_list.pop(item_number - 1)
        else:
            print("Invalid item number")
        continue
    

    # user selected 'x' or 'X' to exit the program
    # user selected 'x' or 'X' to exit the program
    if choice == "X":
        # save the to-do list to a file
        with open("todo_list.txt", "w") as file:
            for todo in todo_list:
                file.write(f"{todo}\n")
            break

    # user selected something else
    print("Invalid choice")