import random
import pandas as pd
from datetime import datetime, timedelta
import os

# Updated output folder path based on new project structure
output_folder = "/Users/rickglenn/Desktop/Warren/data/raw"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Parameters for data generation
categories_income = ["Sales", "Donations", "Sponsorship"]
categories_expense = [
    "Rent", "Payroll", "Utilities", "Loan Payments", "Insurance",
    "Office Supplies", "Marketing", "Inventory", "Taxes", "Travel",
    "Professional Services", "Maintenance", "Memberships"
]
transaction_types = ["Deposit", "Withdrawal"]

# Function to generate transactions for a given month
def generate_monthly_transactions(month, year, num_transactions=20, initial_balance=5000):
    transactions = []
    balance = initial_balance  # Starting balance for the month

    for _ in range(num_transactions):
        # Generate a random date within the month
        day = random.randint(1, 28)  # Simplify to avoid month-end issues
        date = datetime(year, month, day)

        # Randomly select transaction type
        transaction_type = random.choice(transaction_types)

        # Randomly select a category based on transaction type
        category = (
            random.choice(categories_income)
            if transaction_type == "Deposit"
            else random.choice(categories_expense)
        )

        # Generate a random amount
        amount = random.randint(100, 5000) if transaction_type == "Deposit" else random.randint(100, 3000)

        # Update balance
        if transaction_type == "Deposit":
            balance += amount
        else:
            balance -= amount

        # Append transaction details
        transactions.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Transaction Type": transaction_type,
            "Amount": amount,
            "Category": category,
            "Balance": max(balance, 0),  # Ensure non-negative balance
            "Description": f"{transaction_type} for {category}"
        })

    return transactions

# Function to generate data for a given time span
def generate_data(start_date, end_date, transactions_per_month=20, initial_balance=5000):
    transactions = []
    current_date = start_date

    while current_date <= end_date:
        monthly_transactions = generate_monthly_transactions(
            current_date.month, current_date.year, transactions_per_month, initial_balance
        )
        transactions.extend(monthly_transactions)
        # Move to the next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)

    return transactions

# Main script to generate datasets for 1-year, 5-year, and 10-year periods
if __name__ == "__main__":
    # Define time periods
    periods = {
        "1_year": (datetime(2023, 1, 1), datetime(2023, 12, 31)),
        "5_years": (datetime(2018, 1, 1), datetime(2023, 12, 31)),
        "10_years": (datetime(2013, 1, 1), datetime(2023, 12, 31))
    }

    # Generate and save datasets
    for period_name, (start_date, end_date) in periods.items():
        transactions = generate_data(start_date, end_date, transactions_per_month=30)
        df = pd.DataFrame(transactions)
        df.sort_values(by="Date", inplace=True)  # Sort by date

        # Save to CSV
        output_file_path = os.path.join(output_folder, f"mock_banking_data_{period_name}.csv")
        df.to_csv(output_file_path, index=False)
        print(f"Mock banking data ({period_name}) saved to '{output_file_path}'.")
