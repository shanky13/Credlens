import streamlit as st
import pandas as pd
import altair as alt
import gspread
# import google.generativeai as genai
from google import genai
from datetime import datetime

# 1. SETUP & CONFIGURATION
st.set_page_config(
    page_title="CredLens | India's Smartest Card Tool",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

CARD_BRAND_COLORS = {
    "SBI": "#1C4FA1",
    "HDFC": "#004C8F",
    "Axis": "#A6192E",
    "ICICI": "#F58220",
    "Amex": "#006FCF",
    "American Express": "#006FCF",
    "Standard Chartered": "#0473EA",
    "IDFC": "#9C1D27",
    "Tata": "#2B2E34",
    "Amazon": "#FF9900",
}

def get_brand_color(card_name):
    for brand, color in CARD_BRAND_COLORS.items():
        if brand.lower() in card_name.lower():
            return color
    return "#E53935"  # fallback red


# Custom CSS (Dark Mode Compatible)
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; }
    img { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-height: 200px; object-fit: contain; }
    
    /* READABILITY FIX: Force text color for Pros/Cons boxes */
    .pro-box { 
        background-color: #e6fffa;
        display: block;
        text-align: center;
        color: #0f5132; 
        padding: 10px; 
        border-radius: 5px; 
        border-left: 4px solid #00b894; 
        margin:5px auto;    
    }
    .con-box { 
        background-color: #fff5f5; 
        display: block;
        text-align: center;
        color: #842029; 
        padding: 10px; 
        border-radius: 5px; 
        border-left: 4px solid #ff7675; 
        margin:5px auto;
    }
    /* Status Badges */
    .status-badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em; margin-left: 10px; }
    .status-hot { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; } /* Gold */
    .status-devalued { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; } /* Red */
    .status-stable { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; } /* Green */
            
    </style>
    """, unsafe_allow_html=True)

def format_inr(number):
    s, *d = str(int(number)).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return f"₹ {''.join([r] + d)}"

# --- HYBRID AI ENGINE (Feature Flag Ready) ---
@st.cache_resource(show_spinner=False)
def get_ai_verdict(salary, spends, card_name, savings):
    try:
        client = genai.Client(
            api_key=st.secrets["general"]["gemini_api_key"]
        )

        prompt = f"""
        User Spend: {format_inr(spends)}/month. Salary: {format_inr(salary)}.
        Best Card: {card_name} (Saves {format_inr(savings)}/yr).
        Role: Witty financial Advisor
        Task: Write ONE punchy sentence acting as a financial advisor.
        Output: 1 punchy sentence (<20 words).
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )

        return response.text

    except Exception as e:
        st.error(f"🚨 DEBUG ERROR: {str(e)}")
        return None # Silent Fail (Safety Net)

# --- GOOGLE SHEETS CONNECTION ---
def save_to_google_sheets(salary, online, travel, offline, top_card, savings):
    try:
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        sh = gc.open("CredLens_Data")
        worksheet = sh.sheet1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, salary, online, travel, offline, top_card, savings]
        worksheet.append_row(row)
    except Exception:
        pass 

# 2. UI SECTION
st.title("💳 CredLens")
st.markdown("### Maximize your rewards. Minimize your fees.")

# 3. SIDEBAR
with st.sidebar:
    st.header("⚙️ Your Financial Profile")
    salary = st.number_input("Monthly Net Salary", value=50000, step=5000, format="%d")
    st.divider()
    
    st.subheader("💸 Monthly Spends")
    col1, col2 = st.columns(2)
    with col1:
        spend_online = st.number_input("Online (₹)", value=10000, step=1000, format="%d")
        spend_travel = st.number_input("Travel (₹)", value=5000, step=1000, format="%d")
    with col2:
        spend_other = st.number_input("Offline (₹)", value=10000, step=1000, format="%d")
    
    total_monthly_spend = spend_online + spend_travel + spend_other
    st.info(f"Total Monthly Spend: **{format_inr(total_monthly_spend)}**")
    st.divider()
    
    wants_lounge = st.checkbox("✅ Must have Airport Lounge")
    
    # --- FEATURE FLAG ---
    st.markdown("### 🤖 AI Settings")
    enable_ai = st.toggle("Enable AI Advisor", value=False, help="Turn on for personalized advice. Consumes quota.")
    
    calculate_btn = st.button("Calculate Best Card", type="primary")
    # ... inside the sidebar, after the Calculate button ...

    st.divider()
    

# 4. LOGIC ENGINE
@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_csv("cards.csv")
    df.columns = df.columns.str.strip()
    
    # Hybrid Data Safety Defaults
    if 'Pro_Reason' not in df.columns: df['Pro_Reason'] = "Great cashback rates."
    if 'Con_Reason' not in df.columns: df['Con_Reason'] = "Check fee waiver limits."
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
    
    valid_cards = df[df['Min Income'] <= salary].copy()
    if wants_lounge:
        valid_cards = valid_cards[valid_cards['Lounge Access'] == 'Yes']
    valid_cards = valid_cards.sort_values(by='Net Savings', ascending=False)

    if not valid_cards.empty:
        best_card = valid_cards.iloc[0]
        save_to_google_sheets(salary, spend_online, spend_travel, spend_other, best_card['Card Name'], int(best_card['Net Savings']))
        
        # 1. Get the basics of break-even math
        user_annual_spend = total_monthly_spend * 12
        fee = best_card['Fee']

        # 2. Calculate "Effective Rate" (The User's Personal Return %)
        # Logic: We take the 'Net Savings' (Profit) and add back the 'Fee' to get 'Gross Rewards'.
        # Then we divide by total spend to see the percentage.
        if user_annual_spend > 0:
            total_earnings = best_card['Net Savings'] + fee  # E.g. 2000 profit + 500 fee = 2500 earned
            effective_rate = (total_earnings / user_annual_spend) # E.g. 2500 / 100000 = 0.025 (2.5%)
        else:
            effective_rate = 0
        
        # 3. Calculate the Break-Even Target
        # Logic: Fee / Rate
        if effective_rate > 0:
            break_even_spend = int(fee / effective_rate) # E.g. 500 / 0.025 = 20,000
        else:
            break_even_spend = 9999999 # Impossible to break even if rate is 0

        # 4. Calculate Bar Fill %
        if break_even_spend > 0:
            pct_to_breakeven = min(1.0, user_annual_spend / break_even_spend)
        else:
            pct_to_breakeven = 1.0 # Bar is full if card is free

        # --- UI: 3-COLUMN LAYOUT ---
        st.markdown("---")

        # Columns: Analysis (Left) | Spacer | Stats (Middle) | Action (Right)
        col_text, col_spacer, col_stats, col_action = st.columns([2, 0.2, 1.2, 1.2])
        
        # COL 1: ANALYSIS & HYBRID CONTENT
        with col_text:
            col_l , col_c , col_r = st.columns([0.1,2,0.1])
            with col_c:
                # Dynamic status badge
                status = best_card.get("Status","Stable")
                if status == "hot":
                    s_class = "status-hot"
                elif status == "devalued":
                    s_class = "status-devalued"
                else:
                    s_class = "status-stable"

                st.markdown(f"## 🏆 {best_card['Card Name']} <span class='status-badge {s_class}'>{status}</span>", unsafe_allow_html=True)
                metric_col1 , metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric(label="Annual Net Savings", value=format_inr(best_card['Net Savings']), delta="Profit")
                with metric_col2:
                    st.metric(label="Annual Fee", value=format_inr(best_card['Fee']))
                with metric_col3:
                    st.metric(label="Base Reward Rate", value=f"{best_card['Base Rate']}%")
                
                # --- BREAK-EVEN BAR ---
                st.markdown(f"**💰 Break-Even Analysis:**")
                st.progress(pct_to_breakeven)
                
                if fee == 0:
                    st.caption("✅ **Lifetime Free Card.** Pure profit.")
                elif user_annual_spend >= break_even_spend:
                    st.caption(f"✅ **Profit Zone!** You recovered the {format_inr(fee)} fee at {format_inr(break_even_spend)}.")
                else:
                    shortfall = break_even_spend - user_annual_spend
                    st.caption(f"⚠️ **Fee Alert:** Spend {format_inr(shortfall)} more anually to recover the fee.")
                
                

                # --- PROS/CONS BOXES ---            
                #st.markdown("###")
                # Static Content (Instant Load)
                st.markdown(f"""
                <div class="pro-box"><b>✅ The Good:</b> {best_card['Pro_Reason']}</div>
                <div style="margin-top: 5px;"></div>
                <div class="con-box"><b>⚠️ The Bad:</b> {best_card['Con_Reason']}</div>
                """, unsafe_allow_html=True)
            
            # Dynamic AI (Controlled by Feature Flag)
            if enable_ai:
                st.markdown("###")
                with st.spinner("🤖 Advisor thinking..."):
                     ai_verdict = get_ai_verdict(salary, total_monthly_spend, best_card['Card Name'], best_card['Net Savings'])
                if ai_verdict:
                    st.info(f"🤖 **Advisor:** {ai_verdict}")
                else:
                    st.caption("⚠️ AI Napping (Quota). Pros/Cons are accurate.")

        # COL 2: HARD STATS
        with col_stats:
            st.markdown('<div style="padding-top: 10px;"></div>', unsafe_allow_html=True)
            market_rating = best_card.get("Market_Rating" ,4.0)
            st.metric(label="Market Sentiment", value=  f"{market_rating}  ⭐")
            st.markdown('<div style = "margin-top: 2px;font-size: 12px;">Based on public reviews.</style>', unsafe_allow_html=True)
            

            if 'Reward Type' in best_card:
                st.markdown(f"### Type: {best_card['Reward Type']}")
            if pd.notna(best_card["Warning_Text"]) :
                st.warning(f"⚠️ **Heads Up:** {best_card['Warning_Text']}")
            st.markdown(f" For detailed reviews, click [here](https://www.google.com/search?q={best_card['Card Name'].replace(' ', '+')}+reviews).")

        # COL 3: IMAGE & ACTION
        with col_action:
            st.markdown('<div style="padding-top: 15px;"></div>', unsafe_allow_html=True)
            if pd.notna(best_card['Image_URL']) and str(best_card['Image_URL']).startswith('http'):
                st.image(best_card['Image_URL'], use_container_width=True)
            else:
                st.markdown("<h1 style='text-align: center; font-size: 80px;'>💳</h1>", unsafe_allow_html=True)
            
            # Button Stacked Below Image
            link = best_card.get('Apply_Link')
            if pd.notna(link) and str(link).strip() != "":
                st.markdown('<div style="padding-top: 5px;"></div>', unsafe_allow_html=True)
                 #st.link_button("🔗 Apply Now", str(link), type="primary", use_container_width=True,)
                brand_color = get_brand_color(best_card["Card Name"])

                # 4️⃣ Display the Apply button with pulse + glow + hover effect
                # Apply button with pulse + hover glow
                # -----------------------------
                # ALIGNMENT FIX: Center button under image
                # -----------------------------
                st.markdown(
                    f"""
                    <div style="text-align:center;"> <!-- Centering container -->
                        <a href="{best_card['Apply_Link']}" target="_blank">
                            <button class="apply-btn" style="
                                background:{brand_color};
                                color:white;
                                padding:14px 28px;
                                border:none;
                                border-radius:12px;
                                font-size:16px;
                                font-weight:600;
                                cursor:pointer;
                                transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
                                animation: pulse 1.8s infinite alternate; /* Pulse animation */
                            ">
                                🔗 Apply Now
                            </button>
                        </a>
                    </div>

                    <style>
                    /* Hover effect stops pulse and adds glow */
                    .apply-btn:hover {{
                        animation: none; /* Stop pulse on hover */
                        transform: translateY(-2px) scale(1.05);
                        box-shadow: 0 0 20px {brand_color}66;
                        filter: brightness(1.1);
                    }}

                    /* Lightweight pulse animation */
                    @keyframes pulse {{
                        0% {{ transform: scale(1); opacity: 0.9; }}
                        100% {{ transform: scale(1.05); opacity: 1; }}
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                 

        # --- RESTORED: MATH EXPLANATION ---
        st.markdown("---")
        with st.expander("🧮 How did we calculate this? (The Math)"):
            st.markdown(f"""
            **The Formula:**
            We projected your spending over **12 months** and applied the card's specific reward rates.
            
            * **Online Spends:** {format_inr(spend_online * 12)} × **{best_card['Online Rate']}%**
            * **Travel Spends:** {format_inr(spend_travel * 12)} × **{best_card['Travel Rate']}%**
            * **Offline Spends:** {format_inr(spend_other * 12)} × **{best_card['Base Rate']}%**
            
            **Net Calculation:**  `(Total Rewards - Annual Fee {format_inr(best_card['Fee'])}) = {format_inr(best_card['Net Savings'])}`  
            *Note: We also accounted for monthly capping limits.*
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
            display_cols = ['Card Name', 'Fee', 'Net Savings', 'Lounge Access']
            if 'Apply_Link' in valid_cards.columns:
                display_cols.append('Apply_Link')
                
            st.dataframe(
                valid_cards[display_cols],
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Fee": st.column_config.NumberColumn(format="₹ %d"),
                    "Net Savings": st.column_config.NumberColumn(format="₹ %d"),
                    "Apply_Link": st.column_config.LinkColumn("Apply")
                }
            )

    else:
        st.error("😕 No cards found.")
else:
    st.info("👈 Enter your details in the sidebar and click 'Calculate Best Card'")