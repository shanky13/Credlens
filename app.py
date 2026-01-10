import streamlit as st
import pandas as pd
import altair as alt

# 1. SETUP & CONFIGURATION
st.set_page_config(
    page_title="CredLens | India's Smartest Card Tool",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTION: The "Indianizer" ---
def format_inr(number):
    """
    Converts 150000 -> ₹ 1,50,000
    """
    s, *d = str(int(number)).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    amount = "".join([r] + d)
    return f"₹ {amount}"

# 2. HERO SECTION
st.title("💳 CredLens")
st.markdown("### Maximize your rewards. Minimize your fees.")



# 3. SIDEBAR (DASHBOARD STYLE)
with st.sidebar:
    st.header("⚙️ Your Financial Profile")
    
    # --- INCOME SECTION ---
    with st.container():
        st.subheader("💰 Income")
        salary = st.number_input(
            "Monthly Net Salary", 
            value=50000, 
            step=5000,
            format="%d",  # Forces it to be a clean number (no decimals)
            help="Enter your take-home pay after taxes."
        )
        # THE FIX: Instant feedback below the input
        st.caption(f"Reading: **{format_inr(salary)}** / month")
        st.caption(f"Annual: **{format_inr(salary * 12)}** / year")

    st.divider()

  # --- SPENDS SECTION ---
    with st.container():
        st.subheader("💸 Monthly Spends")
        
        col1, col2 = st.columns(2)
        with col1:
            spend_online = st.number_input(
                "Online (₹)", 
                value=10000, 
                step=1000, 
                format="%d",
                help="Amazon, Flipkart, Myntra, Swiggy, Zomato, etc."  # <-- The Question Mark is back
            )
            st.caption(f"{format_inr(spend_online)}") 
            
            spend_travel = st.number_input(
                "Travel (₹)", 
                value=5000, 
                step=1000, 
                format="%d",
                help="Flights, Trains, Hotels, Uber/Ola, etc."         # <-- The Question Mark is back
            )
            st.caption(f"{format_inr(spend_travel)}") 

        with col2:
            spend_other = st.number_input(
                "Offline (₹)", 
                value=10000, 
                step=1000, 
                format="%d",
                help="Groceries, Supermarkets, Store Swipes, Utilities." # <-- The Question Mark is back
            )
            st.caption(f"{format_inr(spend_other)}") 
            
        # Total Summary Box
        total_monthly_spend = spend_online + spend_travel + spend_other
        st.info(f"Total Monthly Spend: **{format_inr(total_monthly_spend)}**")

    st.divider()
    wants_lounge = st.checkbox("✅ Must have Airport Lounge")


# 4. LOGIC ENGINE
@st.cache_data
def load_data():
    return pd.read_csv("cards.csv")

df = load_data()

def calculate_yield(row):
    annual_online = spend_online * 12
    annual_travel = spend_travel * 12
    annual_other = spend_other * 12
    
    # Reward Calculation
    raw_reward = (
        (annual_online * row['Online Rate'] / 100) +
        (annual_travel * row['Travel Rate'] / 100) +
        (annual_other * row['Base Rate'] / 100)
    )
    
    # Cap Logic (Annualized Cap)
    annual_cap = row['Monthly Cap'] * 12
    actual_reward = min(raw_reward, annual_cap)
    
    # Net Benefit
    return actual_reward - row['Fee']

df['Net Savings'] = df.apply(calculate_yield, axis=1)

# 5. FILTERING
valid_cards = df[df['Min Income'] <= salary].copy()
if wants_lounge:
    valid_cards = valid_cards[valid_cards['Lounge Access'] == 'Yes']
valid_cards = valid_cards.sort_values(by='Net Savings', ascending=False)

# 6. RESULTS DISPLAY
if not valid_cards.empty:
    best_card = valid_cards.iloc[0]
    
    # A. The Winner Banner (Cleaner UI)
    st.markdown("---")
    col_winner, col_stats = st.columns([2, 1])
    
    with col_winner:
        st.subheader("🏆 The Best Card for You")
        st.success(f"## {best_card['Card Name']}")
        st.write(f"Reward Type: **{best_card['Reward Type']}**")
        
    with col_stats:
        st.metric(
            label="Annual Net Savings", 
            value=format_inr(best_card['Net Savings']),
            delta="Profit"
        )

    # B. Visual Comparison
    st.subheader("📊 Profitability Comparison")
    
    # Create a cleaner chart data
    chart_data = valid_cards.head(5).copy()
    chart_data['Formatted Savings'] = chart_data['Net Savings'].apply(format_inr)
    
    chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10).encode(
        x=alt.X('Net Savings', title='Net Annual Value (₹)'),
        y=alt.Y('Card Name', sort='-x', title=None),
        color=alt.Color('Net Savings', scale=alt.Scale(scheme='greens'), legend=None),
        tooltip=['Card Name', 'Formatted Savings', 'Fee']
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)

    # C. Data Table (Formatted)
    with st.expander("🔍 See Detailed Breakdown"):
        # Format the table numbers before showing
        display_df = valid_cards[['Card Name', 'Fee', 'Net Savings', 'Lounge Access']].copy()
        display_df['Fee'] = display_df['Fee'].apply(format_inr)
        display_df['Net Savings'] = display_df['Net Savings'].apply(format_inr)
        
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True
        )

else:
    st.error("😕 No cards found. Try increasing your salary or unchecking 'Lounge Access'.")