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
    <h1 class="page-title">CredLens</h1>
    <!-- <h2 class="page-subtitle">Understand what your credit card is actually worth</h2> -->
    <h2 class="page-subtitle">Find the best credit card for your spending.</h2>
    <div class="hero-subtext">Based on how you spend - not generic rankings.</div>
    """, unsafe_allow_html=True)

    #st.markdown("---")
    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
    # st.markdown("""
    # <div style = "border-bottom: 1px solid #1F2933;padding-bottom: 20px;margin-bottom: 24px;"> </div>""")
    

# ui.py

def sidebar_section_header(title):
    """
    Renders a tight header with a top border, bypassing Streamlit's default gaps.
    """
    st.markdown(f"""
    <div class="sidebar-section-header">{title}</div>
    """, unsafe_allow_html=True)


# 1. STYLING (CSS)
# ui.py

def render_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap');

    /* ---------- Design tokens ---------- */
    :root {
    --bg-surface: #111827;
    --bg-elevated: #1F2937;
    --border-subtle: #374151;

    --text-primary: #E5E7EB;
    --text-secondary: #9CA3AF;
    --text-tertiary: #6B7280;

    --accent-blue: #3B82F6;
    --accent-red: #EF4444;
    --accent-green: #22C55E;
    --accent-yellow: #FF9900;

    --font-family-base: "Manrope", "Segoe UI", sans-serif;
    --fs-xs: 0.75rem;
    --fs-sm: 0.875rem;
    --fs-md: 1rem;
    --fs-lg: 1.125rem;
    --fs-xl: 1.25rem;
    --fs-2xl: 1.5rem;
    --fs-3xl: 2.75rem;
    --fs-display-lg: 2.25rem;
    --fs-subtitle: 1.75rem;

    --fw-regular: 400;
    --fw-medium: 500;
    --fw-semibold: 600;
    --fw-bold: 700;

    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-7: 2rem;
    --space-8: 2.5rem;
    }

    /* ---------- Typography baseline ---------- */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"] {
        font-family: var(--font-family-base);
    }

    /* Keep Streamlit Material icons on their own font; avoid icon-name text rendering. */
    [class*="material-symbols"], .material-symbols-rounded, .material-symbols-outlined {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: var(--fw-semibold);
        line-height: 1.25;
        margin: 0;
    }

    h1 { font-size: var(--fs-3xl); letter-spacing: -0.02em; }
    h2 { font-size: var(--fs-2xl); }
    h3 { font-size: var(--fs-xl); }
    h4 { font-size: var(--fs-lg); }
    h5 { font-size: var(--fs-md); }

    /* ---------- Shared text utilities ---------- */
    .hero-subtext {
        font-size: var(--fs-lg);
        font-weight: var(--fw-regular);
        color: var(--text-secondary);
        line-height: 1.45;
        margin: 0 0 var(--space-6) 0;
    }

    .muted-text {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .content-heading {
        color: var(--text-secondary);
        font-size: var(--fs-md);
        font-weight: var(--fw-medium);
        margin: 0 0 var(--space-2) 0;
    }

    .insight-line {
        color: var(--text-primary);
        font-size: var(--fs-md);
        font-weight: var(--fw-medium);
        line-height: 1.45;
        margin: 0 0 var(--space-2) 0;
    }

    .spacer-sm { margin-bottom: var(--space-2); }
    .spacer-md { margin-bottom: var(--space-4); }
    .spacer-lg { margin-bottom: var(--space-6); }

    /* ---------- Headline blocks ---------- */
    .page-title {
        font-size: var(--fs-3xl);
        font-weight: var(--fw-semibold);
        margin: var(--space-2) 0 var(--space-2) 0;
    }

    .page-subtitle {
        font-size: var(--fs-subtitle);
        font-weight: var(--fw-medium);
        color: var(--text-primary);
        margin: 0 0 var(--space-3) 0;
    }

    .sidebar-section-header {
        border-top: 1.2px solid #5f6368;
        margin-top: var(--space-2);
        padding-top: var(--space-4);
        margin-bottom: var(--space-4);
        font-weight: var(--fw-semibold);
        font-size: var(--fs-lg);
        color: var(--text-primary);
    }

    /* Keep section titles clearly below the hero in visual hierarchy. */
    .title-card {
        color: #E0E7FF;
        display: inline-block;
        border: 0;
        border-radius: 999px;
        font-size: var(--fs-xl);
        font-weight: var(--fw-semibold);
        padding: var(--space-2) var(--space-5);
        margin-bottom: var(--space-4);
        line-height: 1.2;
        background-color: #1E1B4B;
    }

    .section-header {
        color: var(--text-primary);
        display: inline-block;
        border: 3px solid #3A2D52;
        border-radius: 999px;
        border-left: 4px solid #ccc;
        font-size: var(--fs-xl);
        font-weight: var(--fw-semibold);
        padding: var(--space-3) var(--space-5);
        margin: var(--space-1) 0;
        line-height: 1.2;
    }

    .best-card-name {
        display: inline-block;
        font-size: var(--fs-display-lg);
        font-weight: var(--fw-semibold);
        color: #F9FAFB;
        letter-spacing: -0.01em;
        margin: 0 0 var(--space-2) 0;
    }

    .best-card-value {
        display: inline-block;
        font-size: var(--fs-display-lg);
        font-weight: var(--fw-bold);
        padding: var(--space-2) var(--space-2) var(--space-2) 3.75rem;
        border-radius: 15px;
    }

    .best-card-value.positive { color: var(--accent-green); }
    .best-card-value.negative { color: #d9534f; }

    .total-spend-chip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: var(--space-2);
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid rgba(156, 163, 175, 0.22);
        background: rgba(17, 24, 39, 0.35);
    }

    .total-spend-label {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-medium);
        line-height: 1.3;
    }

    .total-spend-value {
        color: var(--text-primary);
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        line-height: 1.3;
        white-space: nowrap;
    }

    .market-rating-value {
        font-size: var(--fs-xl);
        font-weight: var(--fw-bold);
        line-height: 1.3;
        margin: 0 0 var(--space-2) 0;
    }

    .apply-cta-wrap {
        text-align: center;
        margin-top: var(--space-4);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        padding: var(--space-3) var(--space-5);
        border-radius: 10px;
        --apply-btn-color: #3B82F6;
    }

    .apply-cta-link { text-decoration: none; }
    .apply-cta-wrap .apply-btn { background-color: var(--apply-btn-color); }

    /* ---------- Containers ---------- */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
    }

    .stAlert { padding: var(--space-2) var(--space-4) !important; }
    div[data-testid="stVerticalBlock"] > div { gap: var(--space-2) !important; }

    div[class*="st-key-styled_container_"] {
        background: #262730;
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 32px;
    }

    div[class*="st-key-styled_container_back_"] {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 1px solid #374151;
        color: var(--text-primary);
        padding: 20px 18px;
        border-radius: 16px;
        margin-bottom: 32px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #3A2D52;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
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
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .alert-title-info { color: #3B82F6; }
    .alert-title-warning { color: #EF4444; }
    .alert-title-success { color: #22C55E; }

    .alert-muted {
        font-size: var(--fs-sm);
        color: var(--text-secondary);
    }
    .alert-muted-spaced { margin-top: 8px; }

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
        font-size: var(--fs-sm);
        color: var(--text-secondary);
    }

    .metric-value {
        font-size: var(--fs-2xl);
        font-weight: var(--fw-semibold);
        color: var(--text-primary);
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
    font-size: var(--fs-md);
    font-weight: var(--fw-regular);
    line-height: 1.5;
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
    font-size: var(--fs-md);
    font-weight: var(--fw-regular);
                }
    
    .money-alert-warning { border-left: 4px solid  var(--accent-yellow); }
    .money-alert-success { border-left: 4px solid  var(--accent-green); }


    .money-alert-title {
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
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
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin-top: 6px;
    }

    /* Highlight best card */
    .highlight-card {
    color: #22C55E;      /* green accent */
    font-weight: var(--fw-bold);     /* bold */
    font-size: var(--fs-md);      /* slightly bigger */
    }



    
    /* 5. EXISTING STYLES (Kept intact) */
    .status-badge { margin: 0 8px; padding: 5px 10px ; border-radius: 999px; font-weight: var(--fw-bold); font-size: var(--fs-xs); vertical-align: middle; }
    .status-hot { background-color: #FEF3C7; color: #78350F; border: 1px solid #ffeeba; }
    .status-devalued { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .status-stable { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }

    .pro-box {  padding: 10px; border-radius: 6px;border: 0px solid #00b894; border-left: 0px solid #00b894; margin: 8px 0; font-size: var(--fs-md);display: block;opacity  : 0.9;} /*background-color: #e6fffa; color: #0f5132; */
    .con-box {  padding: 10px; border-radius: 6px;border: 0px solid #ff7675; border-left: 0px solid #ff7675; margin: 8px 0; font-size: var(--fs-md);display: block; opacity: 0.9;} /* background-color: #fff5f5; color: #842029; */

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
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        cursor: pointer;
        animation: pulse 2s infinite;
        transition: all 0.3s ease;
    }
    .apply-btn:hover { filter: brightness(1.1); transform: translateY(-2px); }
    
    /* Verdict Boxes */
    .verdict-box { padding: 8px 14px; border-radius: 999px; text-align: center; font-weight: var(--fw-semibold); font-size: var(--fs-md);display: inline-block;opacity: 0.85;}
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
        font-size: var(--fs-sm);
        color: #9CA3AF;
        text-align: center;
    }

    /* Apply button */
    .apply-link button {
        width: 220px;
    }

    /* Affiliate text */
    .affiliate-text {
        font-size: var(--fs-xs);
        color: #9CA3AF;
        text-align: center;
    }

    .meta-caption {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin: 0;
    }

    .assumption-note {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin: 0 0 var(--space-2) 0;
    }

    /* Comparison panel for market vs personalized verdict. */
    .compare-shell {
        display: flex;
        align-items: stretch;
        justify-content: center;
        gap: var(--space-4);
        margin: var(--space-6) 0;
    }

    .compare-card {
        flex: 1;
        min-height: 220px;
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: var(--space-4);
        display: flex;
        flex-direction: column;
        gap: var(--space-2);
    }

    .compare-badge {
        display: inline-block;
        width: fit-content;
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        color: var(--text-secondary);
        border: 1px solid var(--border-subtle);
        border-radius: 999px;
        padding: 4px 10px;
    }

    .compare-title {
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        color: var(--text-primary);
        line-height: 1.3;
        margin: 0;
    }

    .compare-value {
        font-size: var(--fs-2xl);
        font-weight: var(--fw-bold);
        color: var(--text-primary);
        line-height: 1.2;
        margin: var(--space-1) 0 0 0;
    }

    .compare-note {
        font-size: var(--fs-md);
        font-weight: var(--fw-medium);
        color: var(--text-primary);
        line-height: 1.45;
        margin: 0;
    }

    .compare-source {
        margin-top: auto;
        font-size: var(--fs-sm);
        color: var(--text-secondary);
        line-height: 1.4;
    }

    /* Verdict pill tuning for compare card (prevents full-width stretch in flex column). */
    .compare-card .verdict-box {
        align-self: flex-start;
        width: fit-content;
        max-width: 100%;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.2;
        letter-spacing: 0.01em;
        opacity: 1;
        margin: var(--space-1) 0 0 0;
    }

    .compare-card .verdict-box.v-neutral {
        background: rgba(59, 130, 246, 0.14);
        color: #BFDBFE;
        border: 1px solid rgba(59, 130, 246, 0.5);
    }

    .compare-card .verdict-box.v-success {
        background: rgba(34, 197, 94, 0.16);
        color: #86EFAC;
        border: 1px solid rgba(34, 197, 94, 0.45);
    }

    .compare-card .verdict-box.v-danger {
        background: rgba(239, 68, 68, 0.16);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.45);
    }

    .compare-vs {
        width: 56px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: var(--text-secondary);
        gap: var(--space-2);
    }

    .compare-vs-line {
        width: 1px;
        height: 48px;
        background: var(--border-subtle);
    }

    .compare-vs-text {
        font-size: var(--fs-sm);
        font-weight: var(--fw-bold);
        letter-spacing: 0.08em;
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
        st.header("Financial Profile")
        st.markdown(
        """<div class="muted-text">Rough estimates are fine. We optimize for spending patterns, not exact precision.</div>""",
        unsafe_allow_html=True
        )
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
            sidebar_section_header("Monthly Spends")  
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
            spend_data = {"Online": online, "Offline": offline, "Travel": travel, "Utilities": utilities, "UPI": upi}
            max_val = max(spend_data.values())
            max_spend_dict = {cat: val for cat, val in spend_data.items() if val == max_val and val > 0}
            

            st.markdown(
                f"""
                <div class="total-spend-chip">
                    <div class="total-spend-label">Total Monthly Spend</div>
                    <div class="total-spend-value">{format_inr(total)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            #st.markdown("---")
            # --- ZONE 3: PREFERENCES & ACTION ---
            sidebar_section_header("Preferences")
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
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)


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
                font-size: var(--fs-md);
                font-weight: var(--fw-semibold);
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
def render_results(best_card, valid_cards_df, spends, verdict, comparison_data=None, max_spend_dict=None):
    """Renders the entire results section (Top Card + Chart + Table). """
    
    #st.markdown("---")
    #Section 1
    
    
    with st.container(key="styled_container_1" , border=False):
        st.markdown(
        """
            <div class="title-card">
                Your Top Recommendation
            </div>
            """,unsafe_allow_html=True
                )
    
        col_det,col_gap,col_action = st.columns([3,0.3,2])
        with col_det:
            # Badge Logic
            status = best_card.get("Status", "Stable")
            s_class = f"status-{status.lower()}" if status.lower() else "stable"
                
            st.markdown(
                f"""<div class="best-card-name">➤ {best_card['Card Name']} 🏆
                <span class='status-badge {s_class}'>{status}</span></div>""",
                unsafe_allow_html=True
            )
                
            annual_net_saving = best_card['Net Savings']
            #delta_text = "Money in your pocket" if annual_net_saving >= 0 else "Cost to you"
                
            value_class = "positive" if annual_net_saving >= 0 else "negative"
            st.markdown(
                f"""<div><span class="best-card-value {value_class}">{format_inr(annual_net_saving)}/year</span></div>""",
                unsafe_allow_html=True
            )
            st.markdown(
                """<div class="hero-subtext">💰 Is what you actually gain after fees</div>""",
                unsafe_allow_html=True
            )

            with st.container(border=False):
                st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
                # We round the percentage to 0 decimal places and use <b> tags for bolding
                total = spends["total"]
                percentage = round((list(max_spend_dict.values())[0] / total * 100)) if total > 0 else 0
                category = list(max_spend_dict.keys())[0]

                #st.markdown(f"""<h4>✔ Great for High Salaried with focus on Travel</h4>""" , unsafe_allow_html=True)
                
                st.markdown(
                    """<div class="insight-line">✔ Potential fit if travel is a meaningful part of your spend.</div>""",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""<div class="insight-line">✔ Estimated value reflects your current monthly usage of {format_inr(spends["total"])}.</div>""",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""<div class="insight-line">✔ <b>{percentage}%</b> of your monthly spend is in the <b>{category}</b> spending category.</div>""",
                    unsafe_allow_html=True
                )

                #st.markdown(f"""<h4>✔ Kharredle na Bhai!!</h4>""" , unsafe_allow_html=True)

        with col_action:
            with st.container(border = False):
                
                img_url = best_card.get('Image_URL')
                if pd.notna(img_url):
                    st.markdown(f"""
                    <div class="card-action-wrapper">
                        <img src="{img_url}" class="credit-card-img"/>
                        <div class="card-caption">
                            Comparison uses rewards and fee math.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Apply Button
                link = best_card.get('Apply_Link')
                if pd.notna(link):
                    
                    color = get_brand_color(best_card['Card Name'])
                    
                    # We inject the style and class here
                    st.markdown(f"""
                    <div class="apply-cta-wrap" style="--apply-btn-color: {color};">
                        <a href="{link}" target="_blank" class="apply-cta-link">
                            <button class="apply-btn">
                                🔗 Apply Now
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(
                    """<div class="meta-caption" style = "text-align:center;"><b>Affiliate link, no extra cost to you.</b></div>""",
                    unsafe_allow_html=True
                    )
                st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

            # 4. CARD: Link 
            #st.markdown(f"For detailed reviews, [click here](https://www.google.com/search?q={best_card['Card Name'].replace(' ', '+')}+reviews).")
            
        
    #st.divider()
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        

    #Section 2
    with st.container( border=False):
        
        
        st.markdown(
        """
            <div class="section-header">
            Quick Reality Check
            </div>
            """,unsafe_allow_html=True
                )
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

        with st.expander("Click to expand"):
            col1, col2, col3 = st.columns(3)

            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
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
                st.markdown("""<h3 class="content-heading">Why this card may fit</h3>""", unsafe_allow_html=True)
                #st.markdown(f"""<div class=" hero-subtext"style = "padding-left:30px;color:#9CA3AF;">Why this Card works for you?</div>""", unsafe_allow_html=True)
                st.markdown(
                    f"""<div class="money-alert--box money-alert-success"><b>Potential Upside:</b> {best_card['Pro_Reason']}</div>""",
                    unsafe_allow_html=True
                )
                st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
                st.markdown("""<h3 class="content-heading">Where it may fall short</h3>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="money-alert--box money-alert-warning" ><b>Potential Limitations:</b> {best_card['Con_Reason']}</div>""", unsafe_allow_html=True)
                st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
                st.markdown("""<h3 class="content-heading">Fee Recovery Estimate</h3>""", unsafe_allow_html=True)
                # Break-Even Bar
                    
                st.markdown(
                    f"""<div class="hero-subtext">Break-Even Analysis (Fee: {format_inr(best_card['Fee'])})</div>""",
                    unsafe_allow_html=True
                )
            
                ##--- SMART LOGIC START ---
                
                if best_card['Fee'] == 0:
                    # CASE 1: Lifetime Free Card
                    st.progress(100, text = " **Lifetime Free Card:** You are profitable from day 1.")
                else:
                    # CASE 2: Normal Card (Do the math)
                    # Calculate percent recovered (capped at 100% for the bar)
                    annual_reward = best_card['Net Savings'] + best_card['Fee']
                    annual_reward = max(0, annual_reward)  # Ensure reward is not negative

                    percent_recovered = min(annual_reward/ (best_card['Fee'] ), 1.0)
                    monthly_rewards = annual_reward / 12
                    months_to_break_even = best_card['Fee'] / monthly_rewards

                    if months_to_break_even <= 12:
                        month_count = max(1, int(round(months_to_break_even)))
                        month_label = "month" if month_count == 1 else "months"
                        st.progress(
                            float(percent_recovered),
                            text=f"Fee recovered in ~{month_count} {month_label} at your current spend. Estimated annual fee recovery: {int(percent_recovered*100)}%."
                        )
                        #st.markdown(f"""<div class=" hero-subtext">⏱️ At current monthly spending of {format_inr(spends['total'])} , you will break even in {int(months_to_break_even)} months.</div>""",unsafe_allow_html=True)
                    else:
                        st.progress(
                            float(percent_recovered),
                            text=f"At current spend, you may not recover the full fee within a year. Estimated annual fee recovery: {int(percent_recovered*100)}%."
                        )
                        #st.caption("⚠️ At current spending, you may not recover the fee within a year.")

            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)


    #st.divider()
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

    with st.container( border=False):
        st.markdown(
        """
            <div class="section-header">
                Market vs CredLens
            </div>
            """,unsafe_allow_html=True
                )
        st.markdown("""<div class="meta-caption">Same card, two scoring lenses.</div>""", unsafe_allow_html=True)
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
        with st.expander("Click to expand"):
            with st.container(border=False):
                # Dynamic class for verdict pill tone
                if "Negative" in verdict:
                    v_class = "v-danger"
                elif "Gem" in verdict or "Top" in verdict:
                    v_class = "v-success"
                else:
                    v_class = "v-neutral"

                comparison_html = f"""
<div class="compare-shell">
  <div class="compare-card">
    <span class="compare-badge">Popularity</span>
    <div class="compare-title">Internet Rating</div>
    <div class="compare-value">{best_card.get("Market_Rating", 4.5)}/5 ⭐</div>
    <div class="compare-note">Publicly rated relatively high in listing sites.</div>
    <div class="compare-source">Average public rating from affiliate listings (not personalized).</div>
  </div>

  <div class="compare-vs">
    <div class="compare-vs-line"></div>
    <div class="compare-vs-text">VS</div>
    <div class="compare-vs-line"></div>
  </div>

  <div class="compare-card">
    <span class="compare-badge">Personal Value</span>
    <div class="compare-title">CredLens Verdict</div>
    <div class="verdict-box {v_class}">{verdict}</div>
    <div class="compare-note">Result depends on your input spending pattern.</div>
    <div class="compare-source">Personalized estimate from rewards minus annual fee math.</div>
  </div>
</div>
"""
                st.markdown(comparison_html, unsafe_allow_html=True)

    
    # with st.container(border=False):
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.markdown("<h3 style='font-size: 25px;font-weight:500px';color:#E5E7EB;> If this card fits your lifestyle:</h3>",unsafe_allow_html=True)

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
        # st.caption("**Affiliate link, no extra cost to you.**")
    
    #st.divider()
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    

    with st.container(border=False):
        
        st.markdown(
        """
            <div class="section-header">
                Current Card Check
            </div>
            """,unsafe_allow_html=True
                )
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

        with st.expander("Click to expand"):
            # --- NEW: SMART CONTEXTUAL ALERTS ---
            if comparison_data:
            
                # 1. THE "NO CARD" NUDGE
                if comparison_data['type'] == 'no_card':
                    st.info(f"""Select your current card in the profile section, or start with **{best_card['Card Name']}** based on your current inputs.""")
                    #st.markdown(f"### Start your credit card journey with ***{best_card['Card Name']}***! ")


                # 2. THE "SAME CARD" VALIDATION
                elif comparison_data['type'] == 'same_card' and comparison_data["current_card_name"] == best_card['Card Name']:
                    st.success(f"You already hold **{best_card['Card Name']}**. Based on current inputs, it remains a strong fit.")
                
                elif comparison_data['type'] == 'same_card' and comparison_data["current_card_name"] != best_card['Card Name']:
                    st.success(f"Your current **{comparison_data['current_card_name']}** card is performing comparably for your current spend profile.")

                # 3. THE "lounge access CARD" VALIDATION
                elif comparison_data['type'] == 'no_card_lounge':
                    st.info(f"**{comparison_data['current_card_name']}** does not include lounge access under current filter settings. **{best_card['Card Name']}** is the nearest lounge-compatible fit.")

                # 3. THE "SWITCH" WARNING (Existing Logic)
                elif comparison_data['type'] == 'switch':
                    curr_name = comparison_data['current_card_name']
                    diff = comparison_data['diff']

                    # Dynamic analogy
                    if diff < 2000:
                        analogy = "roughly offsets one to two casual dining bills."
                    elif diff < 5000:
                        analogy = "roughly offsets a year of streaming and Wi-Fi bills."
                    elif diff < 10000:
                        analogy = "roughly offsets a low-cost domestic flight."
                    elif diff < 25000:
                        analogy = "roughly offsets a mid-range phone purchase."
                    elif diff == 0:
                        analogy = "results are effectively similar."
                    else:
                        analogy = "could materially offset a larger annual expense."

                    if diff > 0:

                        st.markdown(f"""
                        <div class="money-alert">
                            <div class="money-alert-title">
                                Estimated Opportunity Cost
                            </div>

                        Based on your spending pattern, continuing with **{curr_name}** results in an estimated 
                        annual shortfall of **{format_inr(diff)}**.

                        <div class="money-alert-muted">  
                        * Switching to <span class="highlight-card">{best_card['Card Name']}</span> aligns better with your spend mix.    
                        <br>* At current inputs, switching {analogy}
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Negative Diff = The Current Card is ACTUALLY BETTER than our algorithm's pick?
                        # (Rare, but happens if the user selected a Super Premium card we filtered out by salary, or logic quirks)
                        st.markdown(f"✅ <b>Current card remains competitive.</b> Your current card (**{curr_name}**) is estimated at {format_inr(comparison_data['current_savings'])} vs **{best_card['Card Name']}** at {format_inr(best_card['Net Savings'])}.", unsafe_allow_html=True)



    # 5. RESTORED: The Math Expander 
    # This now uses the 'spends' argument we added
    st.markdown(
        """<div class="assumption-note">Estimates are derived from your monthly inputs, published reward rates, annual fees, and simplified cap assumptions.</div>""",
        unsafe_allow_html=True
    )
    st.markdown("---")
    with st.expander("How did we calculate this? (The Math)"):
        
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
            
        formula_md += "\n**Net Calculation(Annual):** `(Total Rewards - Annual Fee) = Profit`"
        
        st.markdown(formula_md)

        # 6. FIXED: Chart Height (Fixing Item #5)
        st.subheader("Profitability Comparison")
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
