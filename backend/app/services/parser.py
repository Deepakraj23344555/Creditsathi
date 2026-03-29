import pandas as pd
import pdfplumber
import io
import numpy as np

class BankStatementParser:
    """
    Handles the extraction and financial aggregation of MSME bank statements.
    Designed to process both structured (CSV) and semi-structured (PDF) files.
    """
    
    @staticmethod
    def parse_csv(file_bytes: bytes) -> pd.DataFrame:
        """Reads a CSV file into a Pandas DataFrame."""
        return pd.read_csv(io.BytesIO(file_bytes))

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> pd.DataFrame:
        """
        Extracts tables from a PDF using pdfplumber.
        Note: Real-world PDFs vary wildly. This targets a standard grid format.
        """
        all_rows = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    all_rows.extend(table)
                    
        if not all_rows:
            raise ValueError("Could not extract tabular data from the PDF.")
            
        # Assuming the first row is the header: Date, Description, Credit, Debit, Balance
        df = pd.DataFrame(all_rows[1:], columns=all_rows[0])
        
        # Clean string currency values to floats
        for col in ["Credit", "Debit", "Balance"]:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('₹', '').replace(['', 'None'], '0').astype(float)
            
        return df

    @classmethod
    def extract_financials(cls, file_bytes: bytes, filename: str) -> dict:
        """
        Orchestrates the parsing and calculates the core metrics required 
        for the Credit Readiness Score (CRS).
        """
        try:
            if filename.endswith('.csv'):
                df = cls.parse_csv(file_bytes)
            elif filename.endswith('.pdf'):
                df = cls.parse_pdf(file_bytes)
            else:
                raise ValueError("Unsupported file format.")

            # Ensure Date column is datetime type
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M')

            # 1. Calculate Average Bank Balance
            avg_balance = df['Balance'].mean()

            # 2. Aggregate monthly inflows (Credits)
            monthly_inflows = df.groupby('Month')['Credit'].sum()
            avg_monthly_revenue = monthly_inflows.mean()

            # 3. Calculate Cash Flow Volatility (Coefficient of Variation)
            # Standard Deviation of inflows / Mean of inflows
            std_dev_inflows = monthly_inflows.std()
            
            if avg_monthly_revenue > 0 and not np.isnan(std_dev_inflows):
                volatility_index = (std_dev_inflows / avg_monthly_revenue) * 100
            else:
                volatility_index = 0.0 # Fallback for flat or empty statements

            # 4. Calculate approximate monthly debt obligations (assumes steady, identical debit patterns)
            # For this MVP, we will assume 15% of avg outlflow represents fixed obligations 
            avg_monthly_outflow = df.groupby('Month')['Debit'].sum().mean()
            estimated_emi = avg_monthly_outflow * 0.15

            return {
                "status": "success",
                "monthly_revenue": round(avg_monthly_revenue, 2),
                "avg_bank_balance": round(avg_balance, 2),
                "cash_flow_volatility_pct": round(volatility_index, 2),
                "estimated_monthly_emi": round(estimated_emi, 2)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
