import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, amount, category, sub_category, transaction_type):
        transaction = {
            'amount': amount,
            'category': category,
            'sub_category': sub_category,
            'type': transaction_type,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        self.transactions.append(transaction)

    def view_summary(self):
        summary = {}
        for transaction in self.transactions:
            month = transaction['date'][:7]
            if month not in summary:
                summary[month] = 0
            summary[month] += transaction['amount']
        return summary

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.transactions = json.load(file)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("File not found. Starting with empty data.")

def main():
    tracker = ExpenseTracker()

    while True:
        action = input("\nWould you like to add an income or expense? (type 'exit' to quit): ").strip().lower()

        if action == 'exit':
            break

        while action not in ['income', 'expenses']:
            print("Invalid input! Please type 'income' or 'expenses'.")
            action = input("Enter again (income/expense): ").strip().lower()

        # Validate amount
        while True:
            try:
                amount = float(input("Enter the amount: "))
                if amount <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid amount! Please enter a positive number.")

        # Validate category
        valid_categories = ['salary', 'business', 'food', 'rent', 'travel', 'other']
        category = input("Enter the category (Salary, Business, Food, Rent, Travel, Other): ").strip().lower()
        while category not in valid_categories:
            print("Invalid category! Choose from: Salary, Business, Food, Rent, Travel, Other.")
            category = input("Enter the category again: ").strip().lower()

        sub_category = input("Enter the sub-category: ").strip()

        tracker.add_transaction(amount, category, sub_category, action)
        print("Transaction added successfully!")

        print("\nCurrent Monthly Summary:", tracker.view_summary())

    
    filename = input("\nEnter filename to save transactions (e.g., data.json): ")
    tracker.save_to_file(filename)
    print("Data saved. Exiting program.")

if __name__ == "__main__":
    main()
