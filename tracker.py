import argparse
from datetime import datetime
import os
import pandas as pd

# Define CSV file
tracker_csv = 'tracker.csv'

# Load existing expenses from CSV
def load_expenses():
    if os.path.exists(tracker_csv):
        return pd.read_csv(tracker_csv)
    else:
        return pd.DataFrame(columns=['ID', 'Date', 'Description', 'Amount','Category'])

# Save expenses to CSV
def save_expenses(expenses):
    expenses.to_csv(tracker_csv, index=False)

# Load the next ID based on existing expenses
def load_next_id(expenses):
    if not expenses.empty:
        return expenses['ID'].max() + 1
    return 1

class Tracker:
    def __init__(self, id, date, description, amount,category):
        self.id = id
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

    def to_dict(self):
        return {
            'ID': self.id,
            'Date': self.date.strftime("%Y-%m-%d"),
            'Description': self.description,
            'Amount': self.amount,
            'Category': self.category,
        }

def add(description, amount,category):
    global next_id
    # Load existing expenses to get the current state
    expenses = load_expenses()

    # Set the current date
    date = datetime.now()

    # Convert amount to float
    try:
        amount = float(amount)
    except ValueError:
        print("Error: Amount must be a number.")
        return

    # Create a new expense
    exp = Tracker(next_id, date, description, amount, category)
    
    # Convert the new expense to a DataFrame
    new_expense_df = pd.DataFrame([exp.to_dict()])

    # Concatenate the new expense with the existing expenses
    expenses = pd.concat([expenses, new_expense_df], ignore_index=True)

    # Save updated expenses to CSV
    save_expenses(expenses)

    print(f"Expense added successfully (ID: {exp.id})")
    next_id += 1  # Increment the ID for the next expense
    
def update_expenses(id, new_description=None, new_amount=None ,new_category =None):
    expenses = load_expenses()
    if expenses.empty:
        print("No expenses found.")
        return 0

    if id not in expenses['ID'].values:
        print(f"No expense found with ID: {id}")
        return 0

    #accessing the entire data using loc base on ID column
    if new_description:
        expenses.loc[expenses['ID'] == id, 'Description'] = new_description
    if new_amount is not None:
        expenses.loc[expenses['ID'] == id, 'Amount'] = new_amount
    if new_category:
        expenses.loc[expenses['ID'] == id, 'Category'] = new_category

    save_expenses(expenses)
    
    print(f"Expense updated successfully (ID: {id})")
    return 1
        
def list_expenses():
    expenses = load_expenses()
    if expenses.empty:
        print("No expenses found.")
    else:
        print("\nID  Date       Description  Amount  Category")
        for _, row in expenses.iterrows():
            print(f"{row['ID']: <3} {row['Date']} {row['Description']: <12} ${row['Amount']:.2f} {row['Category']}")


def summary_expenses():
    expenses = load_expenses()
    if expenses.empty:
        print("No expense found")
        return 0
    
    total = expenses['Amount'].sum()
    print(f"Total expenses: ${total:.2f}")
    return total

#summary of expenses for a specific month
def summary_expenses_month(month):
    expenses = load_expenses()
    if expenses.empty:
        print("No expense found")
        return 0

    expenses['Date'] = pd.to_datetime(expenses['Date'])

    filtered_expenses = expenses[expenses['Date'].dt.month == month]
    

    # Calculate the total amount for the filtered expenses
    total = filtered_expenses['Amount'].sum()

    # Month name mapping
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    if total > 0:
        print(f"Total expenses for {month_names[month - 1]}: ${total:.2f}")
    else:
        print(f"No expenses found for {month_names[month - 1]}.")
    
    return total

def delete_expenses(id):
    expenses = load_expenses()
    
    if expenses.empty:
        print("No expenses found.")
        return 0

    # Check if the ID exists in the DataFrame
    if id not in expenses['ID'].values:
        print(f"No expense found with ID: {id}")
        return 0

    # Remove the expense with the given ID
    expenses = expenses[expenses['ID'] != id]
    save_expenses(expenses)
    
    print(f"Expense deleted successfully (ID: {id})")
    return 1
def view_category_expenses(category):
    expenses = load_expenses()
    filtered_expenses = expenses[expenses['Category'] == category ]
    if filtered_expenses.empty:
        print(f"No expenses found in category: {category}.")
    else:
        print(filtered_expenses)
        
def main():
    global next_id  # Declare next_id as global to modify it
    expenses = load_expenses()  # Load existing expenses
    next_id = load_next_id(expenses)  # Set next_id based on existing expenses

    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add command-specific arguments
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument("--description", required=True, help="Description of the expense")
    add_parser.add_argument("--amount", required=True, type=float, help="Amount of the expense")
    add_parser.add_argument("--category", required=True, help="Category of the expense")
    # List command does not have additional arguments
    subparsers.add_parser('list')

    # Summary Command does not have additional arguments
    summary_parser = subparsers.add_parser('summary')

     # Summary command with month only
    summary_month_parser = subparsers.add_parser('summary_month', help="Get summary of expenses for a specific month")
    summary_month_parser.add_argument("--month", required=True, type=int, help="Month to filter expenses (1-12)")
    
    #delete Command
    delete_parser = subparsers.add_parser('delete', help="Delete an expense by ID")
    delete_parser.add_argument("--id", required=True, type=int, help="ID of the expense to delete")

    #update command
    update_parser = subparsers.add_parser('update',help = "Update an expense by ID")
    update_parser.add_argument("--id", required =True, type = int ,help = "ID of the expense to update")
    update_parser.add_argument("--description", required=False, help="New description of the expense")
    update_parser.add_argument("--amount", required=False, type=float, help="New amount of the expense")

    #category command
    category_parser = subparsers.add_parser('category',help ="View Category ")
    category_parser.add_argument("--name", required=True, help="Name of the category to view expenses for")

    
    args = parser.parse_args()

    if args.command == "add":
        try:
            add(args.description, args.amount,args.category)
        except ValueError:
            print("Error: Please enter a valid number for the amount.")
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary_expenses()
    elif args.command == "summary_month":
        try:
            summary_expenses_month(args.month)
        except ValueError:
                print("Error: Please enter a valid number for the month.")
    elif args.command == "delete":
        try:
            delete_expenses(args.id)
        except ValueError:
                print("Error: Please enter a valid number for the ID.")
    elif args.command == "update":
        # Check if ID is provided
        if args.id is None:
            try:
                args.id = int(input("Please enter the ID of the expense to update: "))
            except ValueError:
                print("Invalid ID entered. Please enter a valid number.")
                return
        update_expenses(args.id, args.description, args.amount)
    elif args.command == "category":
        view_category_expenses(args.name)


if __name__ == "__main__":
    main()
