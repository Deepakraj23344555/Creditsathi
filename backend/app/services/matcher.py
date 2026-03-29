class LenderMatchEngine:
    """
    Connects credit-ready MSMEs with eligible financial institutions 
    based on risk appetite and revenue thresholds.
    """

    # --- MOCK LENDER DATABASE ---
    # In production, this data is fetched from the SQLite/PostgreSQL 'lenders' table.
    LENDERS_DB = [
        {
            "lender_id": 1,
            "lender_name": "SBI SME Finance",
            "lender_type": "Bank",
            "min_credit_score": 700,
            "min_annual_turnover": 5000000.00, # ₹50 Lakhs
            "max_loan_amount": 20000000.00,    # ₹2 Crores
            "interest_rate_range": "9% - 11%"
        },
        {
            "lender_id": 2,
            "lender_name": "Bajaj Finserv",
            "lender_type": "NBFC",
            "min_credit_score": 650,
            "min_annual_turnover": 2000000.00, # ₹20 Lakhs
            "max_loan_amount": 5000000.00,     # ₹50 Lakhs
            "interest_rate_range": "12% - 15%"
        },
        {
            "lender_id": 3,
            "lender_name": "Lendingkart",
            "lender_type": "Fintech",
            "min_credit_score": 550,
            "min_annual_turnover": 1000000.00, # ₹10 Lakhs
            "max_loan_amount": 2000000.00,     # ₹20 Lakhs
            "interest_rate_range": "15% - 18%"
        },
        {
            "lender_id": 4,
            "lender_name": "HDFC Growth Fund",
            "lender_type": "Bank",
            "min_credit_score": 750,
            "min_annual_turnover": 10000000.00, # ₹1 Crore
            "max_loan_amount": 50000000.00,     # ₹5 Crores
            "interest_rate_range": "8.5% - 10.5%"
        }
    ]

    @classmethod
    def find_eligible_lenders(cls, user_score: int, monthly_revenue: float) -> list:
        """
        Filters the lender database against the MSME's profile.
        """
        eligible_matches = []
        annual_revenue = monthly_revenue * 12 # Annualize the parsed monthly revenue

        for lender in cls.LENDERS_DB:
            # The core matching logic
            score_qualifies = user_score >= lender["min_credit_score"]
            revenue_qualifies = annual_revenue >= lender["min_annual_turnover"]

            if score_qualifies and revenue_qualifies:
                # We only return the specific data the frontend needs to display
                eligible_matches.append({
                    "lender_name": lender["lender_name"],
                    "lender_type": lender["lender_type"],
                    "max_loan_amount": lender["max_loan_amount"],
                    "interest_rate_range": lender["interest_rate_range"]
                })

        # Sort matches by lowest interest rate first (best for the MSME)
        # We parse the first number in the string (e.g., "9" from "9% - 11%") for sorting
        eligible_matches.sort(key=lambda x: float(x["interest_rate_range"].split('%')[0]))

        return eligible_matches
