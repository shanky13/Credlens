import streamlit as st
import altair as alt
import pandas as pd
from logic import format_inr # We reuse the formatter

# In ui.py

def render_header():
    """Renders the main page title and subtitle."""
    #st.title("💳 CredLens")
    #st.markdown("### Maximize your rewards. Minimize your fees.")
    #st.markdown("### Understand what your credit card is actually worth")
    st.markdown("""
    <h1>CredLens</h1>
    <h3>Understand what your credit card is actually worth</h3>
    <div class="hero-subtext">
    Based on how you spend — not generic rankings.
    </div>
    """, unsafe_allow_html=True)

# ui.py

def sidebar_section_header(title):
    """
    Renders a tight header with a top border, bypassing Streamlit's default gaps.
    """
    st.markdown(f"""
    <div style="
        border-top: 1.2px solid #5f6368;; 
        margin-top: 5px; 
        padding-top: 15px; 
        margin-bottom: 15px;
        font-weight: 600;
        font-size: 1.2rem;
        color: white;">
        {title}
    </div>
    """, unsafe_allow_html=True)


# 1. STYLING (CSS)
# ui.py

def render_custom_css():
    st.markdown("""
    <style>
    /* 1. LAYOUT & SPACING FIXES */
    .block-container {
        padding-top: 1rem !important; /* Reduce top whitespace */
        padding-bottom: 2rem !important;
    }
    
    /* Compact spacing between elements */
    .stAlert { padding: 0.5rem 1rem !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0.5rem !important; }
    
    /* 2. TYPOGRAPHY & HEADERS */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -1px;
        font-size: 2.5rem;
    }
    
    /* Target the Headers immediately following dividers */
    h2, h3 {
        padding-top: 0.2rem !important; /* Kill the huge default top padding */
        margin-top: 0rem !important;
    }
    
    /* Optional: Fix the specific st.header class if the above doesn't catch it */
    div[data-testid="stMarkdownContainer"] > h2 {
        padding-top: 0rem !important;
    }
                
    .hero-subtext {
        font-size: 1.1rem;
        color: #5f6368;
        margin-bottom: 1.5rem;
    }

    /* 3. THE "MONEY BOX" (Smart Switch Alert) */
    .money-alert {
        background: linear-gradient(135deg, #fff3cd 0%, #fff8e1 100%);
        border: 1px solid #ffeeba;
        border-left: 5px solid #ffc107;
        color: #856404;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .money-alert strong { color: #533f03; }

    /* 4. THE "WINNER CARD" GLOW */
    .winner-container {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Subtle shadow */
        transition: transform 0.2s;
    }
    
    /* 5. EXISTING STYLES (Kept intact) */
    .status-badge { padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 0.75em; vertical-align: middle; }
    .status-hot { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    .status-devalued { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .status-stable { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }

    .pro-box { background-color: #e6fffa; color: #0f5132; padding: 10px; border-radius: 6px; border-left: 4px solid #00b894; margin: 8px 0; font-size: 0.9rem; }
    .con-box { background-color: #fff5f5; color: #842029; padding: 10px; border-radius: 6px; border-left: 4px solid #ff7675; margin: 8px 0; font-size: 0.9rem; }

    /* Pulse Button */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
    }
    .apply-btn {
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        animation: pulse 2s infinite;
        transition: all 0.3s ease;
    }
    .apply-btn:hover { filter: brightness(1.1); transform: translateY(-2px); }
    
    /* Verdict Boxes */
    .verdict-box { padding: 5px 10px; border-radius: 6px; text-align: center; font-weight: bold; font-size: 0.85rem; }
    .v-danger { background-color: #fdf2f2; color: #d9534f; border: 1px solid #f5c6cb; }
    .v-success { background-color: #eafbf1; color: #28a745; border: 1px solid #c3e6cb; }
    .v-neutral { background-color: #f8f9fa; color: #6c757d; border: 1px solid #dee2e6; }
    </style>
                
    /* 6. TIGHTER DIVIDERS */
    hr {
        margin-top: 0.5rem !important;    /* Default is ~2rem */
        margin-bottom: 0rem !important; /* Default is ~2rem */
        border-top: 1px solid #e0e0e0;    /* Optional: Make it subtle/lighter */
    }
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
        
        st.header("👤 Financial Profile")
        #st.markdown("""<div class="hero-subtext">Rough estimates are perfectly fine. We optimise for patterns, not precision.</div>""", unsafe_allow_html=True)
        st.caption("Rough estimates are perfectly fine. We optimise for patterns, not precision.")
        salary = st.number_input("💰 Monthly Take-Home Salary (₹) ", min_value=0, step=5000, key = "salary",format="%d", help="Your take-home pay after taxes and deductions.")
        
        # with st.expander("👤 More About You"):
        #     h1,h2 = st.columns(2)
        #     with h1 :
        #         age = st.number_input("Age" , min_value = 10 , max_value = 100 , key = "age")
        #     with h2 :
        #         credit_score = st.number_input("Credit Score" , min_value = 300 , max_value = 900 , key = "cibil" , help="\nTo get the credit score for free :  \nGpay :Home > scroll to bottom > Check your CIBIL score.  \nPhonepe: Home > Credit Score")
        # Default values just so that code does not break
        age = 18
        credit_score = 750

        #st.markdown("---")

        sidebar_section_header("💸 Monthly Spends")
        c1, c2 = st.columns(2)
        with c1:
            online = st.number_input(" 🛍️ Online (₹)", min_value=0, max_value=100000, step=1000, key="online", format="%d", help="E-commerce, Subscriptions, Bill Payments")
        with c2:
            offline = st.number_input(" 🛒 Offline (₹)", min_value=0, max_value=100000, step=1000, key="offline", format="%d" , help="In-store, Dining, Groceries")

        travel = st.number_input("✈️ Travel (₹)", min_value=0, max_value=100000, step=1000, key="travel", format="%d" , help="Flights, Hotels, Cabs")

        
        # NEW: Advanced Section for Specialist Cards
        with st.expander("Advanced Spends (Utilities, UPI)"):
            utilities = st.number_input("⚡ Utilities", min_value=0, key="utilities", step=500 , help="Electricity, Recharges, Mobile Bills")
            upi = st.number_input("📱 UPI / Scan & Pay", min_value=0, key="upi", step=500 , help="UPI transactions, QR payments")
        
        

        # Total Summary (Immediate Feedback)
        total = online + travel + offline + utilities + upi
        st.info(f"📝 Total Monthly Spend: **{format_inr(total)}**")
        
        #st.markdown("---")
        # --- ZONE 3: PREFERENCES & ACTION ---
        sidebar_section_header("⚙️ Preferences")
        wants_lounge = st.checkbox(" ✈️ Must have Airport Lounge" , key = "filter_lounge" , help="Filter cards that offer complimentary airport lounge access.")

        # --- NEW SECTION: COMPARISON ---
        #st.markdown("---")
        #st.subheader("🔄 Smart Switch")
        #st.caption("Compare against your current card")
        
        # We add "None" as the default option
        current_card_name = st.selectbox(
            "I currently use:", 
            options=["I don't have a card"] + card_list,
            key="current_card_input" , help="Select to see how much more you could earn."
        )
        # -------------------------------
        st.markdown("###") # Spacer

        calculate_button = st.button("**See My recommendations**", type="primary", key="calculate_btn", help="Card recommendations based on your profile and spends.")

        # st.markdown("### 🤖 AI Settings")
        # enable_ai = st.sidebar.toggle("Enable AI Advisor", key = "enable_ai", help="Get personalized card recommendations using AI analysis.")
        # ask_ai_clicked = False

        # if enable_ai:
        #     if st.sidebar.button("🔮 Ask Gemini for Advice"):
        #         ask_ai_clicked = True # To indicate button was clicked
        ask_ai_clicked = False # For now, we keep the AI feature disabled.
        enable_ai = False # For now disabled the ai feature.
        
    return {
            "age": age,
            "credit_score": credit_score,
        "salary": salary,
        "spends": {"online": online, "travel": travel, "offline": offline, "total": total, "utilities": utilities, "upi": upi},
        "wants_lounge": wants_lounge,
        "enable_ai": enable_ai,
        "ask_ai_clicked": ask_ai_clicked,
        "current_card_name": current_card_name,
        "calculate_button" : calculate_button
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
            delta_text = "Money in your pocket" if annual_net_saving >= 0 else "Cost to you"
            
            # UPDATED METRICS (Human Speak)
            m1, m2, m3 = st.columns(3)
            m1.metric("💰 Yearly Profit", value=format_inr(annual_net_saving), delta=delta_text)
            m2.metric("💳 Annual Fee", format_inr(best_card['Fee']))
            m3.metric("📉 Offline Return", f"{best_card['Base Rate']}%")

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
                    # --- UPDATED HTML FOR THE ALERT ---
                    st.markdown(f"""
                    <div class="money-alert">
                        <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 5px;">
                            💸 Stop Losing Money!
                        </div>
                        You are leaving <b>{format_inr(diff)}</b> on the table every year by using <b>{curr_name}</b>.
                        <br><br>
                        <span style="background-color: rgba(255,255,255,0.6); padding: 2px 6px; border-radius: 4px;">
                            👉 Switching {analogy}
                        </span>
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