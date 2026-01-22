#backup of working file with api error sun 11 jan 9:23 pm
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
    /* Make images look crisp */
    img {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        max-height: 200px;
        object-fit: contain;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper: Indian Number Format
def format_inr(number):
    s, *d = str(int(number)).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    amount = "".join([r] + d)
    return f"₹ {amount}"

# --- AI ENGINE (UPDATED MODEL) ---
# Cache resource prevents re-running AI on same inputs (Saves Quota!)
@st.cache_resource(show_spinner=False)
def get_ai_insight_stream(salary, spends, card_name, savings, spend_online, spend_travel, spend_other, wants_lounge, Fee, reward_rate, reward_type):
    try:
        genai.configure(api_key=st.secrets["general"]["gemini_api_key"])
        # ✅ USING YOUR AVAILABLE MODEL (Stable, High Quota)
        model = genai.GenerativeModel('gemini-2.0-flash-lite-001')
        
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
        
        # stream=True enables the "Typing Effect"
        return model.generate_content(prompt, stream=True)
    except Exception as e:
        # We catch the error but return it so the UI can decide to show it or not
        return f"ERROR: {str(e)}"

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

# 3. SIDEBAR (Restored Debugger)
with st.sidebar:
    st.header("⚙️ Your Financial Profile")
    with st.container():
        st.subheader("💰 Income")
        salary = st.number_input("Monthly Net Salary", value=50000, step=5000, format="%d")
        st.caption(f"Reading: **{format_inr(salary)}** / month")
        st.caption(f"Annual: **{format_inr(salary * 12)}** / year")

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
    
    # --- DEBUGGER (Restored) ---
    st.divider()
    with st.expander("🔧 System Debugger"):
        if st.button("Check Available Models"):
            try:
                genai.configure(api_key=st.secrets["general"]["gemini_api_key"])
                models = [m.name for m in genai.list_models()]
                st.write("✅ **Access List:**")
                st.code(models)
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# 4. LOGIC ENGINE (Robust Data Loading)
@st.cache_data(ttl=60) # Short cache so you can update CSV easily
def load_data():
    df = pd.read_csv("cards.csv")
    
    # Force-clean column names (removes hidden spaces)
    df.columns = df.columns.str.strip()
    
    # Force-clean URL data
    if 'Apply_Link' in df.columns:
        df['Apply_Link'] = df['Apply_Link'].astype(str).str.strip()
        df['Apply_Link'] = df['Apply_Link'].replace({'nan': None, 'None': None, '': None})

    # Ensure columns exist
    if 'Image_URL' not in df.columns: df['Image_URL'] = None
    if 'Apply_Link' not in df.columns: df['Apply_Link'] = None
    
    return df

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
        
        # --- UI: THE WINNER SECTION ---
        st.markdown("---")
        
        # 1. Define columns: AI (Left) | Stats (Middle) | Image (Right)
        col_ai, col_stat, col_img = st.columns([2, 1.5, 1])
        
        # --- COLUMN 1: AI Analysis ---
        with col_ai:
            st.markdown(f"### 🏆 {best_card['Card Name']}")
            
            with st.chat_message("assistant"):
                stream_response = get_ai_insight_stream(
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
                
                # Check if it's an error string or a real stream
                if isinstance(stream_response, str) and stream_response.startswith("ERROR"):
                    st.error(stream_response)
                elif stream_response:
                    # Generator loop for smooth streaming
                    st.write_stream(chunk.text for chunk in stream_response)
                else:
                    st.warning("⚠️ AI is busy. Try again.")

        # --- COLUMN 2: Key Stats ---
        with col_stat:
            st.markdown('<div style="padding-top: 10px;"></div>', unsafe_allow_html=True)
            st.metric(label="Annual Net Savings", value=format_inr(best_card['Net Savings']), delta="Profit")
            st.metric(label="Base Reward Rate", value=f"{best_card['Base Rate']}%")
            st.markdown(f"**Fee:** {format_inr(best_card['Fee'])}")
            
             # Apply Button
            link = best_card.get('Apply_Link')
            if pd.notna(link) and str(link).strip() != "":
                 st.markdown('<div style="padding-top: 10px;"></div>', unsafe_allow_html=True)
                 st.link_button("🔗 Apply Now", str(link), type="primary")

        # --- COLUMN 3: Card Image ---
        with col_img:
            st.markdown('<div style="padding-top: 15px;"></div>', unsafe_allow_html=True)
            if pd.notna(best_card['Image_URL']) and str(best_card['Image_URL']).startswith('http'):
                st.image(best_card['Image_URL'], use_container_width=True)
            else:
                st.markdown("<h1 style='text-align: center; font-size: 80px;'>💳</h1>", unsafe_allow_html=True)

        # --- NEW: MATH EXPLANATION ---
        st.markdown("---")
        with st.expander("🧮 How did we calculate this?"):
            st.markdown(f"""
            **The Logic:**
            We calculated the total annual rewards based on your spending pattern:
            * **Online:** {format_inr(spend_online * 12)}/yr × **{best_card['Online Rate']}%**
            * **Travel:** {format_inr(spend_travel * 12)}/yr × **{best_card['Travel Rate']}%**
            * **Offline:** {format_inr(spend_other * 12)}/yr × **{best_card['Base Rate']}%**
            
            **The Formula:**
            `(Total Rewards - Annual Fee {format_inr(best_card['Fee'])}) = Net Savings`
            """)

        # --- COMPARISON CHART ---
        st.subheader("📊 Profitability Comparison")
        chart_data = valid_cards.head(5).copy()
        chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10).encode(
            x=alt.X('Net Savings', title='Net Annual Value (₹)'),
            y=alt.Y('Card Name', sort='-x', title=None),
            color=alt.Color('Net Savings', scale=alt.Scale(scheme='greens'), legend=None),
            tooltip=['Card Name', 'Net Savings', 'Fee']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

        # --- DATA TABLE ---
        with st.expander("🔍 See Detailed Breakdown"):
            display_df = valid_cards[['Card Name', 'Fee', 'Net Savings', 'Lounge Access', 'Apply_Link']]
            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Fee": st.column_config.NumberColumn(format="₹ %d"),
                    "Net Savings": st.column_config.NumberColumn(format="₹ %d"),
                    "Apply_Link": st.column_config.LinkColumn("More Info")
                }
            )

    else:
        st.error("😕 No cards found. Try increasing your salary or unchecking 'Lounge Access'.")
else:
    st.info("👈 Enter your details in the sidebar and click 'Calculate Best Card'")



#extra code for model list
# with st.expander("🛠️ Model Diagnostics (Debug)"):
    #     if st.button("List Available Models"):
    #         try:
    #             # 1. Connect
    #             client = genai.Client(api_key=st.secrets["general"]["gemini_api_key"])
                
    #             # 2. Fetch Models
    #             all_models = client.models.list()
                
    #             # 3. Filter for "Generative" models only
    #             # We look for models that support 'generateContent'
    #             gen_models = []
    #             for m in all_models:
                    
    #                 gen_models.append({
    #                 "Name": m.name,
    #                 "Display": m.display_name,
    #                 "Limit": "Check Studio" # API doesn't share live quota :(
    #                 })
                
    #             # 4. Show as Table
    #             if gen_models:
    #                 st.success(f"Found {len(gen_models)} active models!")
    #                 st.dataframe(pd.DataFrame(gen_models), hide_index=True)
    #             else:
    #                 st.warning("No generative models found.")
                    
    #         except Exception as e:
    #             st.error(f"Fetch failed: {str(e)}")