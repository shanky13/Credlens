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
    .status-badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em; margin-left: 10px; }
    
    /* 🔥 HOT: Gold/Yellow */
    .status-hot { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
    
    /* 🔻 DEVALUED: Red/Danger (CONFIRMED) */
    .status-devalued { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    
    /* ✅ STABLE: Green/Safe */
    .status-stable { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
                
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
def render_sidebar():
    """Renders the sidebar and returns a dictionary of user inputs."""
    with st.sidebar:
        st.header("⚙️ Financial Profile")
        salary = st.number_input("Monthly Net Salary", value=50000, step=5000, format="%d")
        st.divider()
        
        st.subheader("💸 Monthly Spends")
        c1, c2 = st.columns(2)
        with c1:
            online = st.number_input("Online (₹)", value=10000, step=1000, format="%d")
            travel = st.number_input("Travel (₹)", value=5000, step=1000, format="%d")
        with c2:
            offline = st.number_input("Offline (₹)", value=10000, step=1000, format="%d")

        
        # NEW: Advanced Section for Specialist Cards
        with st.expander("Advanced Spends (Utilities, UPI)"):
            utilities = st.number_input("⚡ Utilities (Bills, Recharge)", min_value=0, value=2000, step=500)
            upi = st.number_input("📱 UPI / Scan & Pay", min_value=0, value=5000, step=500)
        
        total = online + travel + offline + utilities + upi
        st.info(f"Total Monthly Spend: **{format_inr(total)}**")
        st.divider()
        
        wants_lounge = st.checkbox("✅ Must have Airport Lounge")
        
        st.markdown("### 🤖 AI Settings")
        enable_ai = st.toggle("Enable AI Advisor", value=False)
        
        calculate = st.button("Calculate Best Card", type="primary")
        
    return {
        "salary": salary,
        "spends": {"online": online, "travel": travel, "offline": offline, "total": total, "utilities": utilities, "upi": upi},
        "wants_lounge": wants_lounge,
        "enable_ai": enable_ai,
        "calculate_btn": calculate
    }

# 4. RESULTS DISPLAY (The Heavy Lifter)
def render_results(best_card, break_even_stats, ai_verdict, valid_cards_df, spends, verdict):
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
                percent_recovered = min(best_card['Net Savings'] + best_card['Fee'], best_card['Fee']) / best_card['Fee']
                
                # Guardrail: Ensure it doesn't crash if something goes wrong, though Fee != 0 covers it
                if percent_recovered < 0: percent_recovered = 0
                
                bar_color = "green" if percent_recovered >= 1.0 else "red"
                st.progress(float(percent_recovered))
                
                if percent_recovered >= 1.0:
                    st.caption("✅ Fee fully recovered.")
                else:
                    st.caption(f"⚠️ You need to earn **{format_inr(best_card['Fee'] - (best_card['Net Savings'] + best_card['Fee']))}** more to recover the fee.")
            
            # --- SMART LOGIC END ---

            # Pros/Cons
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
            
        
        st.markdown("They rate on features. We rate on **Math**.")


        # 3. Reward Type 
        if 'Reward Type' in best_card:
            st.markdown(f"**Type:** {best_card['Reward Type']}")

        if pd.notna(best_card.get("Warning_Text")):
            st.warning(f"⚠️ {best_card['Warning_Text']}")
        
        # 4. CARD: Link 
        search_query = best_card['Card Name'].replace(' ', '+')
        st.markdown(f"For detailed reviews, [click here](https://www.google.com/search?q={search_query}+reviews).")
            
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