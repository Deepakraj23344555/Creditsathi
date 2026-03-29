import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="CreditSaathi MSME Intelligence", page_icon="📈", layout="wide")
API_URL = "http://localhost:8000/api/v1" # Pointing to our local FastAPI backend

# --- SESSION STATE MANAGEMENT ---
# This ensures data isn't lost when we click between tabs
if "report_data" not in st.session_state:
    st.session_state.report_data = None

# --- UI COMPONENTS (PLOTLY) ---
def plot_gauge_chart(score):
    """Creates a professional gauge chart for the 0-850 score."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Readiness Score (CRS)", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 850], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 550], 'color': '#ff4b4b'},    # Red (Poor)
                {'range': [550, 650], 'color': '#ffa800'},  # Yellow (Fair)
                {'range': [650, 750], 'color': '#00d26a'},  # Green (Good)
                {'range': [750, 850], 'color': '#00833e'}   # Dark Green (Excellent)
            ]
        }
    ))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- MAIN APP NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2942/2942821.png", width=60) # Placeholder logo
st.sidebar.title("CreditSaathi")
st.sidebar.write("MSME Credit Intelligence Platform")
page = st.sidebar.radio("Navigation", ["1. Upload Data", "2. Score Dashboard", "3. AI Insights", "4. Lender Matches"])

st.sidebar.markdown("---")
st.sidebar.info("Powered by GST & Alternate Data Analytics")

# ==========================================
# PAGE 1: DATA UPLOAD
# ==========================================
if page == "1. Upload Data":
    st.title("Step 1: MSME Data Ingestion")
    st.write("Upload bank statements and provide basic business details to generate a comprehensive credit profile.")
    
    with st.form("upload_form"):
        col1, col2 = st.columns(2)
        with col1:
            business_name = st.text_input("Business Name", placeholder="e.g., Sharma Manufacturing Works")
            gstin = st.text_input("GSTIN", placeholder="15-digit alphanumeric")
        with col2:
            industry = st.selectbox("Industry Type", ["Manufacturing", "Retail", "Services", "Technology", "Logistics"])
            vintage = st.number_input("Business Vintage (Years)", min_value=0.0, max_value=50.0, value=2.5, step=0.5)
            
        uploaded_file = st.file_uploader("Upload 6-Month Bank Statement (PDF/CSV)", type=['pdf', 'csv'])
        
        submit_button = st.form_submit_button("Generate Credit Intelligence Report 🚀")
        
        if submit_button:
            if not business_name or not gstin or not uploaded_file:
                st.error("Please fill all fields and upload a statement.")
            else:
                with st.spinner("Parsing statements, running scoring engine, and finding matches..."):
                    # We send the data to our FastAPI backend
                    payload = {
                        "business_name": business_name,
                        "gstin": gstin,
                        "vintage_years": vintage,
                        "industry_type": industry
                    }
                    try:
                        response = requests.post(f"{API_URL}/get-report", json=payload)
                        if response.status_code == 200:
                            st.session_state.report_data = response.json()
                            st.success("Analysis Complete! Navigate to the Dashboard to view results.")
                        else:
                            st.error(f"Backend Error: {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to backend. Is your FastAPI server running?")

# ==========================================
# PAGE 2: SCORE DASHBOARD
# ==========================================
elif page == "2. Score Dashboard":
    st.title("Step 2: Credit Readiness Dashboard")
    
    if not st.session_state.report_data:
        st.warning("Please upload data in Step 1 first.")
    else:
        data = st.session_state.report_data["score_data"]
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(plot_gauge_chart(data["total_score"]), use_container_width=True)
            st.markdown(f"**Risk Tier:** `{data['risk_tier']}`")
            
        with col2:
            st.subheader("Factor Breakdown (0-850)")
            breakdown = data["breakdown"]
            # Convert dictionary to DataFrame for easy Plotly bar chart rendering
            df_factors = pd.DataFrame(list(breakdown.items()), columns=['Factor', 'Score'])
            df_factors['Factor'] = df_factors['Factor'].str.replace('_', ' ').str.title()
            
            fig = go.Figure(go.Bar(
                x=df_factors['Score'],
                y=df_factors['Factor'],
                orientation='h',
                marker=dict(color='#0068c9')
            ))
            fig.update_layout(xaxis=dict(range=[0, 850]), height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 3: AI INSIGHTS
# ==========================================
elif page == "3. AI Insights":
    st.title("Step 3: 90-Day Action Plan")
    
    if not st.session_state.report_data:
        st.warning("Please upload data in Step 1 first.")
    else:
        insights = st.session_state.report_data["insights"]
        st.write("Based on our algorithmic analysis, here are the targeted areas for improvement:")
        
        for idx, insight in enumerate(insights):
            with st.expander(f"⚠️ Area {idx+1}: {insight['category']}", expanded=True):
                st.markdown(f"**Observation:** {insight['observation']}")
                st.info(f"**Action Plan:** {insight['action_plan_90_days']}")

# ==========================================
# PAGE 4: LENDER MATCHES
# ==========================================
elif page == "4. Lender Matches":
    st.title("Step 4: Eligible Lenders")
    
    if not st.session_state.report_data:
        st.warning("Please upload data in Step 1 first.")
    else:
        matches = st.session_state.report_data["eligible_lenders"]
        
        if not matches:
            st.error("Your current Credit Readiness Score is too low for our marketplace partners. Please follow the 90-Day Action plan and re-evaluate.")
        else:
            st.success(f"We found {len(matches)} institutional lenders matching your profile!")
            
            # Display beautifully formatted metric cards for each lender
            for match in matches:
                with st.container():
                    st.markdown(f"### 🏦 {match['lender_name']} ({match['lender_type']})")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Est. Interest Rate", match["interest_rate_range"])
                    col2.metric("Max Loan Amount", f"₹ {match['max_loan_amount']:,.2f}")
                    col3.button(f"Apply to {match['lender_name']}", key=match['lender_name'])
                    st.markdown("---")
