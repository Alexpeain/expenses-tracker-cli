# Expense Tracker-Cli

Build a simple expense tracker application to manage your finances. The application should allow users to add, delete, and view their expenses.

# CLI features

- Users can add an expense with a description and amount.
- Users can update an expense.
- Users can delete an expense.
- Users can view all expenses.
- Users can view a summary of all expenses.
- Users can view a summary of expenses for a specific month (of current year).
- Add expense categories and allow users to filter expenses by category.
- Allow users to export expenses to a CSV file.

## Add Category

```bash
  python tracker.py add --description "Lunch" --amount 20 --category "Meal"
```

## Update

```bash
python tracker.py update --id 1 --description "Dinner" --amount 20.00
```

## Delete

```bash
python tracker.py delete --id <expense_id>
```

## List all expenses

```bash
  python tracker.py list
```

## Summary expenses

```bash
python tracker.py summary
```

## Summary Filter by month

```bash
python tracker.py summary_month --month 8
```

## Category Tags

```bash
python tracker.py category --name Meal
```

## export file

```bash
   python tracker.py export --filename "my_expenses.csv"
```

# Project URL

[Expense-tracker](https://roadmap.sh/projects/expense-tracker)
