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
        return pd.DataFrame(columns=['ID', 'Date', 'Description', 'Amount'])

# Save expenses to CSV
def save_expenses(expenses):
    expenses.to_csv(tracker_csv, index=False)

# Load the next ID based on existing expenses
def load_next_id(expenses):
    if not expenses.empty:
        return expenses['ID'].max() + 1
    return 1

class Tracker:
    def __init__(self, id, date, description, amount):
        self.id = id
        self.date = date
        self.description = description
        self.amount = amount

    def to_dict(self):
        return {
            'ID': self.id,
            'Date': self.date.strftime("%Y-%m-%d"),
            'Description': self.description,
            'Amount': self.amount
        }

def add(description, amount):
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
    exp = Tracker(next_id, date, description, amount)
    
    # Convert the new expense to a DataFrame
    new_expense_df = pd.DataFrame([exp.to_dict()])

    # Concatenate the new expense with the existing expenses
    expenses = pd.concat([expenses, new_expense_df], ignore_index=True)

    # Save updated expenses to CSV
    save_expenses(expenses)

    print(f"Expense added successfully (ID: {exp.id})")
    next_id += 1  # Increment the ID for the next expense

def list_expenses():
    expenses = load_expenses()
    if expenses.empty:
        print("No expenses found.")
    else:
        print("\nID  Date       Description  Amount")
        for _, row in expenses.iterrows():
            print(f"{row['ID']: <3} {row['Date']} {row['Description']: <12} ${row['Amount']:.2f}")

def summary_expenses():
    expenses = load_expenses()
    if expenses.empty:
        print("No expense found")
        return 0
    
    total = expenses['Amount'].sum()
    print(f"Total expenses: ${total:.2f}")
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

    # List command does not have additional arguments
    subparsers.add_parser('list')

    # Summary Command does not have additional arguments
    subparsers.add_parser('summary')

    #delete Command
    delete_parser = subparsers.add_parser('delete', help="Delete an expense by ID")
    delete_parser.add_argument("--id", required=True, type=int, help="ID of the expense to delete")

    
        

    args = parser.parse_args()

    if args.command == "add":
        add(args.description, args.amount)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary_expenses()
    elif args.command == "delete":
        delete_expenses(args.id)

if __name__ == "__main__":
    main()
