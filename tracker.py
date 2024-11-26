import argparse
from datetime import datetime


class Tracker:
    def __init__(self, id, date, description, amount):
        self.id = id
        self.date = date
        self.description = description
        self.amount = amount

    def __str__(self):
        return f"ID: {self.id}, Date: {self.date.strftime('%Y-%m-%d')}, Description: {self.description}, Amount: {self.amount}"


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

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    parser.add_argument("command", choices=["add"], help="Command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the command")

    args = parser.parse_args()
    command = args.command

    if command == "add":
        if len(args.args) != 3:
            print("Usage: add <date> <description> <amount>")
            return
        add(*args.args)

if __name__ == "__main__":
    main()
