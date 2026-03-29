class InsightEngine:
    
    # 1. THE RULE BOOK (The Dictionary)
    # This stores the "threshold" (the passing grade) and the advice for each factor.
    RULES = {
        "cash_flow_stability": {
            "threshold": 595, # 70% of 850
            "category": "Cash Flow Volatility",
            "observation": "Your daily bank balance fluctuates significantly.",
            "action_plan_90_days": "Maintain a minimum end-of-day balance of ₹50,000 to stabilize."
        },
        "debt_coverage": {
            "threshold": 595,
            "category": "High Debt Burden",
            "observation": "A high percentage of revenue is consumed by existing EMIs.",
            "action_plan_90_days": "Halt new borrowing. Clear highest-interest loans first."
        },
        "gst_compliance": {
            "threshold": 680, 
            "category": "Tax Compliance",
            "observation": "There are gaps in your GST filing history.",
            "action_plan_90_days": "Reconcile past quarter filings and automate future ones."
        },
        "digital_footprint": {
            "threshold": 510, 
            "category": "Digital Presence",
            "observation": "Limited digital transaction history.",
            "action_plan_90_days": "Shift 30% of B2B transactions to UPI/NEFT."
        },
        "business_vintage": {
            "threshold": 425, 
            "category": "Operational Vintage",
            "observation": "Your business is relatively young.",
            "action_plan_90_days": "Maintain a flawless 90-day streak of zero cheque bounces."
        }
    }

    # 2. THE ENGINE (The Action)
    @classmethod
    def generate(cls, breakdown: dict) -> list:
        insights_generated = []

        # Step A: Sort the factors from lowest score to highest
        sorted_factors = sorted(breakdown.items(), key=lambda item: item[1])

        # Step B: Check the worst scores against our Rule Book
        for factor_name, score in sorted_factors:
            rule = cls.RULES.get(factor_name) # Look up the rule for this factor
            
            # If the score is lower than the passing grade, add the advice!
            if rule and score < rule["threshold"]:
                insights_generated.append({
                    "category": rule["category"],
                    "observation": rule["observation"],
                    "action_plan_90_days": rule["action_plan_90_days"]
                })
            
            # Step C: Stop once we have 3 pieces of advice
            if len(insights_generated) == 3:
                break

        # Fallback: What if they have a perfect score and trigger zero rules?
        if not insights_generated:
            insights_generated.append({
                "category": "Optimal Health",
                "observation": "Your financial metrics are outstanding.",
                "action_plan_90_days": "Leverage your high score to negotiate sub-10% interest rates."
            })

        return insights_generated
