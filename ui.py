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
    <h1 style="font-size:40px; font-weight: 600;margin-top:10px;">CredLens</h1>
    <h3 style="font-size: 28px; font-weight: 500; color: #E5E7EB">Understand what your credit card is actually worth</h3>
    <div class="hero-subtext">
    Based on how you spend — not generic rankings.
    </div>
    """, unsafe_allow_html=True)

    #st.markdown("---")
    st.write("")
    # st.markdown("""
    # <div style = "border-bottom: 1px solid #1F2933;padding-bottom: 20px;margin-bottom: 24px;"> </div>""")
    

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
        font-size: 20px;
        color: white;">
        {title}
    </div>
    """, unsafe_allow_html=True)


# 1. STYLING (CSS)
# ui.py

def render_custom_css():
    st.markdown("""
    <style>
    /* ---------- New UI theme ---------- */             
    :root {
    --bg-surface: #111827;
    --bg-elevated: #1F2937;
    --border-subtle: #374151;

    --text-primary: #E5E7EB;
    --text-secondary: #9CA3AF;

    --accent-blue: #3B82F6;
    --accent-red: #EF4444;
    --accent-green: #22C55E;
    --accent-yellow: #FF9900;
    }
    /* ---------- Section Header ---------- */
    .section-headers {
        font-size: 22px;
        font-weight: 600;
        color: var(--text-primary);
        border-left: 4px solid var(--accent-blue);
        padding: 8px 14px;
        margin: 12px 0;
        background-color: var(--bg-elevated);
        border-radius: 6px;
    }


    .title-card{
    color: #E0E7FF;
    display: inline-block; 
    border: 0px solid #3A2D52; 
    border-radius: 999px; 
    font-size: 24px;
    font-weight: 600;
    padding: 8px 20px; 
    margin-bottom: 15px; /* Controlled margin */
    line-height: 1.2;      /* Centers text vertically */
    background-color: #1E1B4B; /* Subtle background */
    
    }
            
    .section-header{
    color: #E5E7EB;
    display: inline-block; 
    border: 3px solid #3A2D52; 
    border-radius: 999px; 
    border-left: 4px solid #ccc ;
    font-size: 20px;
    font-weight: 600;
    padding: 13px 22px; 
    margin: 5px 0px;       /* Controlled margin */
    line-height: 1.2;      /* Centers text vertically */
    /*background-color: #1B132B;*/ /* Subtle background */
    }
    
    /* ---------- Containers ---------- */
                
    div[class*="st-key-styled_container_"] {
    /*background: var(--bg-surface); */
    background: #262730;
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 32px;
    }

    
    div[class*="st-key-styled_container_back_"] {
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1F2937 100%
        );
    border: 1px solid #374151;
     /* muted red */
    color: #E5E7EB;
    padding: 20px 18px;
    border-radius: 16px;
    margin-bottom: 32px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }

    /* ---------- Alert Box ---------- */
    .alert-box {
        background-color: var(--bg-elevated);
        border: 1px solid var(--border-subtle);
        border-left: 4px solid;
        padding: 16px;
        border-radius: 10px;
        margin: 14px 0;
    }

    .alert-title {
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .alert-muted {
        font-size: 14px;
        color: var(--text-secondary);
    }

    /* Alert variants */
    .alert-info { border-left-color: var(--accent-blue); }
    .alert-warning { border-left-color: var(--accent-yellow); }
    .alert-success { border-left-color: var(--accent-green); }

    /* ---------- Metric Card ---------- */
    .metric-card {
        background-color: var(--bg-elevated);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 14px;
    }

    .metric-label {
        font-size: 13px;
        color: var(--text-secondary);
    }

    .metric-value {
        font-size: 24px;
        font-weight: 600;
        color: var(--text-primary);
    }

    /* ---------- New UI theme close ---------- */
                
    
    /* 1. LAYOUT & SPACING FIXES */
    .block-container {
        padding-top: 3rem !important; /* Reduce top whitespace */
        padding-bottom: 5rem !important;
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
        font-size: 18px;
        font-weight: 400;
        color: #B0B3B8;
        margin-bottom: 1.5rem;
    }
    
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border: 1px solid #3A2D52;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    

    /* 3. THE "MONEY BOX" (Smart Switch Alert) */
    .money-alert {
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1F2937 100%
        );
    border: 1px solid #374151;
     /* muted red */
    color: #E5E7EB;
    padding: 16px 18px;
    border-radius: 15px;
    margin: 16px 0;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
                
    .money-alert--box{background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    color: #E5E7EB;
    border-radius: 16px;
    padding: 15px 20px;
    margin: 5px 0;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    font-size: 18px;
    font-weight: 400;
                }
    
    .money-alert-warning { border-left: 4px solid  var(--accent-yellow); }
    .money-alert-success { border-left: 4px solid  var(--accent-green); }


    .money-alert-title {
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.3px;
        color: #FCA5A5;
        margin-bottom: 6px;
        text-transform: uppercase;
    }

    .money-alert strong {
        color: #FCA5A5;
    }

    .money-alert-muted {
        color: #9CA3AF;
        font-size: 14px;
        margin-top: 6px;
    }

    /* Highlight best card */
    .highlight-card {
    color: #22C55E;      /* green accent */
    font-weight: 700;     /* bold */
    font-size: 18px;      /* slightly bigger */
    }



    
    /* 5. EXISTING STYLES (Kept intact) */
    .status-badge { margin: 0 8px; padding: 5px 10px ; border-radius: 999px; font-weight: bold; font-size: 0.75em; vertical-align: middle; }
    .status-hot { background-color: #FEF3C7; color: #78350F; border: 1px solid #ffeeba; }
    .status-devalued { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .status-stable { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }

    .pro-box {  padding: 10px; border-radius: 6px;border: 0px solid #00b894; border-left: 0px solid #00b894; margin: 8px 0; font-size: 18px;display: block;opacity  : 0.9;} /*background-color: #e6fffa; color: #0f5132; */
    .con-box {  padding: 10px; border-radius: 6px;border: 0px solid #ff7675; border-left: 0px solid #ff7675; margin: 8px 0; font-size: 18px;display: block; opacity: 0.9;} /* background-color: #fff5f5; color: #842029; */

    /* Pulse Button */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(40, 40, 160, 0.4); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 10px rgba(40, 40, 169, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(40, 40, 169, 0); }
    }
    .apply-btn {
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        animation: pulse 2s infinite;
        transition: all 0.3s ease;
    }
    .apply-btn:hover { filter: brightness(1.1); transform: translateY(-2px); }
    
    /* Verdict Boxes */
    .verdict-box { padding: 8px 14px; border-radius: 999px; text-align: center; font-weight: bold; font-size: 18px;display: inline-block;opacity: 0.85;}
    .v-danger { background-color: #fdf2f2; color: #d9534f; border: 1px solid #f5c6cb; }
    .v-success {
    background-color: rgba(34,197,94,0.15);
    color: #22C55E;
    border: 1px solid rgba(34,197,94,0.4);
    }
    .v-neutral { background-color: #f8f9fa; color: #6c757d; border: 1px solid #dee2e6; }
    
                
    /* 6. TIGHTER DIVIDERS - Not working , I guess */
    hr {
        margin-top: 0rem !important;    /* Default is ~2rem */
        margin-bottom: 0rem !important; /* Default is ~2rem */
        border-top: 1px solid #1F2937;;    /* Optional: Make it subtle/lighter */
        margin: 24px 0;
    }

    /* Wrapper controls full layout */
    .card-action-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-top: 10px;
    }

    /* Image styling */
    .credit-card-img {
        width: 260px;
        height: auto;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
        transition: all 0.25s ease;
    }

    .credit-card-img:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 40px rgba(0,0,0,0.45);
    }

    /* Caption */
    .card-caption {
        font-size: 13px;
        color: #9CA3AF;
        text-align: center;
    }

    /* Apply button */
    .apply-link button {
        width: 220px;
    }

    /* Affiliate text */
    .affiliate-text {
        font-size: 12px;
        color: #9CA3AF;
        text-align: center;
    }

    </style>
    """, unsafe_allow_html=True)

def render_section_header(title: str):
    st.markdown(
        f'<div class="section-header">{title}</div>',
        unsafe_allow_html=True
    )


def render_alert(title: str, body: str, variant: str = "info", muted: str = None):
    """
    Renders a styled alert box in Streamlit.
    
    Parameters:
    - title: str -> Main alert title
    - body: str -> HTML/Markdown body text (bold using <strong> or Markdown)
    - variant: str -> "info" | "warning" | "success" (affects border & title color)
    - muted: str -> Optional secondary text below the body, smaller and muted
    """
    
    # Map variant to colors (border-left & title)
    color_map = {
        "info": "#3B82F6",     # Blue
        "warning": "#EF4444",  # Red
        "success": "#22C55E",  # Green
    }
    
    title_color = color_map.get(variant, "#3B82F6")
    
    muted_html = f'<div class="alert-muted" style="margin-top:8px;">{muted}</div>' if muted else ""
    
    st.markdown(f"""
    <div class="alert-box alert-{variant}">
        <div class="alert-title" style="color:{title_color};">
            {title}
        </div>
        <div>{body}</div>
        {muted_html}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )




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
        "SBI": "#1C4D9D",       # Navy Blue
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
    #     # 1. THE HERO IMAGE (New) 🖼️
        st.markdown(
            """
            <style>
            /* Target the image and apply a gradient mask */
            div[data-testid="stImage"] img {
                mask-image: linear-gradient(to bottom, black 85%, transparent 100%);
                -webkit-mask-image: linear-gradient(to bottom, black 85%, transparent 100%);
                width: 180px;
                height: auto;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )
        st.image("hero_image_dark.png", use_container_width=True)
        st.header("👤 Financial Profile")
        st.markdown("""<h5 style="color:#888">Rough estimates are perfectly fine. We optimise for patterns, not precision.</stylev>""", unsafe_allow_html=True)
        #st.caption("Rough estimates are perfectly fine. We optimise for patterns, not precision.")
        with st.container(border=False):
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
            max_spend_cat = None
            spend_data = {"Online": online, "Offline": offline, "Travel": travel, "Utilities": utilities, "UPI": upi}
            max_val = max(spend_data.values())
            max_spend_dict = {cat: val for cat, val in spend_data.items() if val == max_val and val > 0}
            

            st.markdown(f"""<div style="text-align: center; padding: 10px;border-radius: 5px; border: 1px solid #var(--border-subtle); background-color:#2B2E34 ;font-size: 17px;font-weight: 600;">📝 Total Monthly Spend: <b>{format_inr(total)}</b> </div>""", unsafe_allow_html=True)
            st.markdown("###") # Spacer
            #st.markdown("---")
            # --- ZONE 3: PREFERENCES & ACTION ---
            sidebar_section_header("⚙️ Preferences")
            wants_lounge = st.checkbox(" ✈️ Must have Airport Lounge" , key = "filter_lounge" , help="Filter cards that offer complimentary airport lounge access.")

            # --- NEW SECTION: COMPARISON ---

            #st.caption("Compare against your current card")
            
            # We add "None" as the default option
            current_card_name = st.selectbox(
                "I currently use:", 
                options=["I don't have a card"] + card_list,
                key="current_card_input" , help="Select to see how much more you could earn."
            )
            # -------------------------------
            st.markdown("###") # Spacer


            #calculate_button = st.button("**See My recommendations**", type="primary", key="calculate_btn", help="Card recommendations based on your profile and spends.")
            # calculate_button = st.markdown('''
            # <div style="text-align:center; margin-top:10px;">
            #     <button class="apply-btn" style="background-color: #3B82F6; ">
            #     🔍 See My Recommendations
            #     </button>
            # </div>''', unsafe_allow_html=True)

            # Note : Had to create the new button through streamlit as if the up logic was done it was seeting calculate_button to be true always
            st.markdown("""         
            <style>
            div.stButton > button {
                background-color: #3B82F6;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: 600;
                width: 100%;
                animation: pulse 3s ease-in-out ;
            }
            </style>
            """, unsafe_allow_html=True)
            calculate_button = st.button("🔍 See my Recommendations", key="calculate_btn")



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
        "calculate_button" : calculate_button,
        "max_spend_dict": max_spend_dict
        }

# 4. RESULTS DISPLAY (The Heavy Lifter)
def render_results(best_card, break_even_stats, ai_verdict, valid_cards_df, spends, verdict, comparison_data = None,age = 10 , credit_score = 700, approval_odds = 0,max_spend_dict = None):
    """Renders the entire results section (Top Card + Chart + Table). """
    
    #st.markdown("---")
    #Section 1
    
    
    with st.container(key="styled_container_1" , border=False):
        st.markdown(
        f"""
            <div class="title-card">
                Best Card based on your spending 
            </div>
            """, text_alignment= "left",unsafe_allow_html=True
                )
    
        col_det,col_gap,col_action = st.columns([3,0.3,2])
        with col_det:
            # Badge Logic
            status = best_card.get("Status", "Stable")
            s_class = f"status-{status.lower()}" if status.lower() else "stable"
                
            st.markdown(f"<span style='display: inline-block;font-size: 36px;font-weight: 600;padding: 2px ;margin-top: 2px;color: #F9FAFB;letter-spacing: -0.2px;margin-bottom: 8px;'>➤ {best_card['Card Name']} 🏆  <span class='status-badge {s_class}'>{status}</span></span>",text_alignment= "left", unsafe_allow_html=True)
                
            annual_net_saving = best_card['Net Savings']
            #delta_text = "Money in your pocket" if annual_net_saving >= 0 else "Cost to you"
                
            st.markdown(f"""<h4> <span style='color: {"#22C55E" if annual_net_saving >= 0 else "#d9534f"};display: inline-block;font-size: 36px;border: 0.0px solid #ccc; border-radius: 15px; padding: 5px;padding-left: 60px;font-weight:700 '>{format_inr(annual_net_saving)}/year</span></h4>""" ,text_alignment= "left",  unsafe_allow_html=True)
            st.markdown(f"""<div class="hero-subtext" style = "padding-left: 40px;font-weight:400;color:#9CA3AF;margin-bottom:16px; ">💰 Is what you actually gain after fees</div>""" ,text_alignment= "left", unsafe_allow_html=True)

            with st.container(border=False):
                st.markdown(("###"))
                # We round the percentage to 0 decimal places and use <b> tags for bolding
                total = spends["total"]
                percentage = round((list(max_spend_dict.values())[0] / total * 100)) if total > 0 else 0
                category = list(max_spend_dict.keys())[0]

                #st.markdown(f"""<h4>✔ Great for High Salaried with focus on Travel</h4>""" ,text_alignment= "center", unsafe_allow_html=True)
                st.markdown(f"""<h5 style='color:#E5E7EB;;font-weight:500;padding-left: 0px;'>✔ Great for High Salaried with focus on Travel</h5>""" ,text_alignment= "left", unsafe_allow_html=True)
                st.markdown(f"""<h5 style='color:#E5E7EB;;font-weight:500;padding-left: 0px;'>✔ A reasonable choice given your current monthly usage of {format_inr(spends["total"])}</h5>""" ,text_alignment= "left", unsafe_allow_html=True)
                st.markdown(f"""<h5 style='color:#E5E7EB; font-weight:500; padding-left: 0px;'>
                ✔ <b>{percentage}%</b> of your monthly spend is in the <b>{category}</b> spending category.
                </h5>""", 
                unsafe_allow_html=True
)

                #st.markdown(f"""<h4>✔ Kharredle na Bhai!!</h4>""" ,text_alignment= "center", unsafe_allow_html=True)

        with col_action:
            with st.container(border = False):
                
                img_url = best_card.get('Image_URL')
                if pd.notna(img_url):
                    st.markdown(f"""
                    <div class="card-action-wrapper">
                        <img src="{img_url}" class="credit-card-img"/>
                        <div class="card-caption">
                            They rate on features. We rate on Math.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Apply Button
                link = best_card.get('Apply_Link')
                if pd.notna(link):
                    
                    color = get_brand_color(best_card['Card Name'])
                    
                    # We inject the style and class here
                    st.markdown(f"""
                    <div style="text-align:center; margin-top:16px; font-size:15px; font-weight:600; padding:12px 20px; border-radius:10px;">
                        <a href="{link}" target="_blank" style="text-decoration:none;">
                            <button class="apply-btn" style="background-color: {color};">
                                🔗 Apply Now
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption("**Affiliate link, no extra cost to you.**",text_alignment= "center")
                st.write("")

            # 4. CARD: Link 
            search_query = best_card['Card Name'].replace(' ', '+')
            #st.markdown(f"For detailed reviews, [click here](https://www.google.com/search?q={search_query}+reviews).")
            
        
    #st.divider()
    st.write("")
        

    #Section 2
    with st.container( border=False):
        
        
        st.markdown(
        f"""
            <div class="section-header">
            Quick Reality Check
            </div>
            """, text_alignment= "left",unsafe_allow_html=True
                )
        st.write("")

        with st.expander("Click to expand"):
            col1, col2, col3 = st.columns(3)

            st.markdown(" ")
            # 3. Reward Type 
            #if 'Reward Type' in best_card:
                #st.markdown(f"**Type:** {best_card['Reward Type']}")
            col1.metric("💳 Category", best_card['Reward Type'],height="content")
            #col1.metric(label = "This is what we have saved",value=format_inr(annual_net_saving), delta=delta_text, width = "content")
            col2.metric("📈 Annual Fee", format_inr(best_card['Fee']))
            col3.metric("% Base Reward Rate", f"{best_card['Base Rate']}%")

            # --- SMART LOGIC END ---
            with st.container(key="styled_container_back_", border=False):

                #Pros/Cons
                st.markdown("<h3 style='font-weight:500;font-size:18px;color:#888;padding-left:2px;border-radius:3px;'> Why this Card works for you?</h3>", unsafe_allow_html=True)
                #st.markdown(f"""<div class=" hero-subtext"style = "padding-left:30px;color:#9CA3AF;">Why this Card works for you?</div>""", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="money-alert--box money-alert-success" "><b>✅ The Good:</b> {best_card['Pro_Reason']}</div>""",text_alignment= "left", unsafe_allow_html=True)
                st.write("")
                st.markdown("<h3 style='font-weight:500;font-size:18px;color:#888;padding-left:2px;'>Where it falls short?</h3>", unsafe_allow_html=True)
                st.markdown(f"""<div class="money-alert--box money-alert-warning" ><b>⚠️ The Bad:</b> {best_card['Con_Reason']}</div>""",text_alignment= "left", unsafe_allow_html=True)
                st.write(" ")
                st.markdown("<h3 style='font-weight:500;font-size:18px;color:#888;padding-left:2px;'>Fee Reality Check</h3>", unsafe_allow_html=True)
                # Break-Even Bar
                    
                st.markdown(f"""<div class=" hero-subtext"style = "padding-left:30px;color:#9CA3AF;">Break-Even Analysis (Fee: {format_inr(best_card['Fee'])})</div>""", unsafe_allow_html=True)
            
                ##--- SMART LOGIC START ---
                
                if best_card['Fee'] == 0:
                    # CASE 1: Lifetime Free Card
                    st.progress(100, text = " 🎉 **Lifetime Free Card!** You are profitable from Day 1")
                else:
                    # CASE 2: Normal Card (Do the math)
                    # Calculate percent recovered (capped at 100% for the bar)
                    annual_reward = best_card['Net Savings'] + best_card['Fee']
                    annual_reward = max(0, annual_reward)  # Ensure reward is not negative

                    percent_recovered = min(annual_reward/ (best_card['Fee'] ), 1.0)
                    monthly_rewards = annual_reward / 12
                    months_to_break_even = best_card['Fee'] / monthly_rewards

                    if months_to_break_even <= 12:
                        st.progress(float(percent_recovered), text = f" 📈 {int(percent_recovered*100)}% of the annual fee recovered at current monthly expense of {format_inr(spends['total'])} in {int(months_to_break_even)} months.   .")
                        #st.markdown(f"""<div class=" hero-subtext">⏱️ At current monthly spending of {format_inr(spends['total'])} , you will break even in {int(months_to_break_even)} months.</div>""",unsafe_allow_html=True)
                    else:
                        st.progress(float(percent_recovered), text = f" 📈 {int(percent_recovered*100)}% of the annual fee recovered at current monthly expense of {format_inr(spends['total'])}    .")
                        #st.caption("⚠️ At current spending, you may not recover the fee within a year.")

            st.write("")    


    #st.divider()
    st.write("")

    with st.container( border=False):
        st.markdown(
        f"""
            <div class="section-header">
                Market Hype 
            </div>
            """, text_alignment= "left",unsafe_allow_html=True
                )
        st.write("")
        with st.expander("Click to expand"):
            with st.container(key="styled_container_back_2",border=False):
                    # --- NEW: STYLED CONTRAST RATINGS ---
                r1, r2,r3 = st.columns([1,0.3, 1]) # Give Verdict slightly more space
                with r1:
                    with st.container():
                        #st.metric("Market Hype", f"{best_card.get('Market_Rating', 4.5)} ⭐")
                        st.markdown('<h3 style="color:#E0E0E0;font-weight:500;cursor:help ;" title="Based on Net Savings vs Fees">What the internet says?</h3>',text_alignment= "left",unsafe_allow_html=True)
                        
                        #st.markdown("<h3>2️⃣ What the internet says?</h3>", unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size: 25px;font-weight:600;padding-left: 70px; font-weight: bold; cursor: help;" title="Based on Net Savings vs Fees">  {best_card.get("Market_Rating", 4.5)}/5 ⭐</div>',text_alignment= "left",unsafe_allow_html=True)
                        st.write("")
                        st.markdown("<h5 style='font-size: 20px;padding-left: 20px; font-weight: 500;'>➜ Very Popular Card</h5>",text_alignment= "left",unsafe_allow_html=True)
                        st.caption("**Based on average Rating across Cards Affiliate website.**",text_alignment= "left")

                with r3:
                    with st.container(border=False):
                        st.markdown('<h3 style="color:#E0E0E0;font-weight:500;cursor:help ;" title="Based on Net Savings vs Fees">What is the credlens verdict for you?</h5>',text_alignment= "center",unsafe_allow_html=True)
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
                        <div class="verdict-box {v_class} ;">
                            {verdict}
                        </div>
                        """,text_alignment= "center",unsafe_allow_html=True)
                        
                        st.markdown("<h5 style='font-size: 20px;padding-left: 20px; font-weight: 500;'>Popular - but value depends on your spending pattern</h5>",text_alignment= "center",unsafe_allow_html=True)
                        #Hiding feature now based on chatgpt recommendation.
                        #st.markdown(f"<h5> ⚠️ {best_card.get('Warning_Text', 'No specific warnings for this card.')}</h5>",text_alignment= "center",unsafe_allow_html=True)
                        st.caption("**We rate on math, not marketing.**",text_alignment= "center")

    
    # with st.container(border=False):
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.markdown("<h3 style='font-size: 25px;font-weight:500px';color:#E5E7EB;> If this card fits your lifestyle:</h3>",text_alignment= "center",unsafe_allow_html=True)

        # We inject the style and class here
        # st.markdown(f"""
        # <div style="text-align:center; margin:0px;">
        #     <a href="{link}" target="_blank" style="text-decoration:none;">
        #         <button class="apply-btn" style="background-color: {color};">
        #             🔗 Apply Now
        #         </button>
        #     </a>
        # </div>
        # """, unsafe_allow_html=True)
        # st.caption("**Affiliate link, no extra cost to you.**",text_alignment= "center")
    
    #st.divider()
    st.write("")
    

    with st.container(border=False):
        
        st.markdown(
        f"""
            <div class="section-header">
                Current Card Check 🎯
            </div>
            """, text_alignment= "left",unsafe_allow_html=True
                )
        st.write("")

        with st.expander("Click to expand"):
            # --- NEW: SMART CONTEXTUAL ALERTS ---
            if comparison_data:
            
                # 1. THE "NO CARD" NUDGE
                if comparison_data['type'] == 'no_card':
                    st.info(f"""🚀 Select you existing Card in the Profile section OR Start your credit card journey with ***{best_card['Card Name']}***! """)
                    #st.markdown(f"### Start your credit card journey with ***{best_card['Card Name']}***! ")


                # 2. THE "SAME CARD" VALIDATION
                elif comparison_data['type'] == 'same_card' and comparison_data["current_card_name"] == best_card['Card Name']:
                    st.success(f"🎉 **Great Job!** You already own the **{best_card['Card Name']}**. You are maximizing your returns!")
                
                elif comparison_data['type'] == 'same_card' and comparison_data["current_card_name"] != best_card['Card Name']:
                    st.success(f"🎉 **Great Job!** You already own a very good **{comparison_data['current_card_name']}** card. You are maximizing your returns!")

                # 3. THE "lounge access CARD" VALIDATION
                elif comparison_data['type'] == 'no_card_lounge':
                    st.success(f"⚠️ **Your card:** **{comparison_data['current_card_name']}** does not provide lounge access! switch to **{best_card['Card Name']}** to enjoy complimentary lounges. 🛫")

                # 3. THE "SWITCH" WARNING (Existing Logic)
                elif comparison_data['type'] == 'switch':
                    curr_name = comparison_data['current_card_name']
                    diff = comparison_data['diff']

                    # Dynamic analogy
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

                    if diff > 0:

                        st.markdown(f"""
                        <div class="money-alert">
                            <div class="money-alert-title">
                                Opportunity Cost Identified
                            </div>

                        Based on your spending pattern, continuing with **{curr_name}** results in an estimated 
                        annual shortfall of **{format_inr(diff)}**.

                        <div class="money-alert-muted">  
                        * Switching to <span class="highlight-card">{best_card['Card Name']}</span> aligns better with your spend mix.    
                        <br>* 👉  Switching {analogy}
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Negative Diff = The Current Card is ACTUALLY BETTER than our algorithm's pick?
                        # (Rare, but happens if the user selected a Super Premium card we filtered out by salary, or logic quirks)
                        st.markdown(f"✅ <b>Good News!</b> Your current card ({curr_name}) is actually performing great. Your current savings are ->  Current savings: {comparison_data['current_savings']} and best card : {best_card['Card Name']}: {best_card['Net Savings']}. Keep using it!", unsafe_allow_html=True)



    # 5. RESTORED: The Math Expander 
    # This now uses the 'spends' argument we added
    st.markdown("---")
    with st.expander("🧮 How did we calculate this? (The Math)"):
        
        # We build the formula text dynamically so we don't show "0 * 0%" lines
        formula_md = "**The Formula:**\n\n"
        
        # 1. Online
        if spends.get('online', 0) > 0:
            formula_md += f"* **Online(Annual):** {format_inr(spends['online']*12)} × **{best_card.get('Online Rate', 0)}%**\n"
            
        # 2. Utilities (NEW)
        if spends.get('utilities', 0) > 0:
            util_rate = best_card.get('Utility Rate', best_card.get('Base Rate', 0))
            formula_md += f"* **Utilities(Annual):** {format_inr(spends['utilities']*12)} × **{util_rate}%**\n"
            
        # 3. UPI (NEW)
        if spends.get('upi', 0) > 0:
            upi_rate = best_card.get('UPI Rate', 0)
            formula_md += f"* **UPI(Annual):** {format_inr(spends['upi']*12)} × **{upi_rate}%**\n"
            
        # 4. Travel
        if spends.get('travel', 0) > 0:
            formula_md += f"* **Travel(Annual):** {format_inr(spends['travel']*12)} × **{best_card.get('Travel Rate', 0)}%**\n"
            
        # 5. Offline/Base
        if spends.get('offline', 0) > 0:
            formula_md += f"* **Offline(Annual):** {format_inr(spends['offline']*12)} × **{best_card.get('Base Rate', 0)}%**\n"
            
        formula_md += f"\n**Net Calculation(Annual):** `(Total Rewards - Annual Fee) = Profit`"
        
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