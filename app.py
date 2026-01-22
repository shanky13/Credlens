import streamlit as st
print("1. App Started") # <--- Add this

import ui
print("2. UI Imported") # <--- Add this

import logic
print("3. Logic Imported") # <--- Add this

import data_manager
print("4. Data Manager Imported") # <--- Add this

# --- 1. MEMORY INITIALIZATION (New) ---
def init_session_state():
    # Salary Default
    if 'salary' not in st.session_state:
        st.session_state['salary'] = 50000 

    # Spend Categories Defaults
    defaults = {
        'online': 5000,
        'offline': 2000,
        'dining': 1000,
        'travel': 0,
        'utilities': 2000, 
        'upi': 1000        
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Filter Defaults
    if 'filter_lounge' not in st.session_state:
        st.session_state['filter_lounge'] = False

def main():
    # 1. SETUP PAGE (Must be the very first command)

    st.set_page_config(page_title="CredLens", page_icon="💳", layout="wide")

    # Initialize Memory
    init_session_state()

    st.title("Trust & Transparency Unlocked") # <--- Visual check on screen

    # 2. LOAD CSS (From UI module)
    ui.render_custom_css()

    # 3. RENDER HEADER (Your missing piece!)
    ui.render_header()

    # 4. LOAD DATA (From Data module)
    df = data_manager.load_card_data()

    # 5. RENDER SIDEBAR (And capture inputs)
    # We call the function, and it returns the user's choices
    user_inputs = ui.render_sidebar()

    # 6. MAIN LOGIC FLOW
    
        
    # A. Filter Cards based on Salary
    # (Simple pandas filtering can stay here or move to logic.py)
    valid_cards = df[df['Min Income'] <= user_inputs['salary']].copy()
    
    # B. Lounge Filter
    if user_inputs['wants_lounge']:
        valid_cards = valid_cards[valid_cards['Lounge Access'] == 'Yes']

    # C. Calculate Rewards for every card (Using Logic Module)
    # We apply the pure math function to every row
    valid_cards['Net Savings'] = valid_cards.apply(
        lambda row: logic.calculate_card_yield(row, user_inputs['spends']), 
        axis=1
    )
    
    # D. Sort Winners
    valid_cards = valid_cards.sort_values(by='Net Savings', ascending=False)
    
    # E. Display Results (If cards exist)
    if not valid_cards.empty:
        best_card = valid_cards.iloc[0]
        
        # Calculate Break-Even Stats (Using Logic Module)
        be_stats = logic.calculate_break_even_stats(
            fee=best_card['Fee'], 
            net_savings=best_card['Net Savings'], 
            user_total_annual_spend=user_inputs['spends']['total']
        )
        
        # Get AI Verdict (Using Logic Module - Feature Flag Checked)
        ai_text = None
        
        if user_inputs["enable_ai"] and user_inputs["ask_ai_clicked"]:
            with st.spinner("🤖 Asking Gemini..."):
                ai_text = logic.get_ai_verdict(
                    salary=user_inputs['salary'],
                    spends=user_inputs['spends']['total'],
                    card_name=best_card['Card Name'],
                    savings=best_card['Net Savings']
                )

        # 1. Calculate the Verdict (NEW)
        verdict = logic.get_credlens_verdict(
            net_savings=best_card['Net Savings'],
            fee=best_card['Fee']
        )

        # RENDER THE RESULTS (Using UI Module)
        ui.render_results(
            best_card=best_card, 
            break_even_stats=be_stats, 
            ai_verdict=ai_text, 
            valid_cards_df=valid_cards,
            spends = user_inputs["spends"],
            verdict = verdict
        )
        
        # Save Lead (Using Data Module)
        data_manager.save_lead_to_sheets(
            salary=user_inputs['salary'],
            spends=user_inputs['spends'],
            top_card=best_card['Card Name'],
            savings=int(best_card['Net Savings'])
        )
        
    else:
        st.error("😕 No cards found for your salary profile.")

    # else:
    #     # Initial State
    #     st.info("👈 Enter your details in the sidebar to find your perfect card.")


if __name__ == "__main__":
    main()