class CreditScoringEngine:
    """
    Core algorithm for the CreditSaathi MSME Credit Readiness Score (CRS).
    Calculates a transparent, weighted score from 0-850.
    """

    # --- WEIGHT DEFINITIONS ---
    WEIGHTS = {
        "cash_flow_stability": 0.30,
        "gst_compliance": 0.20,
        "debt_coverage": 0.20,
        "business_vintage": 0.15,
        "digital_footprint": 0.15
    }

    @staticmethod
    def _score_cash_flow(volatility_pct: float) -> float:
        """
        Maps volatility to a 0-100 score. 
        Lower volatility = Higher score.
        Assumes > 50% volatility is critically unstable (0 points).
        """
        if volatility_pct <= 0: return 100.0
        if volatility_pct >= 50.0: return 0.0
        # Linear degradation
        return 100.0 - (volatility_pct * 2)

    @staticmethod
    def _score_vintage(years: float) -> float:
        """
        Maps vintage to a 0-100 score.
        Caps at 5 years (a 5-year old business gets max points here).
        """
        if years >= 5.0: return 100.0
        return (years / 5.0) * 100

    @staticmethod
    def _score_debt_coverage(monthly_revenue: float, estimated_emi: float) -> float:
        """
        Calculates Fixed Obligation to Income Ratio (FOIR).
        FOIR > 60% is generally considered unlendable (0 points).
        """
        if monthly_revenue <= 0: return 0.0
        foir_pct = (estimated_emi / monthly_revenue) * 100
        
        if foir_pct <= 10.0: return 100.0
        if foir_pct >= 60.0: return 0.0
        
        # Linear degradation between 10% and 60% FOIR
        return 100.0 - ((foir_pct - 10) * 2)

    @staticmethod
    def _determine_risk_tier(total_score: int) -> str:
        """Categorizes the 0-850 score into standard risk tiers."""
        if total_score >= 750: return "Excellent (Low Risk)"
        if total_score >= 650: return "Good (Moderate Risk)"
        if total_score >= 550: return "Fair (Elevated Risk)"
        return "Poor (High Risk)"

    @classmethod
    def calculate_crs(cls, parsed_financials: dict, user_inputs: dict) -> dict:
        """
        The orchestrator method. Takes raw data, applies the math, 
        and returns the exact payload our API schema demands.
        """
        # 1. Extract inputs (handling simulated data for MVP)
        volatility = parsed_financials.get('cash_flow_volatility_pct', 0.0)
        revenue = parsed_financials.get('monthly_revenue', 0.0)
        emi = parsed_financials.get('estimated_monthly_emi', 0.0)
        
        vintage = user_inputs.get('vintage_years', 0.0)
        # For the MVP, we simulate GST and Digital metrics if they aren't provided by a live API
        gst_score = user_inputs.get('gst_compliance_score', 85.0) 
        digital_score = user_inputs.get('digital_footprint_score', 70.0)

        # 2. Calculate individual 0-100 factors
        factors = {
            "cash_flow_stability": cls._score_cash_flow(volatility),
            "business_vintage": cls._score_vintage(vintage),
            "debt_coverage": cls._score_debt_coverage(revenue, emi),
            "gst_compliance": min(max(gst_score, 0), 100), # Ensure bounds
            "digital_footprint": min(max(digital_score, 0), 100)
        }

        # 3. Apply weights
        weighted_sum = sum(factors[k] * cls.WEIGHTS[k] for k in factors)

        # 4. Scale to 0-850
        final_score = int(weighted_sum * 8.5)

        # 5. Scale factors to standard 850 metric for frontend visualization
        breakdown = {k: int(v * 8.5) for k, v in factors.items()}

        # 6. Generate Risk Flags based on critical thresholds
        risk_flags = []
        if factors['cash_flow_stability'] < 40:
            risk_flags.append("CRITICAL: High Cash Flow Volatility")
        if factors['debt_coverage'] < 50:
            risk_flags.append("WARNING: High Debt Burden (FOIR)")
        if factors['gst_compliance'] < 60:
            risk_flags.append("WARNING: Irregular GST Filing History")

        return {
            "total_score": final_score,
            "breakdown": breakdown,
            "risk_tier": cls._determine_risk_tier(final_score),
            "flags": risk_flags
        }
