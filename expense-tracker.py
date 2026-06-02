import json
import os
from datetime import datetime

class ExpenseTracker:
    def _init_(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        """Load expenses from JSON file if it exists"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.expenses = json.load(file)
            except json.JSONDecodeError:
                print("[Warning] File was corrupted. Starting with an empty tracker.")
                self.expenses = []

    def save_expenses(self):
        """Save current expenses back to the JSON file"""
        with open(self.filename, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, amount, category, description):
        """Add a new expense with timestamp"""
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expense = {
            "amount": float(amount),
            "category": category.capitalize(),
            "description": description,
            "date": date_str
        }
        self.expenses.append(expense)
        self.save_expenses()
        print(f"\n[Success] Added expense of Rs. {amount} under '{category}' category!")

    def view_all_expenses(self):
        """Display all recorded expenses"""
        if not self.expenses:
            print("\n[Info] No expenses recorded yet.")
            return

        print("\n" + "="*65)
        print(f"{'Date & Time':<20} | {'Category':<15} | {'Amount (Rs.)':<12} | {'Description'}")
        print("="*65)
        for exp in self.expenses:
            print(f"{exp['date']:<20} | {exp['category']:<15} | {exp['amount']:<12.2f} | {exp['description']}")
        print("="*65)

    def view_summary(self):
        """Display total budget spent and category-wise breakdown"""
        if not self.expenses:
            print("\n[Info] No data available to generate summary.")
            return

        total = sum(exp['amount'] for exp in self.expenses)
        
        # Calculate category-wise breakdown
        category_totals = {}
        for exp in self.expenses:
            cat = exp['category']
            category_totals[cat] = category_totals.get(cat, 0) + exp['amount']

        print("\n" + "•"*15 + " EXPENSE SUMMARY " + "•"*15)
        print(f"Total Amount Spent: Rs. {total:.2f}")
        print("-"*47)
        print(f"{'Category':<20} | {'Amount Spent (Rs.)':<20}")
        print("-"*47)
        for cat, amt in category_totals.items():
            print(f"{cat:<20} | Rs. {amt:<17.2f}")
        print("•"*47)

def main():
    tracker = ExpenseTracker()

    while True:
        print("\n** Personal Expense Tracker **")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Expense Summary & Analytics")
        print("4. Exit Application")
        
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            try:
                amount = input("Enter Amount (Rs.): ").strip()
                if not amount or float(amount) <= 0:
                    print("[Error] Invalid amount. Please enter a positive number.")
                    continue
                
                category = input("Enter Category (e.g., Food, Rent, Travel): ").strip()
                if not category:
                    print("[Error] Category cannot be empty.")
                    continue
                    
                description = input("Enter Description/Notes: ").strip()
                if not description:
                    description = "N/A"

                tracker.add_expense(amount, category, description)
            except ValueError:
                print("[Error] Please enter a valid numerical value for amount.")

        elif choice == '2':
            tracker.view_all_expenses()

        elif choice == '3':
            tracker.view_summary()

        elif choice == '4':
            print("\nThank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("\n[Invalid Choice] Please enter a number between 1 and 4.")

if _name_ == "_main_":
    main()