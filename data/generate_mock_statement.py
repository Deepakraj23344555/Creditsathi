import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_statement(filename="data/sample_statement.csv"):
    """Generates a realistic 6-month MSME bank statement."""
    dates = [datetime.now() - timedelta(days=x) for x in range(180)]
    dates.reverse()
    
    data = []
    balance = 50000.0 # Starting balance
    
    for date in dates:
        # Simulate daily operations
        if np.random.rand() > 0.6: # 40% chance of a transaction on any given day
            is_credit = np.random.rand() > 0.5
            amount = round(np.random.uniform(1000, 25000), 2)
            
            if is_credit:
                balance += amount
                data.append([date.strftime("%Y-%m-%d"), "Client Payment / Sales", amount, 0.0, balance])
            else:
                balance -= amount
                data.append([date.strftime("%Y-%m-%d"), "Vendor / Utility / EMI", 0.0, amount, balance])

    df = pd.DataFrame(data, columns=["Date", "Description", "Credit", "Debit", "Balance"])
    df.to_csv(filename, index=False)
    print(f"Sample statement generated at {filename}")

if __name__ == "__main__":
    generate_sample_statement()
