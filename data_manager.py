import pandas as pd
import gspread
import streamlit as st
from datetime import datetime

# 1. LOAD DATA
@st.cache_data(ttl=60) 
def load_card_data(csv_path: str = "cards.csv") -> pd.DataFrame:
    """
    Reads the raw CSV and applies safety defaults.
    Returns a clean DataFrame ready for analysis.
    """
    try:
        df = pd.read_csv(csv_path)
        
        # Standardize column names (remove accidental spaces)
        df.columns = df.columns.str.strip()
        
        # Safety: Fill missing critical text fields to prevent crashes
        defaults = {
            'Pro_Reason': "Great cashback rates.",
            'Con_Reason': "Check fee waiver limits.",
            'Image_URL': None,
            'Apply_Link': None,
            'Status': "Stable", # Default status for Devaluation Tracker
            'Warning_Text': None
        }
        
        for col, default_val in defaults.items():
            if col not in df.columns:
                df[col] = default_val
        
        # --- TEST DATA INJECTION (Temporary) ---
        # Let's pretend specific cards are Devalued/Hot to test UI
        # In real life, you edit the CSV file directly.
        
        if 'Status' in df.columns:
            # Force 'Axis Magnus' to be Devalued
            df.loc[df['Card Name'].str.contains("Infinia", case=False), 'Status'] = "Devalued"
            df.loc[df['Card Name'].str.contains("Infinia", case=False), 'Warning_Text'] = "Milestones removed. Fees increased to 12.5k."
            
            # Force 'SBI Cashback' to be Hot
            df.loc[df['Card Name'].str.contains("Neu", case=False), 'Status'] = "Hot"
        # ---------------------------------------
        return df
        

    except FileNotFoundError:
        st.error(f"🚨 CRITICAL ERROR: '{csv_path}' not found. Please upload the CSV.")
        return pd.DataFrame() # Return empty DF to prevent app crash

# 2. SAVE DATA (The "Lead Gen" Connector)
def save_lead_to_sheets(salary, spends, top_card, savings):
    """
    Saves user calculation results to Google Sheets for analytics.
    Fails silently so the user experience isn't interrupted.
    """
    try:
        # Check if secrets exist first
        if "gcp_service_account" not in st.secrets:
            return # Skip if running locally without keys
            
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        sh = gc.open("CredLens_Data")
        worksheet = sh.sheet1
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # We only save the total offline/online breakdown to keep it simple
        row = [timestamp, salary, spends['online'], spends['travel'], spends['offline'], top_card, savings]
        
        worksheet.append_row(row)
        
    except Exception as e:
        # Teacher Note: We print to console for us, but don't show error to user
        print(f"Database Save Error: {e}")

# ... existing code ...

# --- MANUAL TEST ZONE ---
if __name__ == "__main__":
    # Note: Streamlit cache functions are hard to test via raw python script 
    # because they expect a running Streamlit thread. 
    # For data_manager, it's often easier to test by importing it in a temp script.
    print("⚠️ Data Manager requires Streamlit context to test full loading.")
    print("✅ Syntax Check Passed.")