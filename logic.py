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

def calculate_card_yield_details(row, spends_dict):
    """
    Calculates Net Annual Value using category-aware monthly reward allocation.
    Flow:
    1) Category rewards from monthly spends
    2) Reward exclusions
    3) Reward value normalization
    4) Cap application by cap type
    5) Optional milestone bonus
    6) Fee waiver-adjusted net value
    """
    # 1) Monthly spends per category
    monthly_spends = {
        "online": _to_float(spends_dict.get("online", 0), 0),
        "travel": _to_float(spends_dict.get("travel", 0), 0),
        "dining": _to_float(spends_dict.get("dining", 0), 0),
        "utilities": _to_float(spends_dict.get("utilities", 0), 0),
        "upi": _to_float(spends_dict.get("upi", 0), 0),
        "offline": _to_float(spends_dict.get("offline", 0), 0),
    }

    base_rate = _to_float(row.get("Base Rate", 0), 0)
    category_rates = {
        "online": _to_float(row.get("Online Rate", 0), 0),
        "travel": _to_float(row.get("Travel Rate", 0), 0),
        "dining": _to_float(row.get("Dining Rate", 0), 0),
        "utilities": _to_float(row.get("Utility Rate", base_rate), base_rate),
        "upi": _to_float(row.get("UPI Rate", 0), 0),
        "offline": base_rate,
    }

    # 2) Exclusions: remove rewards from excluded categories.
    excluded = _get_excluded_categories(row.get("Reward_Exclusion_Categories", ""))
    category_monthly_reward = {}
    for cat, spend in monthly_spends.items():
        if cat in excluded:
            category_monthly_reward[cat] = 0.0
        else:
            category_monthly_reward[cat] = spend * (category_rates.get(cat, 0) / 100)

    # 3) Reward value normalization (points/miles/coins -> rupee-realistic).
    reward_value = _to_float(row.get("Reward_Value", 1.0), 1.0)
    if reward_value <= 0:
        reward_value = 1.0
    for cat in category_monthly_reward:
        category_monthly_reward[cat] *= reward_value

    # 4) Cap application on monthly rewards with category-aware allocation.
    monthly_cap = _to_float(row.get("Monthly Cap", 999999), 999999)
    cap_type = _normalize_text(row.get("Reward_Cap_Type", ""))
    if not cap_type:
        cap_type = "none" if monthly_cap >= 900000 else "monthly_total"
    monthly_realized_reward = _apply_monthly_cap(
        category_monthly_reward=category_monthly_reward,
        category_rates=category_rates,
        base_rate=base_rate,
        cap_type=cap_type,
        monthly_cap=monthly_cap,
    )
    annual_reward = monthly_realized_reward * 12

    # 5) Milestone bonuses (if milestone columns exist and thresholds are met).
    annual_total_spend = sum(monthly_spends.values()) * 12
    milestone_bonus_annual = _calculate_milestone_bonus(row, annual_total_spend, reward_value)
    annual_reward += milestone_bonus_annual

    # 6) Fee waiver-adjusted effective fee.
    fee = _to_float(row.get("Fee", 0), 0)
    waiver_spend = _to_float(row.get("Fee_Waiver_Spend", float("inf")), float("inf"))
    effective_fee = 0.0 if annual_total_spend >= waiver_spend else fee

    # 7) Net annual savings.
    net_savings = annual_reward - effective_fee
    return {
        "annual_total_spend": annual_total_spend,
        "fee_waiver_spend": waiver_spend,
        "monthly_raw_reward": sum(category_monthly_reward.values()),
        "monthly_realized_reward": monthly_realized_reward,
        "monthly_cap": monthly_cap,
        "cap_type": cap_type,
        "category_monthly_reward": category_monthly_reward,
        "milestone_bonus_annual": milestone_bonus_annual,
        "annual_reward_before_fee": annual_reward,
        "fee": fee,
        "effective_fee": effective_fee,
        "fee_waived": fee > 0 and effective_fee == 0.0,
        "net_savings": net_savings,
    }


def calculate_card_yield(row, spends_dict):
    """Backward-compatible wrapper for existing call sites."""
    return calculate_card_yield_details(row, spends_dict)["net_savings"]

# 3. AI INTEGRATION
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


def _to_float(value, default=0.0):
    """Best-effort numeric parsing for CSV-backed fields."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _normalize_text(value):
    return str(value or "").strip().lower()


def _get_excluded_categories(raw_value):
    """Parse exclusion categories from CSV into normalized internal keys."""
    if raw_value is None:
        return set()
    tokens = [
        t.strip().lower() for t in str(raw_value).replace(";", ",").split(",")
        if t and str(t).strip()
    ]
    mapping = {
        "online": "online",
        "travel": "travel",
        "dining": "dining",
        "utilities": "utilities",
        "utility": "utilities",
        "upi": "upi",
        "offline": "offline",
        "fuel": "offline",
    }
    result = set()
    for token in tokens:
        if token in mapping:
            result.add(mapping[token])
    return result


def _apply_monthly_cap(category_monthly_reward, category_rates, base_rate, cap_type, monthly_cap):
    """Apply monthly reward cap using category-aware priority allocation."""
    total_reward = sum(category_monthly_reward.values())
    if cap_type in {"none", "no_cap"} or monthly_cap >= 900000:
        return total_reward

    if monthly_cap <= 0:
        return 0.0

    if cap_type == "monthly_total":
        return min(total_reward, monthly_cap)

    if cap_type == "utility_cap":
        utility_part = min(category_monthly_reward.get("utilities", 0.0), monthly_cap)
        other_part = total_reward - category_monthly_reward.get("utilities", 0.0)
        return max(0.0, other_part) + utility_part

    if cap_type in {"category_cap", "coins_cap", "milestone"}:
        # Conservative and transparent approach:
        # apply the cap on total realized monthly rewards.
        # This avoids over-crediting base rewards beyond capped programs.
        return min(total_reward, monthly_cap)

    # Unknown cap type defaults to conservative total cap.
    return min(total_reward, monthly_cap)


def _calculate_milestone_bonus(card, annual_total_spend, reward_value):
    """
    Optional milestone bonuses from CSV if columns exist.
    Supported naming patterns:
    - Milestone_Threshold / Milestone_Bonus
    - Milestone_Threshold_1 / Milestone_Bonus_1 ... _2, _3
    """
    bonus = 0.0
    pairs = []

    if "Milestone_Threshold" in card and "Milestone_Bonus" in card:
        pairs.append(("Milestone_Threshold", "Milestone_Bonus"))

    for idx in range(1, 5):
        t_col = f"Milestone_Threshold_{idx}"
        b_col = f"Milestone_Bonus_{idx}"
        if t_col in card and b_col in card:
            pairs.append((t_col, b_col))

    for t_col, b_col in pairs:
        threshold = _to_float(card.get(t_col, 0), 0)
        raw_bonus = _to_float(card.get(b_col, 0), 0)
        if threshold > 0 and annual_total_spend >= threshold and raw_bonus > 0:
            bonus += raw_bonus * (reward_value if reward_value > 0 else 1.0)

    return bonus


def _clamp_score(score):
    return max(0, min(100, int(round(score))))


def _roi_penalty(net_roi):
    if net_roi > 5000:
        return 0
    if net_roi > 2000:
        return 10
    if net_roi > 0:
        return 25
    return 50


def _reward_friction_penalty(card):
    realization_type = _normalize_text(card.get("Reward_Realization_Type", ""))
    reward_type = _normalize_text(card.get("Reward Type", ""))

    # Primary mapping from explicit Reward_Realization_Type.
    mapping = {
        "cashback": 0,
        "cobrand_wallet": 10,
        "co_brand_wallet": 10,
        "portal_locked": 15,
        "travel_transfer": 10,
        "milestone_based": 20,
        "basic_points": 20,
    }
    if realization_type:
        return mapping.get(realization_type, 10)

    # Backward-compatible inference from Reward Type when explicit column is missing.
    mapping = {
        "cashback": 0,
        "miles": 10,
        "travel": 10,
        "points": 20,
        "milestone": 20,
        "neucoins": 10,
    }
    return mapping.get(reward_type, 10)


def _cap_penalty(card):
    cap_type = _normalize_text(card.get("Reward_Cap_Type", ""))
    monthly_cap = _to_float(card.get("Monthly Cap", 999999), 999999)
    warning_text = _normalize_text(card.get("Warning_Text", ""))

    type_penalty = {
        "none": 0,
        "monthly_total": 10,
        "category_cap": 15,
        "utility_cap": 10,
        "coins_cap": 15,
        "milestone": 10,
    }
    if cap_type:
        penalty = type_penalty.get(cap_type, 10)
    else:
        # Backward-compatible approximation.
        if monthly_cap >= 900000:
            penalty = 0
        elif monthly_cap <= 600:
            penalty = 15
        elif monthly_cap <= 1500:
            penalty = 12
        elif monthly_cap <= 5000:
            penalty = 10
        else:
            penalty = 8

    if "coins cap" in warning_text or "category cap" in warning_text:
        penalty = max(penalty, 15)
    elif "utility cap" in warning_text or "capped" in warning_text or "cap" in warning_text:
        penalty = max(penalty, 10)

    return penalty


def _fee_penalty(card):
    fee = _to_float(card.get("Fee", 0), 0)
    if fee == 0:
        return 0
    if fee < 1000:
        return 5
    if fee < 5000:
        return 10
    return 20


def _effective_fee(card, annual_total_spend):
    fee = _to_float(card.get("Fee", 0), 0)
    waiver_spend = _to_float(card.get("Fee_Waiver_Spend", float("inf")), float("inf"))
    if annual_total_spend >= waiver_spend:
        return 0.0
    return fee


def _devaluation_penalty(card):
    status = _normalize_text(card.get("Status", ""))
    if "devalued" in status:
        return 20
    if "stable" in status:
        return 5
    return 0


def _truth_label(score):
    if score >= 85:
        return "Hidden Gem", "success"
    if score >= 70:
        return "Solid Card", "neutral"
    if score >= 50:
        return "Average Value", "warning"
    if score >= 30:
        return "Overhyped", "danger"
    return "Avoid", "danger"


def assign_credlens_badges(card, truth_score, net_roi):
    """Create compact, user-facing badges from score and card traits."""
    badges = []
    market_rating = _to_float(card.get("Market_Rating", 0), 0)
    fee = _to_float(card.get("Fee", 0), 0)
    status = _normalize_text(card.get("Status", ""))
    online_rate = _to_float(card.get("Online Rate", 0), 0)
    dining_rate = _to_float(card.get("Dining Rate", 0), 0)
    upi_rate = _to_float(card.get("UPI Rate", 0), 0)

    if truth_score >= 85 and net_roi > 3000:
        badges.append({"name": "Hidden Gem", "tone": "good"})
    elif 70 <= truth_score < 85 and net_roi > 0:
        badges.append({"name": "Safe Pick", "tone": "info"})

    if online_rate >= 5:
        badges.append({"name": "Online King", "tone": "category"})
    if dining_rate >= 8:
        badges.append({"name": "Dining King", "tone": "category"})
    if upi_rate >= 1.5:
        badges.append({"name": "UPI King", "tone": "category"})

    if market_rating > 4.3 and truth_score < 60:
        badges.append({"name": "Overhyped", "tone": "warn"})
    if fee > 5000 and truth_score < 70:
        badges.append({"name": "High Fee Risk", "tone": "warn"})
    if "devalued" in status:
        badges.append({"name": "Recently Devalued", "tone": "warn"})

    return badges[:3]


def calculate_truth_score(card, net_roi):
    """
    CredLens Truth Score (0-100):
    100 - ROI - Cap - Reward Friction - Fee - Devaluation
    """
    score = 100
    score -= _roi_penalty(net_roi)
    score -= _cap_penalty(card)
    score -= _reward_friction_penalty(card)
    score -= _fee_penalty(card)
    score -= _devaluation_penalty(card)
    return _clamp_score(score)


def build_credlens_truth_insight(card, monthly_total_spend=0):
    """
    Returns truth score, label, tone and badges for rendering in UI.
    """
    net_roi = _to_float(card.get("Net Savings", 0), 0)
    score = calculate_truth_score(card, net_roi)
    label, tone = _truth_label(score)
    badges = assign_credlens_badges(card, score, net_roi)
    realization_type = _normalize_text(card.get("Reward_Realization_Type", ""))
    cap_type = _normalize_text(card.get("Reward_Cap_Type", ""))
    reward_value = _to_float(card.get("Reward_Value", 1.0), 1.0)
    exclusion_categories = sorted(
        list(_get_excluded_categories(card.get("Reward_Exclusion_Categories", "")))
    )

    annual_total_spend = _to_float(monthly_total_spend, 0) * 12
    effective_fee = _effective_fee(card, annual_total_spend)
    fee = _to_float(card.get("Fee", 0), 0)
    fee_waived = fee > 0 and effective_fee == 0

    return {
        "score": score,
        "label": label,
        "tone": tone,
        "badges": badges,
        "reward_value": reward_value,
        "realization_type": realization_type,
        "cap_type": cap_type,
        "fee_waived": fee_waived,
        "exclusion_categories": exclusion_categories,
    }


# --- MANUAL TEST ZONE ---
if __name__ == "__main__":
    print("🧪 Testing Logic Module...")
    
    # 1. Test Formatting
    print(f"Format Check: 10000 -> {format_inr(10000)}")
    
    # 2. Test AI (Only works if you have API key in secrets, otherwise skips)
    print("✅ Logic Module Valid.")

    print(get_credlens_verdict(100, 500))
