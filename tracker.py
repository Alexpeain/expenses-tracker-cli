import argparse
from datetime import datetime
import os
import pandas as pd

#define csv file
tracker_csv = 'tracker.csv'

#load csv file
def load_expenses():
    if os.path.exists(tracker_csv):
        return pd.read_csv(tracker_csv)
    else:
        return pd.DataFrame(columns=['ID', 'Date', 'Description', 'Amount'])
#save expense
def save_expenses(expenses):
    expenses.to_csv(tracker_csv,index= False)
                                     
                                     

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


expense_tracker = []
next_id = 1

def add(date_str, description, amount):
    global next_id
    # Convert date string to datetime object
    date = datetime.strptime(date_str, "%Y-%m-%d")
    # Create a new expense
    exp = Tracker(next_id, date, description, float(amount))
    expense_tracker.append(exp)
    print(f"Expense added successfully (ID: {exp.id})")
    next_id += 1

    #convert to DataFrame and save
    expenses_df = pd.DataFrame([e.to_dict() for e in expense_tracker])
    save_expenses(expenses_df)

def list():
    expenses = load_expenses()
    if expenses.empty:
        print("No expenses found.")
    else:
        print("\nID  Date       Description  Amount")
        for _, row in expenses.iterrows():
            print(f"{row['ID']: <3} {row['Date']} {row['Description']: <12} ${row['Amount']:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    parser.add_argument("command", choices=["add","list"], help="Command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the command")

    args = parser.parse_args()
    expenses = load_expenses()
    command = args.command

    if command == "add":
        if len(args.args) != 3:
            print("Usage: add <date> <description> <amount>")
            return
        add(*args.args)
    elif command == "list":
        list()

if __name__ == "__main__":
    main()
