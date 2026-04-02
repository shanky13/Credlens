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
    #milestone_bonus_annual = _calculate_milestone_bonus(row, annual_total_spend, reward_value)
    #annual_reward += milestone_bonus_annual

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
        #"milestone_bonus_annual": milestone_bonus_annual,
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


def build_hero_content(card, spends, max_spend_dict=None, wants_lounge=False, truth_insight=None):
    """
    Returns plain-language hero copy for the winning card.
    This keeps recommendation messaging consistent and out of the UI layer.
    """
    max_spend_dict = max_spend_dict or {}
    truth_insight = truth_insight or {}

    total_spend = _to_float(spends.get("total", 0), 0)
    net_savings = _to_float(card.get("Net Savings", 0), 0)
    fee = _to_float(card.get("Fee", 0), 0)
    annual_total_spend = total_spend * 12
    fee_waived = bool(truth_insight.get("fee_waived", False))
    cap_type = _normalize_text(truth_insight.get("cap_type", card.get("Reward_Cap_Type", "")))
    realization_type = _normalize_text(
        truth_insight.get("realization_type", card.get("Reward_Realization_Type", ""))
    )
    exclusion_categories = truth_insight.get("exclusion_categories", []) or []
    truth_label = str(truth_insight.get("label", "") or "").strip()

    top_category = None
    if max_spend_dict:
        top_category = next(iter(max_spend_dict.keys()))
    elif total_spend > 0:
        spend_priority = {
            "Online": _to_float(spends.get("online", 0), 0),
            "Offline": _to_float(spends.get("offline", 0), 0),
            "Travel": _to_float(spends.get("travel", 0), 0),
            "Utilities": _to_float(spends.get("utilities", 0), 0),
            "UPI": _to_float(spends.get("upi", 0), 0),
        }
        top_category = max(spend_priority, key=spend_priority.get)

    category_copy = {
        "Online": "online shopping",
        "Offline": "offline spending",
        "Travel": "travel",
        "Utilities": "utility payments",
        "UPI": "UPI payments",
    }
    top_category_copy = category_copy.get(top_category, "current spending pattern")
    top_category_spend = 0.0
    if top_category == "Online":
        top_category_spend = _to_float(spends.get("online", 0), 0)
    elif top_category == "Offline":
        top_category_spend = _to_float(spends.get("offline", 0), 0)
    elif top_category == "Travel":
        top_category_spend = _to_float(spends.get("travel", 0), 0)
    elif top_category == "Utilities":
        top_category_spend = _to_float(spends.get("utilities", 0), 0)
    elif top_category == "UPI":
        top_category_spend = _to_float(spends.get("upi", 0), 0)
    top_category_share_pct = (top_category_spend / total_spend * 100.0) if total_spend > 0 and top_category_spend > 0 else 0.0
    why_this_card_source = str(card.get("Pro_Reason", "") or "").strip()
    if not why_this_card_source:
        if fee <= 0:
            why_this_card_source = "It has no annual fee."
        elif fee_waived:
            why_this_card_source = "Its annual fee is waived at your current spend."
        else:
            why_this_card_source = "It matches your current spending mix well."
    elif not why_this_card_source.lower().startswith(("it ", "its ", "this card ", "the card ")):
        why_this_card_source = why_this_card_source[0].upper() + why_this_card_source[1:]
    why_this_card = _first_sentence(why_this_card_source, "It matches your spending well.")

    if top_category_copy == "current spending pattern":
        fit_reason = "Best match for your current spending mix."
    elif top_category_copy.endswith("spending") or top_category_copy.endswith("payments"):
        fit_reason = f"Best for your {top_category_copy}."
    else:
        fit_reason = f"Best for your {top_category_copy} spend."

    if wants_lounge and top_category:
        fit_reason = f"{fit_reason.rstrip('.')} and lounge need."

    if total_spend <= 0:
        context_line = "Add spending to refine this match."
    else:
        context_line = f"Based on {format_inr(total_spend)}/month spend."

    if cap_type in {"monthly_total", "category_cap", "utility_cap", "coins_cap", "milestone"}:
        caution = "Watch out: reward caps can limit extra value if your spending increases."
    elif exclusion_categories:
        caution = (
            f"Watch out: some spending categories do not earn rewards on this card."
        )
    elif fee > 0 and not fee_waived:
        caution = "Watch out: this card only stays worth it if your rewards cover the annual fee."
    elif realization_type in {"portal_locked", "cobrand_wallet", "co_brand_wallet", "basic_points"}:
        caution = "Watch out: part of the value depends on how easily you can redeem the rewards."
    elif net_savings <= 0:
        caution = "Watch out: at your current spend, this card may not create positive net value."
    else:
        caution = "Watch out: this result is strongest if your spending pattern stays similar."

    fee_value = _to_float(card.get("Fee", 0), 0)
    fee_waiver_spend = _to_float(card.get("Fee_Waiver_Spend", float("inf")), float("inf"))
    fee_display = "No annual fee" if fee_value <= 0 else f"{format_inr(fee_value)}/year"
    if fee_value > 0 and fee_waived:
        fee_detail = f"Waived at {format_inr(fee_waiver_spend)} annual spend."
    elif fee_value > 0 and fee_waiver_spend < float("inf"):
        fee_detail = f"Waiver starts at {format_inr(fee_waiver_spend)} annual spend."
    else:
        fee_detail = None

    fee_hook = None
    if fee_value > 0:
        fee_hook = "(See how soon you can waive the fee below.)"

    return {
        "headline_value": format_inr(net_savings),
        "value_subline": "Estimated savings per year",
        "why_this_card": why_this_card,
        "fit_reason": fit_reason,
        "caution": caution,
        "context_line": context_line,
        "hero_type_label": _humanize_reward_type(
            card.get("Reward Type", "") or card.get("Reward_Realization_Type", "")
        ),
        "hero_realization_label": _humanize_realization_type(truth_insight.get("realization_type", "")),
        "truth_label": truth_label,
        "fee_display": fee_display,
        "fee_detail": fee_detail,
        "fee_hook": fee_hook,
        "cta_note": (
            "Annual fee is effectively waived at your current spend."
            if fee > 0 and fee_waived and annual_total_spend > 0
            else None
        ),
    }


def build_recommendation_explanation(card, spends, max_spend_dict=None, truth_insight=None):
    """
    Builds the explanation layer shown directly below the hero.
    It combines user-fit messaging, card metadata, and caution signals.
    """
    max_spend_dict = max_spend_dict or {}
    truth_insight = truth_insight or {}

    total_spend = _to_float(spends.get("total", 0), 0)
    net_savings = _to_float(card.get("Net Savings", 0), 0)
    fee = _to_float(card.get("Fee", 0), 0)
    fee_waived = bool(truth_insight.get("fee_waived", False))
    cap_type = _normalize_text(truth_insight.get("cap_type", card.get("Reward_Cap_Type", "")))
    realization_type = _normalize_text(
        truth_insight.get("realization_type", card.get("Reward_Realization_Type", ""))
    )
    exclusion_categories = truth_insight.get("exclusion_categories", []) or []

    top_category = next(iter(max_spend_dict.keys())) if max_spend_dict else None
    category_copy = {
        "Online": "online shopping",
        "Offline": "offline spending",
        "Travel": "travel",
        "Utilities": "utilities",
        "UPI": "UPI payments",
    }
    top_category_copy = category_copy.get(top_category, "your current spending")

    primary_reason = f"Good match for your {top_category_copy} spend."
    if not top_category:
        primary_reason = "Good match for your current spending."

    supporting_reason = _first_sentence(
        str(card.get("Pro_Reason", "") or "").strip(),
        "That is where this card gives you the most value.",
    )
    if supporting_reason:
        supporting_reason = supporting_reason.rstrip(".") + "."

    caution_lines = []
    if cap_type in {"monthly_total", "category_cap", "utility_cap", "coins_cap", "milestone"}:
        caution_lines.append("Rewards have monthly limits.")
    if exclusion_categories:
        caution_lines.append("Some spending may not earn rewards.")
    if fee > 0 and not fee_waived:
        caution_lines.append("The annual fee still matters.")
    if realization_type in {"portal_locked", "cobrand_wallet", "co_brand_wallet", "basic_points"}:
        caution_lines.append("Redemption may take extra steps.")

    primary_caution = caution_lines[0] if caution_lines else str(card.get("Con_Reason", "") or "").strip()
    if not primary_caution:
        primary_caution = "Value can change if your spending changes."

    secondary_caution = None
    if len(caution_lines) > 1:
        secondary_caution = caution_lines[1]
    elif str(card.get("Con_Reason", "") or "").strip() and primary_caution != str(card.get("Con_Reason", "") or "").strip():
        secondary_caution = str(card.get("Con_Reason", "") or "").strip()

    if total_spend > 0:
        methodology_line = f"Based on {format_inr(total_spend)}/month."
    else:
        methodology_line = "Includes fee, caps, and limits."

    fee_verdict = "Fee looks worth it"
    if fee <= 0 or fee_waived:
        fee_verdict = "Fee is not a blocker"
    elif net_savings <= 0:
        fee_verdict = "Fee may not be worth it"
    elif net_savings < fee:
        fee_verdict = "Fee is borderline"

    return {
        "primary_reason": primary_reason,
        "supporting_reason": supporting_reason,
        "primary_caution": primary_caution,
        "secondary_caution": secondary_caution,
        "methodology_line": methodology_line,
        "fee_verdict": fee_verdict,
    }


def build_value_reality_insight(card, spends, truth_insight=None):
    """
    Builds plain-language cards for explaining how usable the estimated value is in real life.
    """
    truth_insight = truth_insight or {}
    calc = calculate_card_yield_details(card, spends)

    realization_type = _normalize_text(
        truth_insight.get("realization_type", card.get("Reward_Realization_Type", ""))
    )
    cap_type = _normalize_text(truth_insight.get("cap_type", card.get("Reward_Cap_Type", "")))
    exclusion_categories = truth_insight.get("exclusion_categories", []) or []
    fee_waived = bool(calc.get("fee_waived", False) or truth_insight.get("fee_waived", False))
    monthly_cap = _to_float(calc.get("monthly_cap", 0), 0)
    monthly_realized = _to_float(calc.get("monthly_realized_reward", 0), 0)
    annual_spend = _to_float(calc.get("annual_total_spend", 0), 0)
    waiver_spend = _to_float(calc.get("fee_waiver_spend", 0), 0)
    reward_value = _to_float(truth_insight.get("reward_value", card.get("Reward_Value", 1.0)), 1.0)

    flexibility_title = "Rewards"
    flexibility_body = "Rewards are direct cashback."
    if realization_type in {"portal_locked", "cobrand_wallet", "co_brand_wallet"}:
        flexibility_body = "Rewards come through a partner portal."
    elif realization_type in {"travel_transfer"}:
        flexibility_body = "Rewards are best used for travel."
    elif realization_type in {"basic_points", "milestone_based"}:
        flexibility_body = "Rewards come through points."
    elif abs(reward_value - 1.0) > 0.001:
        flexibility_body = f"This estimate already adjusts rewards to about {reward_value:.2f}x of their headline value."

    cap_title = "Reward Limits"
    cap_body = "No major reward cap is reducing this estimate."
    cap_note = None
    cap_progress_pct = None
    cap_progress_label = None
    if monthly_cap > 0 and monthly_cap < 900000:
        if monthly_cap > 0:
            cap_pct = max(0.0, min(100.0, (monthly_realized / monthly_cap) * 100))
            cap_body = (
                f"You have already earned {format_inr(monthly_realized)} of the "
                f"{format_inr(monthly_cap)} monthly reward limit."
            )
            cap_note = "Rewards stop after the monthly reward limit."
            cap_progress_pct = cap_pct
            cap_progress_label = f"{cap_pct:.0f}% of monthly reward limit reached"
    elif cap_type in {"category_cap", "utility_cap", "coins_cap", "milestone"}:
        cap_body = "This card has limits that can reduce value."
        cap_note = "Reward limits apply."
    if exclusion_categories:
        exclusion_label = ", ".join(str(x).title() for x in exclusion_categories[:3])
        cap_body += f" Some spending does not count: {exclusion_label}."

    fee_title = "Fee"
    fee_body = "The annual fee is not hurting your value right now."
    fee_note = None
    fee_progress_pct = None
    fee_progress_label = None
    if waiver_spend > 0 and waiver_spend < 9e8:
        if fee_waived:
            fee_body = "Great news: you already clear the fee waiver."
            fee_note = "Fee waiver removes the annual fee."
            fee_progress_pct = 100
            fee_progress_label = "100% of fee waiver reached"
        else:
            fee_body = f"You have spent {format_inr(annual_spend)} of the {format_inr(waiver_spend)} needed for the fee waiver."
            fee_note = "Fee waiver means no annual fee."
            fee_progress_pct = max(0.0, min(100.0, (annual_spend / waiver_spend) * 100)) if waiver_spend > 0 else None
            if fee_progress_pct is not None:
                fee_progress_label = f"{fee_progress_pct:.0f}% of fee waiver reached"
    elif _to_float(card.get("Fee", 0), 0) > 0 and not fee_waived:
        fee_body = "The annual fee still matters."

    lead_line = "A quick look at rewards, limits, and fee."

    return {
        "lead_line": lead_line,
        "cards": [
            {"title": flexibility_title, "body": flexibility_body},
            {
                "title": cap_title,
                "body": cap_body,
                "note": cap_note,
                "progress_pct": cap_progress_pct,
                "progress_label": cap_progress_label,
            },
            {
                "title": fee_title,
                "body": fee_body,
                "note": fee_note,
                "progress_pct": fee_progress_pct,
                "progress_label": fee_progress_label,
            },
        ],
    }


def _first_sentence(text, fallback=""):
    """Return a short, single-sentence version of a CSV-backed reason string."""
    value = str(text or "").strip()
    if not value:
        return fallback

    for separator in (". ", "? ", "! "):
        if separator in value:
            value = value.split(separator, 1)[0].strip()
            break

    value = value.rstrip(".!?").strip()
    if not value:
        return fallback

    if len(value) > 140:
        value = value[:137].rsplit(" ", 1)[0].rstrip(".!?").strip() + "..."

    return value + "."


def _humanize_reward_type(value):
    """Map internal reward type strings to readable labels."""
    text = _normalize_text(value)
    mapping = {
        "cashback": "Cashback rewards",
        "points": "Points rewards",
        "miles": "Miles rewards",
        "milestone": "Milestone rewards",
        "neucoins": "NeuCoins rewards",
        "basic_points": "Points rewards",
        "milestone_based": "Milestone rewards",
        "portal_locked": "Portal locked",
        "cobrand_wallet": "Co-brand wallet",
        "co_brand_wallet": "Co-brand wallet",
        "travel_transfer": "Travel transfer",
    }
    if text in mapping:
        return mapping[text]
    return str(value or "").replace("_", " ").strip().title() or "Not set"


def _humanize_realization_type(value):
    """Map reward realization strings to a user-facing payout style."""
    text = _normalize_text(value)
    mapping = {
        "cashback": "Direct cashback",
        "points": "Points payout",
        "miles": "Miles payout",
        "milestone_based": "Milestone based",
        "basic_points": "Points payout",
        "portal_locked": "Portal locked",
        "cobrand_wallet": "Co-brand wallet",
        "co_brand_wallet": "Co-brand wallet",
        "travel_transfer": "Travel transfer",
    }
    if text in mapping:
        return mapping[text]
    return str(value or "").replace("_", " ").strip().title() or "Not set"


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
        t.strip().lower() for t in str(raw_value).replace("|", ",").split(",")
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


# def _calculate_milestone_bonus(card, annual_total_spend, reward_value):
#     """
#     Optional milestone bonuses from CSV if columns exist.
#     Supported naming patterns:
#     - Milestone_Threshold / Milestone_Bonus
#     - Milestone_Threshold_1 / Milestone_Bonus_1 ... _2, _3
#     """
#     bonus = 0.0
#     pairs = []

#     if "Milestone_Threshold" in card and "Milestone_Bonus" in card:
#         pairs.append(("Milestone_Threshold", "Milestone_Bonus"))

#     for idx in range(1, 5):
#         t_col = f"Milestone_Threshold_{idx}"
#         b_col = f"Milestone_Bonus_{idx}"
#         if t_col in card and b_col in card:
#             pairs.append((t_col, b_col))

#     for t_col, b_col in pairs:
#         threshold = _to_float(card.get(t_col, 0), 0)
#         raw_bonus = _to_float(card.get(b_col, 0), 0)
#         if threshold > 0 and annual_total_spend >= threshold and raw_bonus > 0:
#             bonus += raw_bonus * (reward_value if reward_value > 0 else 1.0)

#     return bonus


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

def check_current_card(best_card, df, user_inputs):
    # --- NEW: SMART COMPARISON LOGIC (3 Scenarios) ---
    comparison_result = {"type": "no_comparison", "current_card_name": None}  # Default if we can't compare
    current_card_name = user_inputs.get('current_card_name')
    
    # SCENARIO 1: User has NO card (The Nudge)
    if current_card_name == "I don't have a card":
        comparison_result = {
            "type": "no_card"
            
        }
        
    # SCENARIO 2: User ALREADY has the Winner (The Validation)
    elif current_card_name == best_card['Card Name']:
        comparison_result = {
            "type": "same_card",
            "current_card_name": current_card_name
            
        }

    # SCENARIO 3: User has a DIFFERENT card (The Switch Math)
    elif current_card_name:
        # Find the row for the current card in the ORIGINAL dataframe
        
        current_card_row = df[df['Card Name'] == current_card_name]
        # Apply lounge filter if needed
        if user_inputs['wants_lounge']:
            current_card_row = current_card_row[current_card_row['Lounge Access'] == 'Yes'] 
        
        if not current_card_row.empty:
            current_card_row = current_card_row.iloc[0]
            
            # Run the Math
            current_savings = calculate_card_yield(current_card_row, user_inputs['spends'])
            diff = best_card['Net Savings'] - current_savings
            
            # Only show if there's a real difference.
            # Note: lounge eligibility is already handled by the earlier filter when enabled.
            if abs(diff) > 100:
                comparison_result = {
                    "type": "switch",
                    "current_card_name": current_card_name,
                    "diff": int(diff),
                    "current_savings": int(current_savings) 
                }
            else:
                comparison_result = {
                    "type": "same_card",
                    "current_card_name": current_card_name
                }

        else:
            comparison_result = {
                "type": "no_card_lounge",
                "current_card_name": current_card_name
            }

    return comparison_result


# --- MANUAL TEST ZONE ---
if __name__ == "__main__":
    print("🧪 Testing Logic Module...")
    
    # 1. Test Formatting
    print(f"Format Check: 10000 -> {format_inr(10000)}")
    
    # 2. Test AI (Only works if you have API key in secrets, otherwise skips)
    print("✅ Logic Module Valid.")

    print(get_credlens_verdict(100, 500))

    print("Checking exclusions")
    print(_get_excluded_categories("Online, Travel|Dining;Utilities"))
    print(calculate_card_yield_details.category_monthly_reward)
