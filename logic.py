import streamlit as st
from google import genai

# 1. UTILITIES
def format_inr(number):
    """Converts a number (10000) into Indian Format (₹ 10,000)"""
    s, *d = str(int(number)).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return f"₹ {''.join([r] + d)}"

# 2. CORE MATH (Pure Function)
# logic.py

def calculate_card_yield(row, spends_dict):
    """
    Calculates the Net Annual Value with support for Specialist Categories (Utility/UPI).
    Robust against missing CSV columns using .get() defaults.
    """
    
    # 1. ANNUALIZE SPENDS
    # We use .get() to avoid errors if specific keys are missing
    annual_online   = spends_dict.get('online', 0) * 12
    annual_travel   = spends_dict.get('travel', 0) * 12
    annual_dining   = spends_dict.get('dining', 0) * 12
    annual_util     = spends_dict.get('utilities', 0) * 12  # <--- NEW
    annual_upi      = spends_dict.get('upi', 0) * 12        # <--- NEW
    
    # 2. BASE REWARDS CALCULATION (Using specific rates)
    # Note: row.get('Column', default) handles cases where older CSVs might lack the column
    
    reward_online = annual_online * (row.get('Online Rate', 0) / 100)
    reward_travel = annual_travel * (row.get('Travel Rate', 0) / 100)
    reward_dining = annual_dining * (row.get('Dining Rate', 0) / 100)
    
    # SPECIALIST CATEGORIES
    # Default to 'Base Rate' if 'Utility Rate' is missing in CSV
    util_rate = row.get('Utility Rate', row.get('Base Rate', 0))
    reward_util = annual_util * (util_rate / 100)
    
    # Default to 0 if 'UPI Rate' is missing (Most cards give 0 on UPI)
    upi_rate = row.get('UPI Rate', 0)
    reward_upi = annual_upi * (upi_rate / 100)

    # 3. OFFLINE / OTHER CALCULATION
    # Anything not in the buckets above falls into Offline/Base
    annual_offline = spends_dict.get('offline', 0) * 12
    reward_offline = annual_offline * (row.get('Base Rate', 0) / 100)
    
    # 4. TOTAL GROSS REWARD
    raw_total_reward = (
        reward_online + 
        reward_travel + 
        reward_dining + 
        reward_util + 
        reward_upi + 
        reward_offline
    )
    
    # 5. APPLY CAPPING LOGIC
    # Some cards have monthly caps. We approximate this annually.
    # (For exact precision, we would need category-level caps, but this is a safe estimation)
    annual_cap = row.get('Monthly Cap', 999999) * 12
    actual_reward = min(raw_total_reward, annual_cap)
    
    # 6. NET SAVINGS (Profit)
    return actual_reward - row['Fee']

# 3. BREAK-EVEN LOGIC
def calculate_break_even_stats(fee, net_savings, user_total_annual_spend):
    """
    Calculates metrics for the Break-Even Bar.
    """
    if user_total_annual_spend > 0:
        total_earnings = net_savings + fee
        effective_rate = total_earnings / user_total_annual_spend
    else:
        effective_rate = 0
        
    # Calculate Target Spend
    if effective_rate > 0:
        break_even_spend = int(fee / effective_rate)
    else:
        break_even_spend = 9999999 if fee > 0 else 0
        
    # Calculate Progress (0.0 to 1.0)
    if break_even_spend > 0:
        pct_to_breakeven = min(1.0, user_total_annual_spend / break_even_spend)
    else:
        pct_to_breakeven = 1.0 # Already won if fee is 0
        
    return {
        "break_even_spend": break_even_spend,
        "effective_rate": effective_rate,
        "pct_fill": pct_to_breakeven
    }

# 4. AI INTEGRATION
# Note: kept cached to save money/quota
@st.cache_resource(show_spinner=False)
def get_ai_verdict(salary, spends, card_name, savings):
    """
    Calls Gemini to get a witty 1-line review.
    """
    try:
        if "general" not in st.secrets or "gemini_api_key" not in st.secrets["general"]:
            return None # Fail gracefully if no key

        client = genai.Client(api_key=st.secrets["general"]["gemini_api_key"])

        prompt = f"""
        User Spend: {format_inr(spends)}/month. Salary: {format_inr(salary)}.
        Best Card: {card_name} (Saves {format_inr(savings)}/yr).
        Role: Witty financial Advisor
        Task: Write ONE punchy sentence acting as a financial advisor.
        Output: 1 punchy sentence (<20 words).
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash-lite', # Updated to 2.0 as per discussion
            contents=prompt
        )

        return response.text

    except Exception as e:
        # Log error internally but return None so UI doesn't break
        print(f"AI Error: {e}")
        return None
    
# logic.py

def get_credlens_verdict(net_savings, fee):
    """
    Returns a dynamic rating based on mathematical ROI.
    """
    # 1. The Red Flag (Losing Money)
    if net_savings < 0:
        return "⚠️ Negative ROI"
    
    # 2. The Gold Mine (High Multiplier)
    # If the card pays you 3x the fee (e.g., Fee 500, Savings 1500+)
    if fee > 0 and net_savings >= (fee * 3):
        return "💎 Hidden Gem"
    
    # 3. The Free Lunch (Lifetime Free + Profit)
    if fee == 0 and net_savings > 0:
        return "🏆 Top Pick"
        
    # 4. Standard Case
    return "✅ Fair Value"


# --- MANUAL TEST ZONE ---
if __name__ == "__main__":
    print("🧪 Testing Logic Module...")
    
    # 1. Test Formatting
    print(f"Format Check: 10000 -> {format_inr(10000)}")
    
    # 2. Test Break-Even
    stats = calculate_break_even_stats(fee=500, net_savings=2000, user_total_annual_spend=100000)
    print(f"Break-Even Stats: {stats}")
    
    # 3. Test AI (Only works if you have API key in secrets, otherwise skips)
    print("✅ Logic Module Valid.")

    print(get_credlens_verdict(100, 500))

