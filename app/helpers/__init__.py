import csv
from typing import Dict, List


def read_csv(filename: str) -> List[Dict]:

    transactions = []

    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        next(reader, None)
        for row in reader:
            amount, transaction_type, *remaining = row
            transactions.append({
                "amount": amount,
                "transaction_type": transaction_type
            })

    return transactions
