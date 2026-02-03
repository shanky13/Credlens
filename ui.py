import streamlit as st
import altair as alt
import pandas as pd
from logic import format_inr # We reuse the formatter

# In ui.py

def render_header():
    """Renders the main page title and subtitle."""
    st.title("💳 CredLens")
    st.markdown("### Maximize your rewards. Minimize your fees.")

# 1. STYLING (CSS)
# ui.py

def render_custom_css():
    st.markdown("""
    <style>
    /* ... Keep your existing card/box styles here ... */
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; }
    img { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-height: 200px; object-fit: contain; }
    
    .pro-box { background-color: #e6fffa; color: #0f5132; padding: 10px; border-radius: 5px; border-left: 4px solid #00b894; margin:5px auto; }
    .con-box { background-color: #fff5f5; color: #842029; padding: 10px; border-radius: 5px; border-left: 4px solid #ff7675; margin:5px auto; }
    
    /* --- 2. STATUS BADGES (THIS IS WHAT YOU ASKED ABOUT) --- */
    .status-badge { padding: 4px 8px; border-radius: 130px; font-weight: bold; font-size: 0.8em; margin-left: 5px; }
    
    /* 🔥 HOT: Gold/Yellow */
    .status-hot { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .status-hot::after { content: " 🔥"; font-size: 0.8em; }
    
    /* 🔻 DEVALUED: Red/Danger (CONFIRMED) */
    .status-devalued { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .status-devalued::after { content: " 🔻"; font-size: 0.8em; } 
    
    /* ✅ STABLE: Green/Safe */
    .status-stable { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .status-stable::after { content: " ✅"; font-size: 0.8em; }
                
    /* --- NEW: BUTTON ANIMATION STYLES --- */
    
    /* 1. The Pulse Definition */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.1);  }
        50% { transform: scale(1.05); box-shadow: 0 0 15px 5px rgba(0, 0, 0, 0.15); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.1); }
    }

    /* 2. The Button Class */
    .apply-btn {
        color:white;
        padding:14px 28px;
        border:none;
        border-radius:12px;
        font-size:16px;
        font-weight:600;
        cursor:pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
        animation: pulse 1.8s infinite ease-in-out;
        
    }

    /* 3. Hover Effect (Stop pulsing, start glowing) */
    .apply-btn:hover {
        /* THE MAGIC TRICK */
        /* brightness(1.1) = 110% brightness (Lighter/Glow) */
        /* brightness(0.9) = 90% brightness (Darker) */
        filter: brightness(1.3); 
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        transform: translateY(-10px) scale(1.5);
        /* Grow slightly */
    }
    
    /* --- 4. VERDICT BOXES (New Feature) --- */
    .verdict-box {
        padding: 5px 8px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        font-size: 0.9rem;
        line-height: 1.2;
        border: 1px solid transparent; /* Placeholder for border */
    }

    /* Variation 1: The Red Flag */
    .v-danger { background-color: #fdf2f2; color: #d9534f; border-color: #f5c6cb; }

    /* Variation 2: The Gem */
    .v-success { background-color: #eafbf1; color: #28a745; border-color: #c3e6cb; }

    /* Variation 3: Fair Value */
    .v-neutral { background-color: #f0f2f6; color: #155724; border-color: #dfe2e5; }
    </style>
    """, unsafe_allow_html=True)

    # --- 5. METRIC LABEL FIX (Prevents "Annual Net S...") ---
    st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        white-space: normal !important; /* Forces text to wrap */
        overflow: visible !important;   /* Shows the full text */
        line-height: 1.2 !important;    /* Keeps lines close together */
        height: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HELPER: BRAND COLORS

def get_brand_color(card_name):
    # Dictionary mapping brand keywords to Hex Codes
    colors = {
        # The Big Players
        "SBI": "#1C4FA1",       # Navy Blue
        "HDFC": "#004C8F",      # Dark Blue
        "Axis": "#97144D",      # Burgundy (Axis Official)
        "ICICI": "#F58220",     # Orange
        "Amex": "#006FCF",      # Bright Blue
        "American": "#006FCF",  
        
        # The New Specialists (Added)
        "Airtel": "#E40000",    # Airtel Red
        "Swiggy": "#FC8019",    # Swiggy Orange
        "Tata": "#2B2E34",      # Tata Black/Grey
        "Amazon": "#FF9900",    # Amazon Yellow/Orange
        "HSBC": "#DB0011",      # HSBC Red
        "Yes": "#00539C",       # Yes Bank Blue
        "AU": "#682C91",        # AU Bank Purple
        "IDFC": "#9C1D27",      # IDFC Red
        "OneCard": "#1A1A1A",   # Metal Black
        "Standard": "#007D3E",  # SC Green (Official is Green/Blue)
    }
    
    # Search for the keyword in the card name
    for brand, color in colors.items():
        if brand.lower() in str(card_name).lower():
            return color
            
    # Default Color (if no brand matches)
    return "#555555" # Changed to Grey (Neutral) instead of Red (Danger)

# 3. SIDEBAR INPUTS
def render_sidebar(card_list):
    """Renders the sidebar and returns a dictionary of user inputs."""
    with st.sidebar:
        st.header("⚙️ Financial Profile")
        
        h1,h2 = st.columns(2)

        with h1 :
            age = st.number_input("Age" , min_value = 10 , max_value = 100 , key = "age")
        with h2 :
            credit_score = st.number_input("Credit Score" , min_value = 300 , max_value = 900 , key = "cibil" , help="\nTo get the credit score for free :  \nGpay :Home > scroll to bottom > Check your CIBIL score.  \nPhonepe: Home > Credit Score")

        salary = st.number_input("Monthly Net Salary", min_value=0, step=5000, key = "salary",format="%d", help="Your take-home pay after taxes and deductions.")
        st.divider()
        
        st.subheader("💸 Monthly Spends")
        c1, c2 = st.columns(2)
        with c1:
            online = st.number_input("Online (₹)", min_value=0, max_value=100000, step=1000, key="online", format="%d", help="E-commerce, Subscriptions, Bill Payments")
            travel = st.number_input("Travel (₹)", min_value=0, max_value=100000, step=1000, key="travel", format="%d" , help="Flights, Hotels, Cabs")
        with c2:
            offline = st.number_input("Offline (₹)", min_value=0, max_value=100000, step=1000, key="offline", format="%d" , help="In-store, Dining, Groceries")

        
        # NEW: Advanced Section for Specialist Cards
        with st.expander("Advanced Spends (Utilities, UPI)"):
            utilities = st.number_input("⚡ Utilities (Bills, Recharge)", min_value=0, key="utilities", step=500 , help="Electricity, Water, Mobile Bills")
            upi = st.number_input("📱 UPI / Scan & Pay", min_value=0, key="upi", step=500 , help="UPI transactions, QR payments")
        
        total = online + travel + offline + utilities + upi
        st.info(f"Total Monthly Spend: **{format_inr(total)}**")
        
        
        wants_lounge = st.checkbox(" ✈️ Must have Airport Lounge" , key = "filter_lounge" , help="Filter cards that offer complimentary airport lounge access.")

        # --- NEW SECTION: COMPARISON ---
        st.divider()
        st.subheader("🔄 Smart Switch")
        st.caption("Compare against your current card")
        
        # We add "None" as the default option
        current_card_name = st.selectbox(
            "I currently use:", 
            options=["I don't have a card"] + card_list,
            key="current_card_input" , help="Select your current primary credit card for comparison."
        )
        # -------------------------------

        st.sidebar.markdown("---")

        st.markdown("### 🤖 AI Settings")
        enable_ai = st.sidebar.toggle("Enable AI Advisor", key = "enable_ai", help="Get personalized card recommendations using AI analysis.")
        ask_ai_clicked = False

        if enable_ai:
            if st.sidebar.button("🔮 Ask Gemini for Advice"):
                ask_ai_clicked = True # To indicate button was clicked
        
    return {
            "age": age,
            "credit_score": credit_score,
        "salary": salary,
        "spends": {"online": online, "travel": travel, "offline": offline, "total": total, "utilities": utilities, "upi": upi},
        "wants_lounge": wants_lounge,
        "enable_ai": enable_ai,
        "ask_ai_clicked": ask_ai_clicked,
        "current_card_name": current_card_name
    }

# 4. RESULTS DISPLAY (The Heavy Lifter)
def render_results(best_card, break_even_stats, ai_verdict, valid_cards_df, spends, verdict, comparison_data = None,age = 10 , credit_score = 700, approval_odds = 0):
    """Renders the entire results section (Top Card + Chart + Table)."""
    
    st.markdown("---")
    
    # A. Layout: Left (Details) | Right (Stats & Image)
    # Using the same ratio as before
    col_text, col_stats, col_action = st.columns([2.0, 1.2, 1.2])

    # --- LEFT COLUMN: Main Info & Break-Even ---
    with col_text:
        col_c, col_r = st.columns([ 2, 0.02])
        with col_c:
            # Badge Logic
            status = best_card.get("Status", "Stable")
            s_class = f"status-{status.lower()}" if status.lower() else "stable"
            
            st.markdown(f"## 🏆 {best_card['Card Name']} <span class='status-badge {s_class}'>{status}</span>", unsafe_allow_html=True)
            annual_net_saving = best_card['Net Savings']
            delta_text = "Profit" if annual_net_saving >= 0 else "-Loss" 
            # Key Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Annual Net Savings", value = format_inr(annual_net_saving), delta_color="normal", delta = delta_text)
            m2.metric("Annual Fee", format_inr(best_card['Fee']))
            m3.metric("Base Reward", f"{best_card['Base Rate']}%")

            # Break-Even Bar
            
            st.caption(f"**Break-Even Analysis** (Fee: {format_inr(best_card['Fee'])})")
            
            # --- SMART LOGIC START ---
            if best_card['Fee'] == 0:
                # CASE 1: Lifetime Free Card
                st.success("🎉 **Lifetime Free Card!** You are profitable from Day 1.")
                st.progress(100)
            else:
                # CASE 2: Normal Card (Do the math)
                # Calculate percent recovered (capped at 100% for the bar)
                annual_reward = best_card['Net Savings'] + best_card['Fee']
                annual_reward = max(0, annual_reward)  # Ensure reward is not negative

                percent_recovered = min(annual_reward/ (best_card['Fee'] ), 1.0)
                
                st.progress(float(percent_recovered))
                
                if percent_recovered >= 1.0:
                    st.caption("✅ Congratulations! For current spend Fee is fully recovered in an year.")
                else:
                    st.caption(f"ℹ️ Your rewards recover **{int(percent_recovered*100)}%** of the annual fee.")

            if best_card['Fee'] > 0 and annual_reward > 0:
                monthly_rewards = annual_reward / 12
                months_to_break_even = best_card['Fee'] / monthly_rewards

                if months_to_break_even <= 12:
                    st.caption(
                    f"⏱️ At current monthly spending, you will break even in **{int(months_to_break_even)} months**.")
                else:
                    st.caption("⚠️ At current spending, you may not recover the fee within a year.")

            
            # --- SMART LOGIC END ---

            # Pros/Cons
            st.markdown("Why This Card?")
            st.markdown(f"""
            <div class="pro-box"><b>✅ The Good:</b> {best_card['Pro_Reason']}</div>
            <div class="con-box"><b>⚠️ The Bad:</b> {best_card['Con_Reason']}</div>
            """, unsafe_allow_html=True)
            
            # AI Verdict Display
            if ai_verdict:
                st.markdown("###")
                st.info(f"🤖 **Advisor:** {ai_verdict}")

    # --- RIGHT COLUMNS: Stats & Image ---
    with col_stats:
        st.markdown('<div style="padding-top: 10px;"></div>', unsafe_allow_html=True)
        # --- NEW: CONTRAST RATINGS ---
        # We split the stats column into two mini-columns
        
        # --- NEW: STYLED CONTRAST RATINGS ---
        r1, r2 = st.columns([1, 1]) # Give Verdict slightly more space
        
        with r1:
            st.metric("Market Hype", f"{best_card.get('Market_Rating', 4.5)} ⭐")
        
        with r2:
            st.markdown('<div style="text-align: center; font-weight: bold; cursor: help;" title="Based on Net Savings vs Fees">CredLens Verdict</div>', unsafe_allow_html=True)

            # Dynamic Color Logic
            # 1. LOGIC: Pick the Class Name (Not the color code)
            if "Negative" in verdict:
                v_class = "v-danger"
            elif "Gem" in verdict or "Top" in verdict:
                v_class = "v-success"
            else:
                v_class = "v-neutral"
            
            # 2. RENDER: Use the class
            st.markdown(f"""
            <div class="verdict-box {v_class}">
                {verdict}
            </div>
            """, unsafe_allow_html=True)

        # 3. Reward Type 
        # if 'Reward Type' in best_card:
        #     st.markdown(f"**Type:** {best_card['Reward Type']}")

        
        if pd.notna(best_card.get("Warning_Text")):
            st.warning(f"⚠️ {best_card['Warning_Text']}")
        
        # --- NEW: SMART CONTEXTUAL ALERTS ---
        if comparison_data:
        
            # 1. THE "NO CARD" NUDGE
            if comparison_data['type'] == 'no_card':
                st.info(f"🚀 **Get Best Card Now:** Start your credit card journey with  **{best_card['Card Name']}!** " )

            # 2. THE "SAME CARD" VALIDATION
            elif comparison_data['type'] == 'same_card':
                st.success(f"🎉 **Great Job!** You already own the **{best_card['Card Name']}**. You are maximizing your returns!")

            # 3. THE "SAME CARD" VALIDATION
            elif comparison_data['type'] == 'no_card_lounge':
                st.success(f"⚠️ **Your card:** **{comparison_data['current_card_name']}** does not provide lounge access! switch to **{best_card['Card Name']}** to enjoy complimentary lounges. 🛫")

            # 3. THE "SWITCH" WARNING (Existing Logic)
            elif comparison_data['type'] == 'switch':
                curr_name = comparison_data['current_card_name']
                diff = comparison_data['diff']

                if diff > 0:
                # Positive Diff = The Winner is BETTER (Switch!)
                
                    # --- DYNAMIC ANALOGY ENGINE ---
                    if diff < 2000:
                        analogy = "pays for a nice weekend dinner! 🍕"
                    elif diff < 5000:
                        analogy = "covers your Netflix & WiFi bills for the year! 🎬"
                    elif diff < 10000:
                        analogy = "effectively pays for a domestic flight! ✈️"
                    elif diff < 25000:
                        analogy = "is like getting a free Android phone every year! 📱"
                    elif diff == 0:
                        analogy = "Great choice!!"
                    else:
                        analogy = "could pay for an international holiday! 🏖️"
                    # ------------------------------

                    st.warning(f"💸 **Stop Losing Money!**")
                    st.markdown(f"""
                    <div style="background-color: #fff3cd; color: #155724; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107; margin-bottom: 20px;">
                        You are leaving <b>{format_inr(diff)}</b> on the table every year by using <b>{curr_name}</b> instead of <b>{best_card['Card Name']}</b>.
                        <br>
                        <small>👉  Switching {analogy}</small>
                    </div>
                    """, unsafe_allow_html=True)

                elif diff < 0: 
                    # Negative Diff = The Current Card is ACTUALLY BETTER than our algorithm's pick?
                    # (Rare, but happens if the user selected a Super Premium card we filtered out by salary, or logic quirks)
                    st.success(f"✅ **Good News!** Your current card ({curr_name}) is actually performing great. as the diff is {diff} and current savings is {comparison_data['current_savings']}. Keep using it!")

            approval = st.button("Click here for your approval odds", key="approval_button")
            if approval:
                st.balloons()
                st.info(f"Based on your credit score of {credit_score} , your approval odds for {best_card['Card Name']} is approximately {approval_odds*100:.1f}% .")
        #else:
            #st.balloons()
            #st.info(f"""Its the best time to go ahead with ✅ {best_card['Card Name']}!""")
        # ----------------------------------------

        

       
            
    with col_action:
        st.markdown('<div style="padding-top: 15px;"></div>', unsafe_allow_html=True)
        img_url = best_card.get('Image_URL')
        if pd.notna(img_url):
            st.image(img_url, use_container_width=True)
        
        # Apply Button
        link = best_card.get('Apply_Link')
        if pd.notna(link):
            color = get_brand_color(best_card['Card Name'])
            
            # We inject the style and class here
            st.markdown(f"""
            <div style="text-align:center; margin-top:15px;">
                <a href="{link}" target="_blank" style="text-decoration:none;">
                    <button class="apply-btn" style="background-color: {color}; ">
                        🔗 Apply Now
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("###")
        st.markdown("They rate on features. We rate on **Math**.")
        # 4. CARD: Link 
        search_query = best_card['Card Name'].replace(' ', '+')
        st.markdown(f"For detailed reviews, [click here](https://www.google.com/search?q={search_query}+reviews).")

    # 5. RESTORED: The Math Expander 
    # This now uses the 'spends' argument we added
    st.markdown("---")
    with st.expander("🧮 How did we calculate this? (The Math)"):
        
        # We build the formula text dynamically so we don't show "0 * 0%" lines
        formula_md = "**The Formula:**\n\n"
        
        # 1. Online
        if spends.get('online', 0) > 0:
            formula_md += f"* **Online:** {format_inr(spends['online']*12)} × **{best_card.get('Online Rate', 0)}%**\n"
            
        # 2. Utilities (NEW)
        if spends.get('utilities', 0) > 0:
            util_rate = best_card.get('Utility Rate', best_card.get('Base Rate', 0))
            formula_md += f"* **Utilities:** {format_inr(spends['utilities']*12)} × **{util_rate}%**\n"
            
        # 3. UPI (NEW)
        if spends.get('upi', 0) > 0:
            upi_rate = best_card.get('UPI Rate', 0)
            formula_md += f"* **UPI:** {format_inr(spends['upi']*12)} × **{upi_rate}%**\n"
            
        # 4. Travel
        if spends.get('travel', 0) > 0:
            formula_md += f"* **Travel:** {format_inr(spends['travel']*12)} × **{best_card.get('Travel Rate', 0)}%**\n"
            
        # 5. Offline/Base
        if spends.get('offline', 0) > 0:
            formula_md += f"* **Offline:** {format_inr(spends['offline']*12)} × **{best_card.get('Base Rate', 0)}%**\n"
            
        formula_md += f"\n**Net Calculation:** `(Total Rewards - Annual Fee) = Profit`"
        
        st.markdown(formula_md)

    # 6. FIXED: Chart Height (Fixing Item #5)
    st.subheader("📊 Profitability Comparison")
    chart_data = valid_cards_df.head(5).copy()
    c = alt.Chart(chart_data).mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10).encode(
        x=alt.X('Net Savings', title='Net Annual Value (₹)'),
        y=alt.Y('Card Name', sort='-x', title=None),
        color=alt.Color('Net Savings', scale=alt.Scale(scheme='greens'), legend=None)
    ).properties(height=350) # <--- Increased height here
    st.altair_chart(c, use_container_width=True)
    
    with st.expander("🔍 Detailed Comparison"):
            # Define the columns we WANT to show
        display_cols = [
            "Card Name", "Status", "Net Savings", "Fee", 
            "Reward Type", "Min Income", "Warning_Text"
        ]
        
        # Filter the dataframe to only show these columns (if they exist)
        # We use list intersection to avoid errors if a column is missing
        final_cols = [c for c in display_cols if c in valid_cards_df.columns]
        
        display_df = valid_cards_df[final_cols].copy()
        
        # Format the numbers for display
        if "Net Savings" in display_df.columns:
            display_df["Net Savings"] = display_df["Net Savings"].apply(format_inr)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Hot, Stable, or Devalued",
                    width="small"
                ),
                "Warning_Text": st.column_config.TextColumn(
                    "Warnings",
                    width="medium"
                )
            }
        )