import time

import streamlit as st

import ui

import logic

import data_manager

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
        'utilities': 0, 
        'upi': 0        
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Filter Defaults
    if 'filter_lounge' not in st.session_state:
        st.session_state['filter_lounge'] = False
    
    # Initialize the timer if not present
    if 'last_save_time' not in st.session_state:    
        st.session_state['last_save_time'] = 0

    if 'age' not in st.session_state:
        st.session_state['age'] = 25

    if 'cibil' not in st.session_state:
        st.session_state['cibil'] = 700
    
    if 'results_visible' not in st.session_state:
        st.session_state['results_visible'] = False


def reset_inputs():
    """Resets user-editable inputs to defaults and hides results."""
    defaults = {
        "salary": 50000,
        "online": 5000,
        "offline": 2000,
        "travel": 0,
        "utilities": 0,
        "upi": 0,
        "filter_lounge": False,
        "current_card_input": "I don't have a card",
    }
    for key, value in defaults.items():
        st.session_state[key] = value
    st.session_state["results_visible"] = False
# --- 2. MAIN APPLICATION FLOW ---
    

def main():
    # 1. SETUP PAGE (Must be the very first command)

    st.set_page_config(page_title="CredLens", page_icon="💳", layout="wide", initial_sidebar_state= "expanded")

    # Initialize Memory
    init_session_state()

    #st.title("Trust & Transparency Unlocked") # <--- Visual check on screen

    # 2. LOAD CSS (From UI module)
    ui.render_custom_css()

    # 3. RENDER HEADER (Your missing piece!)
    ui.render_header()

    # 4. LOAD DATA (From Data module)
    df = data_manager.load_card_data()

    #Get all card names from dropdown
    all_card_names = df["Card Name"].unique().tolist()

    # 5. RENDER SIDEBAR (And capture inputs)
    # We call the function, and it returns the user's choices
    user_inputs = ui.render_sidebar(all_card_names, reset_callback=reset_inputs)

    #st.write("DEBUG results_visible:", st.session_state["results_visible"])
    #st.write(user_inputs.get("calculate_button") )


    # 6. MAIN LOGIC FLOW

    # --- BUTTON LOGIC START ---
    # Check if button was pressed just now
    show_loading = bool(user_inputs.get("calculate_button"))
    if show_loading:
        st.session_state['results_visible'] = True

    # ONLY Run Main Logic if the flag is True
    if st.session_state["results_visible"]:

        def run_recommendation_flow():
            # A. Filter Cards based on Salary
            valid_cards_local = df[df['Min Income'] <= user_inputs['salary']].copy()
            
            # B. Lounge Filter
            if user_inputs['wants_lounge']:
                valid_cards_local = valid_cards_local[valid_cards_local['Lounge Access'] == 'Yes']

            # C. Calculate Rewards for every card (Using Logic Module)
            valid_cards_local['Net Savings'] = valid_cards_local.apply(
                lambda row: logic.calculate_card_yield(row, user_inputs['spends']), 
                axis=1
            )
            
            # D. Sort Winners
            valid_cards_local = valid_cards_local.sort_values(by='Net Savings', ascending=False)
            return valid_cards_local

        if show_loading:
            with st.spinner("Calculating personalized recommendations..."):
                valid_cards = run_recommendation_flow()
        else:
            valid_cards = run_recommendation_flow()

        # E. Display Results (If cards exist)
        if not valid_cards.empty:
            best_card = valid_cards.iloc[0]

            # --- NEW: SMART COMPARISON LOGIC (3 Scenarios) ---
            comparison_result = None
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
                    current_savings = logic.calculate_card_yield(current_card_row, user_inputs['spends'])
                    current_card_lounge = current_card_row['Lounge Access']
                    diff = best_card['Net Savings'] - current_savings
                    
                    # Only show if there's a real difference
                    if abs(diff) > 100 and current_card_lounge == 'Yes':
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


            # Get AI Verdict (Using Logic Module - Feature Flag Checked)
            if user_inputs["enable_ai"] and user_inputs["ask_ai_clicked"]:
                with st.spinner("🤖 Asking Gemini..."):
                    logic.get_ai_verdict(
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
                valid_cards_df=valid_cards,
                spends = user_inputs["spends"],
                verdict = verdict,
                comparison_data = comparison_result,
                max_spend_dict = user_inputs["max_spend_dict"],
                wants_lounge = user_inputs["wants_lounge"]
            )
            
            # Save Lead (Using Data Module)
            current_time = time.time()
            if current_time - st.session_state["last_save_time"]> 10:

                data_manager.save_lead_to_sheets(
                    salary=user_inputs['salary'],
                    spends=user_inputs['spends'],
                    top_card=best_card['Card Name'],
                    savings=int(best_card['Net Savings'])
                )

                #update the timer
                st.session_state["last_save_time"] = current_time

        else: 
            st.error("😕 No cards found for your salary profile.")
            
    else:
        # Initial State (Before Button Click)
        st.info("👈 Enter your details in the sidebar and click 'See recommendations' to find your perfect card.")
        
        # Optional: Show a "Teaser" image or value prop here to fill empty space
        st.markdown("""
        <div style="text-align: center; color: #888; padding: 50px;">
            <h3>Ready to stop losing money?</h3>
            <p>We analyze hidden fees, reward caps, and your actual spending patterns.</p>
        </div>
        """, unsafe_allow_html=True)
    
        

    # else:
    #     # Initial State
    #     st.info("👈 Enter your details in the sidebar to find your perfect card.")


if __name__ == "__main__":
    main()
