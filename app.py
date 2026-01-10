import streamlit as st
import pandas as pd
import altair as alt
import gspread
import google.generativeai as genai
from datetime import datetime

# 1. SETUP & CONFIGURATION
st.set_page_config(
    page_title="CredLens | India's Smartest Card Tool",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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

# Helper: Indian Number Format
def format_inr(number):
    s, *d = str(int(number)).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    amount = "".join([r] + d)
    return f"₹ {amount}"

# --- AI ENGINE (UPDATED) ---
def get_ai_insight(salary, spends, card_name, savings, spend_online, spend_travel, spend_other, wants_lounge, Fee, reward_rate, reward_type):
    try:
        # 1. Configure
        genai.configure(api_key=st.secrets["general"]["gemini_api_key"])
        
        # 2. Model Selection
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 3. The Prompt (Optimized Structure)
        prompt = f"""
        You are an expert Credit Card Advisor in India.
        
        # User Profile
        - Income: {format_inr(salary)}
        - Spends: {format_inr(spends)} (Online: {format_inr(spend_online)}, Travel: {format_inr(spend_travel)})
        - Lounge Need: {"Yes" if wants_lounge else "No"}
        
        # The Card: {card_name}
        - Fee: {format_inr(Fee)}
        - Reward: {reward_rate}% ({reward_type})
        - Net Savings: {format_inr(savings)}
        
        # Task
        Write a short, punchy analysis in Markdown format:
        
        ### 💳 {reward_type} Card ({reward_rate}% Return)
        
        **✅ Why this fits you:**
        * [Reason 1 based on their highest spend category]
        * [Reason 2 based on benefits vs fee]
        
        **⚠️ One Downside:**
        * [One logical con based on their profile]
        
        Use an encouraging, professional tone. Keep it brief.
        """
        
        # 4. Generate
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Insight unavailable: {str(e)}"

# --- GOOGLE SHEETS CONNECTION ---
def save_to_google_sheets(salary, online, travel, offline, top_card, savings):
    try:
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        sh = gc.open("CredLens_Data")
        worksheet = sh.sheet1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, salary, online, travel, offline, top_card, savings]
        worksheet.append_row(row)
    except Exception as e:
        print(f"Logging failed: {e}")

# 2. HERO SECTION
st.title("💳 CredLens")
st.markdown("### Maximize your rewards. Minimize your fees.")

# 3. SIDEBAR
with st.sidebar:
    st.header("⚙️ Your Financial Profile")
    with st.container():
        st.subheader("💰 Income")
        salary = st.number_input("Monthly Net Salary", value=50000, step=5000, format="%d")
        st.caption(f"Reading: **{format_inr(salary)}** / month")
        st.caption(f"Annual Salary: **{format_inr(salary * 12)}** / year")

    st.divider()

    with st.container():
        st.subheader("💸 Monthly Spends")
        col1, col2 = st.columns(2)
        with col1:
            spend_online = st.number_input("Online (₹)", value=10000, step=1000, format="%d")
            st.caption(f"{format_inr(spend_online)}") 
            spend_travel = st.number_input("Travel (₹)", value=5000, step=1000, format="%d")
            st.caption(f"{format_inr(spend_travel)}") 
        with col2:
            spend_other = st.number_input("Offline (₹)", value=10000, step=1000, format="%d")
            st.caption(f"{format_inr(spend_other)}") 
            
        total_monthly_spend = spend_online + spend_travel + spend_other
        st.info(f"Total Monthly Spend: **{format_inr(total_monthly_spend)}**")

    st.divider()
    wants_lounge = st.checkbox("✅ Must have Airport Lounge")
    calculate_btn = st.button("Calculate Best Card", type="primary")
    
    st.divider()
    # Debugger (Optional: You can remove this later)
    with st.expander("🔧 System Debugger"):
        if st.button("Check Available Models"):
            try:
                genai.configure(api_key=st.secrets["general"]["gemini_api_key"])
                models = [m.name for m in genai.list_models()]
                st.write("✅ Available Models:")
                st.write(models)
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# 4. LOGIC ENGINE
@st.cache_data
def load_data():
    return pd.read_csv("cards.csv")

df = load_data()

def calculate_yield(row):
    annual_online = spend_online * 12
    annual_travel = spend_travel * 12
    annual_other = spend_other * 12
    raw_reward = ((annual_online * row['Online Rate'] / 100) + (annual_travel * row['Travel Rate'] / 100) + (annual_other * row['Base Rate'] / 100))
    annual_cap = row['Monthly Cap'] * 12
    actual_reward = min(raw_reward, annual_cap)
    return actual_reward - row['Fee']

# 5. MAIN EXECUTION
if calculate_btn:
    df['Net Savings'] = df.apply(calculate_yield, axis=1)
    
    # Filter Logic
    valid_cards = df[df['Min Income'] <= salary].copy()
    if wants_lounge:
        valid_cards = valid_cards[valid_cards['Lounge Access'] == 'Yes']
    valid_cards = valid_cards.sort_values(by='Net Savings', ascending=False)

    if not valid_cards.empty:
        best_card = valid_cards.iloc[0]
        
        # Save Data
        save_to_google_sheets(salary, spend_online, spend_travel, spend_other, best_card['Card Name'], int(best_card['Net Savings']))
        
        # --- UI DISPLAY ---
        st.markdown("---")
        col_winner, col_stats = st.columns([2, 1])
        
        with col_winner:
            st.subheader("🏆 The Best Card for You")
            st.success(f"## {best_card['Card Name']}")
            
            # --- AI INSIGHT BUTTON ---
            with st.spinner("🤖 Asking Gemini for advice..."):
                # UPDATED: Passing all variables correctly now!
                insight = get_ai_insight(
                    salary=salary,
                    spends=total_monthly_spend,
                    card_name=best_card['Card Name'],
                    savings=best_card['Net Savings'],
                    spend_online=spend_online,
                    spend_travel=spend_travel,
                    spend_other=spend_other,
                    wants_lounge=wants_lounge,
                    Fee=best_card['Fee'],
                    reward_rate=best_card.get('Base Rate', 0),
                    reward_type=best_card.get('Reward Type', 'Points')
                )
                st.info(f"**Why this card?**\n\n{insight}")
            
        with col_stats:
            st.metric(label="Annual Net Savings", value=format_inr(best_card['Net Savings']), delta="Profit")

        # Chart
        st.subheader("📊 Profitability Comparison")
        chart_data = valid_cards.head(5).copy()
        chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10).encode(
            x=alt.X('Net Savings', title='Net Annual Value (₹)'),
            y=alt.Y('Card Name', sort='-x', title=None),
            color=alt.Color('Net Savings', scale=alt.Scale(scheme='greens'), legend=None),
            tooltip=['Card Name', 'Net Savings', 'Fee']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

        # --- DATA TABLE (Updated for Sorting) ---
        with st.expander("🔍 See Detailed Breakdown"):
            # Create a clean view for the table
            display_df = valid_cards[['Card Name', 'Fee', 'Net Savings', 'Lounge Access']]
            
            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Fee": st.column_config.NumberColumn(format="₹ %d"),
                    "Net Savings": st.column_config.NumberColumn(format="₹ %d"),
                }
            )

    else:
        st.error("😕 No cards found. Try increasing your salary or unchecking 'Lounge Access'.")
else:
    st.info("👈 Enter your details in the sidebar and click 'Calculate Best Card'")