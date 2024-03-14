from expense import Expense
import calendar
import datetime


def main():
    print(f"Running expense tracker!")
    expense_file_path = "expense.csv"
    budget = 200

    # Get users input for expense.
    expense = get_user_expense()


    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expense.
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print(f"Getting user expense")
    expense_name = input("Enter expense name: ")
    print(f"You have entered {expense_name}")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍛food", "🏠home", "💰work", "🤸🏻fun", "🎀misc" 
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories): 
            print(f" {i+1}. {category_name}")
        
        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) -1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category. Please try again!")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing user expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            expense_name, expense_category, expense_amount = stripped_line.split(",")
            line_expense = Expense(name=expense_name, category=expense_category, amount=float(expense_amount))
            print(line_expense)

            expenses.append(line_expense)
        print(expenses)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category 
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount


    print("Expenses by Categories: ")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"You have spent ${total_spent:.2f} this month!")

    remaining_budget = budget - total_spent
    print(f"You have left only ${total_spent:.2f} this month!")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(pink(f"Budget per day: ${daily_budget:.2f}"))

def pink(text):
    return f"\033[92m{text}\033[95m"

if __name__ == "__main__": 
    main()