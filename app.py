import streamlit as st
import pandas as pd
import altair as alt

# 1. SETUP (Must be the first command)
st.set_page_config(
    page_title="CredLens | Maximize Your Credit Card Rewards",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            /* header {visibility: hidden;} */
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. HERO SECTION
st.title("💳 CredLens")
st.markdown("### Stop guessing. Start saving.")
st.markdown(
    """
    Most credit card "guides" are just paid ads. **CredLens is different.**
    We use **math**, not opinions, to find the card that actually pays you the most based on *your* spending habits.
    """
)

with st.expander("ℹ️ How does the math work?"):
    st.write("""
    1. **We Annualize:** We take your monthly spend and multiply by 12.
    2. **We Apply Limits:** If a card has a monthly cap (e.g., SBI Cashback's ₹5000 limit), we respect it.
    3. **We Deduct Fees:** We subtract the annual fee to show you 'Net Savings'.
    4. **No Bias:** We don't sell cards. The math decides the winner.
    """)

st.write("---")

# 3. SIDEBAR INPUTS
st.sidebar.header("📝 Your Profile")
salary = st.sidebar.number_input("Monthly Net Income (₹)", value=50000, step=5000)

with st.sidebar.expander("💸 Monthly Spends Details", expanded=True):
    spend_online = st.number_input(
        "Online Shopping (₹)", 
        value=10000, 
        step=1000,
        help="Amazon, Flipkart, Myntra, and other e-commerce sites."
    )
    spend_travel = st.number_input(
        "Travel (₹)", 
        value=5000, 
        step=1000,
        help="Flights, Hotels, Trains, and Bus bookings."
    )
    spend_other = st.number_input(
        "Other / Offline (₹)", 
        value=10000, 
        step=1000,
        help="Groceries, Dining, Utilities, and Offline swipe transactions."
    )

wants_lounge = st.sidebar.checkbox("I need Airport Lounge Access ✈️")

# 4. LOAD DATA & CALCULATE
@st.cache_data
def load_data():
    return pd.read_csv("cards.csv")

df = load_data()

def calculate_yield(row):
    # Annualize the monthly spends
    annual_online = spend_online * 12
    annual_travel = spend_travel * 12
    annual_other = spend_other * 12
    
    # 1. Calculate Raw Rewards (Uncapped)
    raw_online = (spend_online * row['Online Rate'] / 100)
    raw_travel = (spend_travel * row['Travel Rate'] / 100)
    raw_other = (spend_other * row['Base Rate'] / 100)
    
    raw_monthly_reward = raw_online + raw_travel + raw_other
    
    # 2. Apply the Cap (The "Bouncer" Logic)
    # logic: take the SMALLER number between "calculated reward" and "monthly limit"
    actual_monthly_reward = min(raw_monthly_reward, row['Monthly Cap'])
    
    # 3. Annualize
    total_annual_reward = actual_monthly_reward * 12
    
    # Net Benefit = Total Rewards - Annual Fee
    return total_annual_reward - row['Fee']

# Apply the math
df['Net Savings (₹)'] = df.apply(calculate_yield, axis=1)

# 5. FILTERING
# Step A: Filter by Income
valid_cards = df[df['Min Income'] <= salary].copy()

# Step B: Filter by Lounge (Optional)
if wants_lounge:
    valid_cards = valid_cards[valid_cards['Lounge Access'] == 'Yes']

# Step C: Sort to find the Winner
valid_cards = valid_cards.sort_values(by='Net Savings (₹)', ascending=False)

# 6. SHOW RESULTS
if not valid_cards.empty:
    best_card = valid_cards.iloc[0]
    
    # A. The Headline
    st.success(f"🏆 Best Card for You: **{best_card['Card Name']}**")
    st.metric(
        label="Total Annual Savings",
        value=f"₹ {int(best_card['Net Savings (₹)'])}",
        delta="Money in your pocket"
    )
    
    # B. The Visual (Altair Upgrade)
    st.write("---")
    st.header("📈 Savings Comparison")
    
    # Get top 5 cards
    top_cards = valid_cards.head(5).copy()
    
    # Create the Altair Chart
    chart = alt.Chart(top_cards).mark_bar().encode(
        x=alt.X('Net Savings (₹)', title='Annual Net Savings (₹)'),
        y=alt.Y('Card Name', sort='-x', title='Credit Card'),
        color=alt.Color('Net Savings (₹)', scale=alt.Scale(scheme='greens'), legend=None),
        tooltip=['Card Name', 'Net Savings (₹)', 'Fee', 'Reward Type']
    ).properties(
        height=300
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # C. The Details
    st.write("### 📊 Detailed Breakdown")
    st.dataframe(
        valid_cards[['Card Name', 'Fee', 'Net Savings (₹)', 'Lounge Access']],
        hide_index=True,
        use_container_width=True
    )

else:
    st.warning("No cards found for your criteria. Try lowering the filters.")