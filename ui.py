import streamlit as st
import altair as alt
import pandas as pd
import html
import logic
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
    <h2 class="page-subtitle">Find the best credit card for your spending</h2>
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
    --border-card: rgba(156, 163, 175, 0.22);
    --surface-card: rgba(17, 24, 39, 0.34);
    --surface-card-strong: rgba(31, 41, 55, 0.55);
    --radius-card: 12px;

    --text-primary: #E5E7EB;
    --text-secondary: #AEB8C6;
    --text-tertiary: #6B7280;

    --accent-blue: #3B82F6;
    --accent-red: #EF4444;
    --accent-green: #22C55E;
    --accent-yellow: #FF9900;

    --font-family-base: "Manrope", "Segoe UI", sans-serif;
    --fs-xs: 0.8125rem;
    --fs-sm: 0.95rem;
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
        margin-bottom: var(--space-3);
    }

    .content-heading {
        color: var(--text-secondary);
        font-size: var(--fs-md);
        font-weight: var(--fw-medium);
        line-height: 1.4;
        margin: 0 0 var(--space-1) 0;
    }

    .reality-subtext {
        color: var(--text-secondary);
        font-size: var(--fs-md);
        line-height: 1.45;
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
        font-size: var(--fs-md);
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
        display: inline-flex;
        align-items: center;
        border: 1px solid rgba(107, 114, 128, 0.38);
        border-left: 3px solid rgba(96, 165, 250, 0.75);
        border-radius: 10px;
        background: rgba(31, 41, 55, 0.35);
        font-size: var(--fs-lg);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.01em;
        padding: 7px 13px;
        margin: var(--space-2) 0 var(--space-1) 0;
        line-height: 1.2;
    }

    .section-subtitle {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.4;
        margin: 0 0 var(--space-2) 0;
    }

    .best-card-name {
        display: inline-block;
        max-width: 100%;
        word-break: break-word;
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
        padding: 0;
        border-radius: 15px;
        line-height: 1.15;
    }

    .best-card-value.positive { color: var(--accent-green); }
    .best-card-value.negative { color: #d9534f; }

    .best-card-support {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.4;
        margin: var(--space-1) 0 var(--space-2) 0;
    }

    .hero-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 0 0 var(--space-2) 0;
    }

    .hero-meta-chip {
        display: inline-block;
        border: 1px solid rgba(156, 163, 175, 0.24);
        background: rgba(31, 41, 55, 0.45);
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-medium);
        border-radius: 999px;
        padding: 3px 9px;
        line-height: 1.25;
    }

    .hero-fact-row {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: var(--space-2);
        margin: 0 0 var(--space-2) 0;
    }

    .hero-fact-pill {
        border: 1px solid rgba(156, 163, 175, 0.2);
        background: rgba(31, 41, 55, 0.45);
        border-radius: 10px;
        padding: 7px 9px;
    }

    .hero-fact-label {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.3;
        margin: 0 0 2px 0;
    }

    .hero-fact-value {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.35;
        margin: 0;
    }

    .kpi-label {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-medium);
        letter-spacing: 0.01em;
        margin: 0 0 var(--space-1) 0;
    }

    .kpi-subnote {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        margin: var(--space-1) 0 var(--space-3) 0;
    }

    .context-chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-2);
        margin: 0 0 var(--space-3) 0;
    }

    .context-chip {
        font-size: var(--fs-sm);
        color: var(--text-secondary);
        border: 1px solid rgba(156, 163, 175, 0.24);
        background: rgba(17, 24, 39, 0.3);
        border-radius: 999px;
        padding: 5px 10px;
        line-height: 1.35;
        white-space: nowrap;
    }

    .context-chip--travel {
        border-color: rgba(59, 130, 246, 0.45);
        color: #BFDBFE;
        background: rgba(30, 58, 138, 0.25);
    }

    /* Secondary information blocks share one surface language for cleaner scan. */
    .fact-card {
        border: 1px solid var(--border-card);
        background: var(--surface-card);
        border-radius: var(--radius-card);
        padding: 10px 12px;
        margin: 0 0 var(--space-2) 0;
    }

    .fact-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: var(--space-3);
        padding: 6px 0;
        border-bottom: 1px solid rgba(156, 163, 175, 0.16);
    }

    .fact-row:last-child {
        border-bottom: none;
        padding-bottom: 2px;
    }

    .fact-label {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-medium);
        line-height: 1.4;
        white-space: nowrap;
    }

    .fact-value {
        color: var(--text-primary);
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        line-height: 1.4;
        text-align: right;
    }

    .fact-summary {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin: 0;
    }

    .insight-panel {
        border: 1px solid var(--border-card);
        background: var(--surface-card);
        border-radius: var(--radius-card);
        padding: 12px 12px 10px 12px;
        margin: 0 0 var(--space-1) 0;
    }

    .insight-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: var(--space-2);
    }

    @media (max-width: 900px) {
        .insight-grid {
            grid-template-columns: 1fr;
        }
    }

    .insight-item {
        border: 1px solid rgba(156, 163, 175, 0.18);
        background: var(--surface-card-strong);
        border-radius: 10px;
        padding: 10px;
    }

    .insight-item-title {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin: 0 0 4px 0;
    }

    .insight-item-value {
        color: var(--text-primary);
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        line-height: 1.35;
        margin: 0;
    }

    .insight-panel-note {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.4;
        margin: 10px 2px 2px 2px;
    }

    .hero-fit-line {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        margin: 6px 2px 0 2px;
        padding-top: var(--space-2);
        border-top: 1px solid rgba(156, 163, 175, 0.16);
    }

    .hero-fit-label {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-medium);
        margin-right: 2px;
    }

    .hero-fit-pill {
        display: inline-block;
        border-radius: 999px;
        padding: 3px 8px;
        font-size: var(--fs-xs);
        line-height: 1.25;
        border: 1px solid rgba(156, 163, 175, 0.2);
        color: var(--text-secondary);
        background: rgba(17, 24, 39, 0.45);
    }

    .hero-fit-pill--active {
        color: #BFDBFE;
        border-color: rgba(59, 130, 246, 0.45);
        background: rgba(30, 58, 138, 0.25);
    }

    .hero-fit-pill--lounge {
        color: #BFDBFE;
        border-color: rgba(59, 130, 246, 0.45);
        background: rgba(30, 58, 138, 0.25);
    }

    .alt-card-preview {
        border: 1px solid rgba(156, 163, 175, 0.24);
        background: rgba(17, 24, 39, 0.3);
        border-radius: 12px;
        padding: 12px;
        margin: var(--space-3) 0 0 0;
    }

    .alt-card-kicker {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin: 0 0 6px 0;
    }

    .alt-card-name {
        color: var(--text-primary);
        font-size: var(--fs-lg);
        font-weight: var(--fw-semibold);
        line-height: 1.3;
        margin: 0 0 4px 0;
    }

    .alt-card-value {
        color: #BFDBFE;
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        line-height: 1.35;
        margin: 0 0 4px 0;
    }

    .alt-card-gap,
    .alt-card-reason {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin: 0 0 4px 0;
    }

    .fit-panel {
        border: 1px solid var(--border-card);
        background: var(--surface-card);
        border-radius: var(--radius-card);
        padding: 12px;
        margin: 0;
    }

    .fit-metric-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: var(--space-2);
        margin-bottom: var(--space-2);
    }

    .fit-metric-item {
        border: 1px solid rgba(156, 163, 175, 0.18);
        background: var(--surface-card-strong);
        border-radius: 10px;
        padding: 10px;
    }

    .fit-metric-label {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin: 0 0 4px 0;
    }

    .fit-metric-value {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.35;
        margin: 0;
    }

    .fit-row {
        border: 1px solid rgba(156, 163, 175, 0.18);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: var(--space-2);
        background: var(--surface-card-strong);
    }

    .fit-row-positive { border-left: 4px solid var(--accent-green); }
    .fit-row-warning { border-left: 4px solid var(--accent-yellow); }
    .fit-row-neutral { border-left: 4px solid var(--accent-blue); margin-bottom: 0; }

    .fit-row-title {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin: 0 0 4px 0;
    }

    .fit-row-copy {
        color: var(--text-primary);
        font-size: var(--fs-md);
        line-height: 1.45;
        margin: 0;
    }

    .fit-progress-track {
        width: 100%;
        height: 8px;
        border-radius: 999px;
        background: rgba(75, 85, 99, 0.45);
        overflow: hidden;
        margin: 8px 0;
    }

    .fit-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #2563EB 0%, #22C55E 100%);
        border-radius: 999px;
    }

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

    .mini-input-label {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.3;
        margin: 0 0 4px 0;
    }

    .market-rating-value {
        font-size: var(--fs-xl);
        font-weight: var(--fw-bold);
        line-height: 1.3;
        margin: 0 0 var(--space-2) 0;
    }

    .apply-cta-wrap {
        text-align: center;
        margin-top: var(--space-2);
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

    /* Default container surface for most sections (consistent base style). */
    div[class*="st-key-styled_container_"] {
        background: #262730;
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 16px;
    }

    /* Accent container used only for high-emphasis areas (keep usage limited). */
    div[class*="st-key-styled_container_feature_"] {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 1px solid #374151;
        color: var(--text-primary);
        padding: 24px 22px;
        border-radius: 16px;
        margin-bottom: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }

    /* 3. THE "MONEY BOX" (Smart Switch Alert) */
    .money-alert {
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1F2937 100%
        );
    border: 1px solid var(--border-card);
     /* muted red */
    color: #E5E7EB;
    font-size: var(--fs-md);
    font-weight: var(--fw-regular);
    line-height: 1.5;
    padding: 14px 16px;
    border-radius: 15px;
    margin: 12px 0;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
                
    .money-alert--box{background: rgba(17, 24, 39, 0.45);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    border-radius: 12px;
    padding: 12px 14px;
    margin: 5px 0;
    box-shadow: none;
    font-size: var(--fs-md);
    font-weight: var(--fw-regular);
    line-height: 1.45;
                }

    .money-alert--box b {
        color: var(--text-primary);
        font-weight: var(--fw-semibold);
    }

    .fee-outlook-card {
        border: 1px solid var(--border-card);
        background: var(--surface-card);
        border-radius: var(--radius-card);
        padding: 12px 14px;
        margin-top: 6px;
        margin-bottom: 14px;
    }

    .fee-outlook-head {
        display: flex;
        align-items: baseline;
        justify-content: flex-start;
        gap: var(--space-2);
        margin-bottom: 6px;
    }

    .fee-outlook-title {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        margin: 0;
        line-height: 1.35;
    }

    .fee-outlook-status {
        display: inline-block;
        border-radius: 999px;
        padding: 2px 8px;
        font-size: var(--fs-xs);
        line-height: 1.25;
        font-weight: var(--fw-semibold);
        text-transform: uppercase;
        letter-spacing: 0.03em;
        border: 1px solid rgba(156, 163, 175, 0.2);
        color: var(--text-secondary);
        background: rgba(17, 24, 39, 0.45);
        white-space: nowrap;
        margin-left: 0;
    }

    .fee-outlook-status--excellent {
        color: #86EFAC;
        border-color: rgba(34, 197, 94, 0.45);
        background: rgba(20, 83, 45, 0.28);
    }

    .fee-outlook-status--moderate {
        color: #FCD34D;
        border-color: rgba(245, 158, 11, 0.45);
        background: rgba(120, 53, 15, 0.25);
    }

    .fee-outlook-status--weak {
        color: #FCA5A5;
        border-color: rgba(239, 68, 68, 0.45);
        background: rgba(127, 29, 29, 0.25);
    }

    .fee-outlook-bar {
        width: min(320px, 100%);
        height: 8px;
        border-radius: 999px;
        background:
            repeating-linear-gradient(
                to right,
                rgba(148, 163, 184, 0.18) 0,
                rgba(148, 163, 184, 0.18) 1px,
                transparent 1px,
                transparent 25%
            ),
            rgba(75, 85, 99, 0.45);
        overflow: hidden;
        margin: 8px 0;
    }

    .fee-outlook-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563EB 0%, #22C55E 100%);
    }

    .fee-outlook-note {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .fee-outlook-percent {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.35;
        margin: 0 0 6px 0;
    }

    .fee-outlook-timebox {
        border: 1px solid rgba(156, 163, 175, 0.18);
        border-radius: 10px;
        background: rgba(31, 41, 55, 0.45);
        padding: 8px 10px;
        margin: 6px 0 0 0;
    }

    .fee-outlook-timebox-label {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.3;
        margin: 0 0 3px 0;
    }

    .fee-outlook-timebox-value {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.35;
        margin: 0;
    }

    .fee-outlook-scale {
        width: min(320px, 100%);
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.2;
        margin: -2px 0 8px 0;
    }

    .fee-outlook-scale span:nth-child(1) { text-align: left; }
    .fee-outlook-scale span:nth-child(2),
    .fee-outlook-scale span:nth-child(3),
    .fee-outlook-scale span:nth-child(4) { text-align: center; }
    .fee-outlook-scale span:nth-child(5) { text-align: right; }

    .fee-outlook-facts {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: var(--space-2);
        margin: 8px 0 6px 0;
    }

    .fee-outlook-fact {
        border: 1px solid rgba(156, 163, 175, 0.18);
        border-radius: 10px;
        background: rgba(31, 41, 55, 0.45);
        padding: 8px 10px;
    }

    .fee-outlook-fact-label {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-medium);
        margin: 0 0 2px 0;
    }

    .fee-outlook-fact-value {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        margin: 0;
    }

    .fee-outlook-note strong {
        color: var(--text-primary);
        font-weight: var(--fw-semibold);
    }
    
    .money-alert-warning { border-left: 4px solid  var(--accent-yellow); }
    .money-alert-success { border-left: 4px solid  var(--accent-green); }


    .money-alert-title {
        font-size: var(--fs-sm);
        font-weight: var(--fw-medium);
        color: var(--text-secondary);
        margin-bottom: 6px;
    }

    .money-alert strong {
        color: var(--text-primary);
        font-weight: var(--fw-bold);
    }

    .money-alert-muted {
        color: #9CA3AF;
        font-size: var(--fs-xs);
        line-height: 1.45;
        margin-top: 8px;
        font-style: italic;
    }

    .opportunity-amount {
        color: var(--accent-green);
        font-size: var(--fs-2xl);
        font-weight: var(--fw-semibold);
        line-height: 1.2;
        margin: 2px 0 6px 0;
    }

    .opportunity-summary {
        color: var(--text-secondary);
        font-size: var(--fs-md);
        line-height: 1.45;
        margin: 0 0 8px 0;
    }

    .opportunity-row {
        color: var(--text-secondary);
        font-size: var(--fs-md);
        line-height: 1.45;
        margin: 2px 0;
    }

    .opportunity-label {
        color: var(--text-secondary);
        font-weight: var(--fw-medium);
    }

    /* Neutral inline emphasis for card names in switch copy */
    .highlight-card {
        display: inline-block;
        color: var(--text-primary);
        font-weight: var(--fw-bold);
        font-size: var(--fs-sm);
        line-height: 1.2;
        padding: 2px 8px;
        border-radius: 999px;
        border: 1px solid rgba(156, 163, 175, 0.35);
        background: rgba(17, 24, 39, 0.45);
        vertical-align: baseline;
    }

    .opportunity-facts {
        margin: 0 0 var(--space-1) 0;
        padding-left: 1rem;
        color: var(--text-secondary);
    }

    .opportunity-facts li {
        margin: 0 0 4px 0;
        line-height: 1.45;
        font-size: var(--fs-sm);
    }



    
    /* 5. EXISTING STYLES (Kept intact) */
    .status-badge { margin: 0 8px; padding: 5px 10px ; border-radius: 999px; font-weight: var(--fw-bold); font-size: var(--fs-xs); vertical-align: middle; }
    .status-hot { background-color: #FEF3C7; color: #78350F; border: 1px solid #ffeeba; }
    .status-devalued { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .status-stable { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }

    .apply-btn {
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .apply-btn:hover { filter: brightness(1.06); transform: translateY(-1px); }
    
    /* Verdict Boxes */
    .verdict-box { padding: 8px 14px; border-radius: 999px; text-align: center; font-weight: var(--fw-semibold); font-size: var(--fs-md);display: inline-block;opacity: 0.85;}
    .v-danger { background-color: #fdf2f2; color: #d9534f; border: 1px solid #f5c6cb; }
    .v-success {
    background-color: rgba(34,197,94,0.15);
    color: #22C55E;
    border: 1px solid rgba(34,197,94,0.4);
    }
    .v-neutral {
    background-color: rgba(148, 163, 184, 0.14);
    color: #CBD5E1;
    border: 1px solid rgba(148, 163, 184, 0.38);
    }
    
                
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
        gap: 8px;
        margin-top: 4px;
    }

    /* Image styling */
    .credit-card-img {
        width: 210px;
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

    .final-cta-card {
        border: 1px solid var(--border-card);
        background: var(--surface-card);
        border-radius: var(--radius-card);
        padding: 14px;
        margin: 0 0 var(--space-2) 0;
    }

    .final-cta-title {
        color: var(--text-primary);
        font-size: var(--fs-lg);
        font-weight: var(--fw-semibold);
        line-height: 1.3;
        margin: 0 0 6px 0;
    }

    .final-cta-note {
        color: var(--text-secondary);
        font-size: var(--fs-md);
        line-height: 1.45;
        margin: 0 0 10px 0;
    }

    .compare-shell {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: var(--space-3);
        margin: var(--space-2) 0 0 0;
    }

    .compare-card {
        min-height: 0;
        background: var(--surface-card);
        border: 1px solid var(--border-card);
        border-radius: var(--radius-card);
        padding: 12px 14px;
        display: grid;
        grid-template-rows: auto auto minmax(2.2rem, auto) auto auto;
        row-gap: 6px;
        align-content: start;
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
        margin: 2px 0 0 0;
    }

    .compare-note {
        font-size: var(--fs-sm);
        font-weight: var(--fw-regular);
        color: var(--text-secondary);
        line-height: 1.4;
        margin: 2px 0 0 0;
    }

    .compare-source {
        margin-top: var(--space-1);
        font-size: var(--fs-xs);
        color: var(--text-tertiary);
        line-height: 1.4;
    }

    .compare-facts {
        margin: 0;
        padding-left: 16px;
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.4;
    }

    .compare-facts li {
        margin: 0 0 2px 0;
    }

    /* Verdict pill tuning for compare card (prevents full-width stretch in flex column). */
    .compare-card .verdict-box {
        align-self: flex-start;
        width: fit-content;
        max-width: 100%;
        padding: 6px 11px;
        border-radius: 999px;
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.2;
        letter-spacing: 0.01em;
        opacity: 1;
        margin: 0;
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

    .truth-score-line {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin: 2px 0 0 0;
    }

    .truth-score-label {
        font-size: var(--fs-xs);
        color: var(--text-secondary);
        font-weight: var(--fw-medium);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .truth-score-value {
        font-size: var(--fs-lg);
        font-weight: var(--fw-semibold);
        color: var(--text-primary);
        line-height: 1.2;
    }

    .truth-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 2px 0 0 0;
    }

    .truth-badge {
        display: inline-block;
        border-radius: 999px;
        padding: 3px 9px;
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        line-height: 1.25;
        border: 1px solid var(--border-subtle);
        color: var(--text-secondary);
        background: rgba(17, 24, 39, 0.35);
    }

    .truth-badge--good {
        color: #86EFAC;
        border-color: rgba(34, 197, 94, 0.45);
        background: rgba(20, 83, 45, 0.24);
    }

    .truth-badge--info {
        color: #BFDBFE;
        border-color: rgba(59, 130, 246, 0.45);
        background: rgba(30, 58, 138, 0.25);
    }

    .truth-badge--category {
        color: #DDD6FE;
        border-color: rgba(139, 92, 246, 0.45);
        background: rgba(76, 29, 149, 0.25);
    }

    .truth-badge--warn {
        color: #FDE68A;
        border-color: rgba(245, 158, 11, 0.5);
        background: rgba(120, 53, 15, 0.28);
    }

    @media (max-width: 900px) {
        .compare-shell {
            grid-template-columns: 1fr;
            gap: var(--space-2);
        }
    }

    .compare-subtitle {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin: 0 0 var(--space-2) 0;
    }

    button:focus-visible,
    [role="button"]:focus-visible,
    a:focus-visible,
    summary:focus-visible,
    [data-testid="stDataFrame"] *:focus-visible {
        outline: 2px solid #60A5FA !important;
        outline-offset: 2px !important;
        border-radius: 6px;
    }

    .fit-status-chip {
        display: inline-block;
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        color: var(--text-secondary);
        border: 1px solid rgba(156, 163, 175, 0.3);
        border-radius: 999px;
        padding: 4px 10px;
        margin: 0 0 var(--space-2) 0;
        background: rgba(17, 24, 39, 0.35);
    }

    .top3-reco-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: var(--space-2);
        margin: 0 0 var(--space-3) 0;
    }

    .top3-reco-card {
        border: 1px solid var(--border-card);
        background: var(--surface-card);
        border-radius: var(--radius-card);
        padding: 10px 12px;
    }

    .top3-reco-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 6px;
    }

    .top3-reco-thumb-wrap {
        width: 96px;
        height: 60px;
        border-radius: 10px;
        border: 1px solid rgba(156, 163, 175, 0.24);
        background: rgba(31, 41, 55, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        flex-shrink: 0;
    }

    .top3-reco-thumb {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 0;
        display: block;
    }

    .top3-reco-rank {
        display: inline-block;
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: var(--text-secondary);
        border: 1px solid rgba(156, 163, 175, 0.25);
        border-radius: 999px;
        padding: 2px 8px;
        margin: 0 0 8px 0;
        line-height: 1.25;
    }

    .top3-reco-rank--best {
        color: #86EFAC;
        border-color: rgba(34, 197, 94, 0.45);
        background: rgba(20, 83, 45, 0.28);
    }

    .top3-reco-name {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.35;
        margin: 0;
        flex: 1;
        min-width: 0;
    }

    .top3-reco-note {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.35;
        margin: 0 0 6px 0;
        text-align: left;
    }

    .top3-reco-value {
        color: var(--text-primary);
        font-size: var(--fs-md);
        font-weight: var(--fw-semibold);
        line-height: 1.3;
        margin: 0 0 2px 0;
    }

    .top3-reco-fee {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.35;
        margin: 0;
    }

    .top3-reco-metrics {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: var(--space-2);
        margin-top: var(--space-1);
        text-align: left;
    }

    .top3-reco-metric {
        border: 1px solid rgba(156, 163, 175, 0.18);
        background: rgba(31, 41, 55, 0.45);
        border-radius: 8px;
        padding: 6px 8px;
    }

    .top3-reco-metric-label {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.2;
        margin: 0 0 2px 0;
    }

    .top3-reco-metric-value {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.3;
        margin: 0;
    }

    @media (max-width: 900px) {
        .top3-reco-grid {
            grid-template-columns: 1fr;
        }
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
def render_sidebar(card_list, reset_callback=None):
    """Renders the sidebar and returns a dictionary of user inputs."""
    with st.sidebar:
        st.header("Financial Profile")
        st.markdown(
        """<div class="muted-text">Rough estimates are enough. We use patterns in your spending, not exact numbers.</div>""",
        unsafe_allow_html=True
        )
        #st.caption("Rough estimates are perfectly fine. We optimise for patterns, not precision.")
        with st.container(border=False):
            salary = st.number_input("💰 Monthly Salary ₹", min_value=0, step=5000, key = "salary",format="%d", help="Your take-home pay after taxes and deductions.")
            
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
            sidebar_section_header(" Monthly Spends")
            st.markdown(
                """<div class="muted-text">Start with rough values. You can fine-tune later.</div>""",
                unsafe_allow_html=True
            )
            # Keep these horizontal with compact labels above inputs.
            c1, c2 = st.columns(2, gap="small")
            with c1:
                st.markdown("""<div class="mini-input-label">🛍️ Online ₹</div>""", unsafe_allow_html=True)
                online = st.number_input(
                    "Online",
                    min_value=0,
                    max_value=100000,
                    step=1000,
                    key="online",
                    format="%d",
                    help="E-commerce, subscriptions, bill payments",
                    label_visibility="collapsed",
                )
            with c2:
                st.markdown("""<div class="mini-input-label">🛒 Offline ₹</div>""", unsafe_allow_html=True)
                offline = st.number_input(
                    "Offline",
                    min_value=0,
                    max_value=100000,
                    step=1000,
                    key="offline",
                    format="%d",
                    help="In-store, dining, groceries",
                    label_visibility="collapsed",
                )

            travel = st.number_input("✈️ Travel ₹", min_value=0, max_value=100000, step=1000, key="travel", format="%d" , help="Flights, hotels, cabs")

            
            # NEW: Advanced Section for Specialist Cards
            with st.expander("Advanced Spends (Optional)"):
                utilities = st.number_input("⚡ Utilities ₹", min_value=0, key="utilities", step=500 , help="Electricity, recharges, mobile bills")
                upi = st.number_input("📱 UPI / Scan & Pay ₹", min_value=0, key="upi", step=500 , help="UPI transactions, QR payments")

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
            div.st-key-calculate_btn button {
                background-color: #3B82F6;
                color: white;
                padding: 10px 12px;
                border-radius: 8px;
                font-size: var(--fs-sm);
                font-weight: var(--fw-semibold);
                width: 100%;
                min-height: 42px;
                white-space: nowrap;
            }
            div.st-key-reset_btn button {
                background: transparent;
                color: var(--text-secondary);
                border: 1px solid var(--border-subtle);
                padding: 8px 10px;
                border-radius: 8px;
                font-size: var(--fs-sm);
                font-weight: var(--fw-medium);
                width: 100%;
                min-height: 38px;
                white-space: nowrap;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                margin: 8px 0 0 0;
            }
            div.st-key-reset_btn button:hover {
                border-color: #6B7280;
                color: var(--text-primary);
            }
            </style>
            """, unsafe_allow_html=True)
            calculate_button = st.button("🔍 See recommendations", key="calculate_btn", help="View personalized card recommendations")
            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
            reset_button = st.button(
                "Reset inputs",
                key="reset_btn",
                help="Clear all inputs and start fresh.",
                on_click=reset_callback
            )
            



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
def render_results(best_card, valid_cards_df, spends, verdict, truth_insight=None, comparison_data=None, max_spend_dict=None, wants_lounge=False):
    """Renders the entire results section (Top Card + Chart + Table). """

    def render_top3_recommendation_cards(cards_df):
        """Render compact top-3 recommendation tiles."""
        top3_df = cards_df.head(3).copy()
        if top3_df.empty:
            return

        rank_labels = ["Recommended", "Rank #2", "Rank #3"]
        rank_notes = [
            "Highest estimated net value for your current spend profile.",
            "Strong alternate if you prefer a different issuer or rewards style.",
            "Backup option with competitive value for your current inputs.",
        ]
        top3_cards_html = ['<div class="top3-reco-grid">']
        for idx, row in enumerate(top3_df.to_dict("records")):
            rank_label = rank_labels[idx] if idx < len(rank_labels) else f"Rank #{idx + 1}"
            rank_note = rank_notes[idx] if idx < len(rank_notes) else "Alternative card option."
            rank_class = "top3-reco-rank top3-reco-rank--best" if idx == 0 else "top3-reco-rank"
            card_name = html.escape(str(row.get("Card Name", "")))
            net_value = format_inr(row.get("Net Savings", 0))
            fee_value = format_inr(row.get("Fee", 0))
            image_url_raw = row.get("Image_URL")
            image_html = ""
            if pd.notna(image_url_raw):
                image_url = html.escape(str(image_url_raw))
                image_html = (
                    f'<div class="top3-reco-thumb-wrap">'
                    f'<img src="{image_url}" class="top3-reco-thumb" alt="{card_name} card image" loading="lazy"/>'
                    f'</div>'
                )
            top3_cards_html.append(
                f'<div class="top3-reco-card">'
                f'<div class="{rank_class}">{html.escape(rank_label)}</div>'
                f'<div class="top3-reco-head">'
                f'<div class="top3-reco-name">{card_name}</div>'
                f'{image_html}'
                f'</div>'
                f'<div class="top3-reco-note">{html.escape(rank_note)}</div>'
                f'<div class="top3-reco-metrics">'
                f'  <div class="top3-reco-metric">'
                f'    <div class="top3-reco-metric-label">Value</div>'
                f'    <div class="top3-reco-metric-value">{net_value}/year</div>'
                f'  </div>'
                f'  <div class="top3-reco-metric">'
                f'    <div class="top3-reco-metric-label">Fee</div>'
                f'    <div class="top3-reco-metric-value">{fee_value}</div>'
                f'  </div>'
                f'</div>'
                f'</div>'
            )
        top3_cards_html.append("</div>")
        st.markdown("".join(top3_cards_html), unsafe_allow_html=True)
    
    #st.markdown("---")
    #Section 1
    
    
    with st.container(key="styled_container_feature_1" , border=False):
        st.markdown(
        """
            <div class="title-card">
                Your Top Recommendation
            </div>
            """,unsafe_allow_html=True
                )
    
        col_det,col_gap,col_action = st.columns([3,0.3,2])
        with col_det:
            st.markdown(
                f"""<div class="best-card-name">➤ {best_card['Card Name']}</div>""",
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
                """<div class="best-card-support">Net value after annual fee.</div>""",
                unsafe_allow_html=True
            )
            hero_category = html.escape(str(best_card.get("Reward Type", "Card")))
            hero_status = html.escape(str(best_card.get("Status", "Stable")))
            st.markdown(
                f"""
                <div class="hero-meta-row">
                    <span class="hero-meta-chip">Category: {hero_category}</span>
                    <span class="hero-meta-chip">Status: {hero_status}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            total_spend_value = float(spends.get("total", 0) or 0)
            max_spend_dict = max_spend_dict or {}
            if max_spend_dict and total_spend_value > 0:
                top_category, top_value = next(iter(max_spend_dict.items()))
                top_driver_label = f"{html.escape(str(top_category))} ({round((top_value / total_spend_value) * 100)}%)"
            else:
                top_driver_label = "Not enough spend data"
            st.markdown(
                f"""
                <div class="hero-fact-row">
                    <div class="hero-fact-pill">
                        <div class="hero-fact-label">Spend considered</div>
                        <div class="hero-fact-value">{format_inr(total_spend_value)}/month</div>
                    </div>
                    <div class="hero-fact-pill">
                        <div class="hero-fact-label">Top driver</div>
                        <div class="hero-fact-value">{top_driver_label}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            travel_spend = spends.get("travel", 0)
            travel_state = "Travel active" if travel_spend > 0 else "Travel limited"
            lounge_state = "Lounge required" if wants_lounge else "No lounge filter"
            travel_pill_class = "hero-fit-pill hero-fit-pill--active" if travel_spend > 0 else "hero-fit-pill"
            lounge_pill_class = "hero-fit-pill hero-fit-pill--lounge" if wants_lounge else "hero-fit-pill"
            st.markdown(
                f"""
                <div class="hero-fit-line">
                    <span class="hero-fit-label">Travel fit</span>
                    <span class="{travel_pill_class}">{travel_state}</span>
                    <span class="{lounge_pill_class}">{lounge_state}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_action:
            with st.container(border = False):
                
                img_url = best_card.get('Image_URL')
                if pd.notna(img_url):
                    st.markdown(f"""
                    <div class="card-action-wrapper">
                        <img src="{img_url}" class="credit-card-img"/>
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
    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

    # Section 2 (restored): Why This Card Fits
    with st.container(border=False):
        st.markdown(
        """
            <div class="section-header">
            Why This Card Fits
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("""<div class="section-subtitle">Why this card fits your current spending and fee profile.</div>""", unsafe_allow_html=True)
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

        with st.container(border=False):
            st.markdown("""<div class="content-heading">Why this card works for you</div>""", unsafe_allow_html=True)
            st.markdown(
                f"""<div class="money-alert--box money-alert-success"><b>Strength:</b> {best_card['Pro_Reason']}</div>""",
                unsafe_allow_html=True
            )
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            st.markdown("""<div class="content-heading">Watch-outs</div>""", unsafe_allow_html=True)
            st.markdown(
                f"""<div class="money-alert--box money-alert-warning"><b>Limitations:</b> {best_card['Con_Reason']}</div>""",
                unsafe_allow_html=True
            )
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            st.markdown("""<div class="content-heading">Annual fee check</div>""", unsafe_allow_html=True)

            fee_value = float(best_card.get("Fee", 0) or 0)
            spend_value = format_inr(spends.get("total", 0))
            fee_label = format_inr(fee_value)
            annual_reward_raw = max(0.0, float(best_card.get("Net Savings", 0)) + fee_value)

            if fee_value <= 0:
                recovered_pct = 100
                break_even_value = "Month 1"
                recovered_value = fee_label
                status_label = "Excellent"
                status_class = "fee-outlook-status fee-outlook-status--excellent"
                month_estimate_line = "No annual fee, so recovery starts immediately."
                context_line = f"Based on your current spend of <strong>{spend_value}/month</strong>."
            else:
                recovered_ratio = min(annual_reward_raw / fee_value, 1.0)
                recovered_pct = int(round(recovered_ratio * 100))
                monthly_reward = annual_reward_raw / 12
                recovered_value = format_inr((recovered_pct / 100) * fee_value)

                if monthly_reward <= 0:
                    break_even_value = ">12 months"
                    month_estimate_line = "Estimated full fee recovery may take over 12 months."
                    context_line = f"At <strong>{spend_value}/month</strong>, rewards may not fully cover the annual fee."
                else:
                    months_to_break_even = fee_value / monthly_reward
                    if months_to_break_even <= 12:
                        month_count = max(1, int(round(months_to_break_even)))
                        month_label = "month" if month_count == 1 else "months"
                        break_even_value = f"~{month_count} {month_label}"
                        month_estimate_line = f"You are likely to recover the full fee in {break_even_value}."
                    else:
                        break_even_value = ">12 months"
                        month_estimate_line = "Full fee recovery may take over 12 months."
                    context_line = f"Based on your current spend of <strong>{spend_value}/month</strong>."

                if recovered_pct >= 90:
                    status_label = "Excellent"
                    status_class = "fee-outlook-status fee-outlook-status--excellent"
                elif recovered_pct >= 60:
                    status_label = "Moderate"
                    status_class = "fee-outlook-status fee-outlook-status--moderate"
                else:
                    status_label = "Weak"
                    status_class = "fee-outlook-status fee-outlook-status--weak"

            st.markdown(
                f"""
                <div class="fee-outlook-card">
                    <div class="fee-outlook-head">
                    <div class="fee-outlook-title">Annual fee recovery</div>
                        <div class="{status_class}">{status_label}</div>
                    </div>
                    <div class="fee-outlook-percent">Recovered this year: <strong>{recovered_value}</strong> of <strong>{fee_label}</strong></div>
                    <div class="fee-outlook-bar">
                        <div class="fee-outlook-fill" style="width: {recovered_pct}%;"></div>
                    </div>
                    <div class="fee-outlook-timebox">
                        <div class="fee-outlook-timebox-value">{month_estimate_line}</div>
                    </div>
                    <div class="fee-outlook-note">{context_line}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

    #st.divider()
    with st.container( border=False):
        st.markdown(
        """
            <div class="section-header">
                Popularity vs Personal Value
            </div>
            """,unsafe_allow_html=True
                )
        st.markdown("""<div class="section-subtitle">Public rating vs your personal value from this card.</div>""", unsafe_allow_html=True)
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
        with st.container(border=False):
            # Dynamic class for verdict pill tone
            if truth_insight and truth_insight.get("tone") == "danger":
                v_class = "v-danger"
            elif truth_insight and truth_insight.get("tone") == "success":
                v_class = "v-success"
            elif "Negative" in verdict:
                v_class = "v-danger"
            elif "Gem" in verdict or "Top" in verdict:
                v_class = "v-success"
            else:
                v_class = "v-neutral"

            market_rating_raw = best_card.get("Market_Rating", 4.5)
            try:
                market_rating_value = float(market_rating_raw)
                if pd.isna(market_rating_value):
                    market_rating_value = 4.5
            except (TypeError, ValueError):
                market_rating_value = 4.5

            truth_score = None
            truth_label = verdict
            truth_badges_html = ""
            truth_facts_html = ""
            quick_win_html = ""
            calc_quick = logic.calculate_card_yield_details(best_card, spends)
            if truth_insight:
                truth_score = truth_insight.get("score")
                truth_label = truth_insight.get("label", verdict)
                badge_chunks = []
                for badge in truth_insight.get("badges", []):
                    badge_name = html.escape(str(badge.get("name", "")))
                    badge_tone = html.escape(str(badge.get("tone", "")))
                    badge_chunks.append(
                        f'<span class="truth-badge truth-badge--{badge_tone}">{badge_name}</span>'
                    )
                truth_badges_html = "".join(badge_chunks)

                realization_type = str(truth_insight.get("realization_type", "") or "").strip().lower()
                cap_type = str(truth_insight.get("cap_type", "") or "").strip().lower()
                reward_value = truth_insight.get("reward_value", 1.0)
                fee_waived = bool(truth_insight.get("fee_waived", False))
                exclusion_categories = truth_insight.get("exclusion_categories", []) or []

                realization_copy = {
                    "cashback": "Rewards are direct cashback (easy to redeem).",
                    "portal_locked": "Rewards are mainly usable inside issuer portal.",
                    "travel_transfer": "Best value often needs travel transfer redemption.",
                    "cobrand_wallet": "Rewards are mostly locked to partner ecosystem.",
                    "co_brand_wallet": "Rewards are mostly locked to partner ecosystem.",
                    "milestone_based": "Benefits depend on hitting milestone spend.",
                    "basic_points": "Rewards are generic points with lower redemption ease.",
                }
                cap_copy = {
                    "none": "No major reward cap is applied in this estimate.",
                    "monthly_total": "Monthly total reward cap can limit upside.",
                    "category_cap": "Category-specific caps can reduce realized value.",
                    "utility_cap": "Utility rewards are capped for this card.",
                    "coins_cap": "Coin caps can restrict effective rewards.",
                    "milestone": "Milestone gates can delay/limit reward realization.",
                }

                fact_items = []
                try:
                    rv = float(reward_value)
                    if abs(rv - 1.0) > 0.001:
                        fact_items.append(
                            f"Reward value adjusted to <strong>{rv:.2f}x</strong> to reflect realistic redemption."
                        )
                except (TypeError, ValueError):
                    pass

                if realization_type in realization_copy:
                    fact_items.append(realization_copy[realization_type])
                if cap_type in cap_copy:
                    fact_items.append(cap_copy[cap_type])
                if fee_waived:
                    fact_items.append("At your current spend, annual fee is treated as waived.")
                if exclusion_categories:
                    exclusion_label = ", ".join(str(x).title() for x in exclusion_categories[:3])
                    fact_items.append(f"Reward exclusions applied: {html.escape(exclusion_label)}.")

                if fact_items:
                    list_items = "".join(f"<li>{item}</li>" for item in fact_items[:3])
                    truth_facts_html = f'<ul class="compare-facts">{list_items}</ul>'

            # Quick-win insight strip: cap usage, fee waiver progress, top reward driver.
            quick_items = []
            monthly_cap = float(calc_quick.get("monthly_cap", 0) or 0)
            monthly_realized = float(calc_quick.get("monthly_realized_reward", 0) or 0)
            cap_type = str(calc_quick.get("cap_type", "none") or "none").lower()

            if monthly_cap > 0 and monthly_cap < 900000:
                cap_pct = max(0.0, min(100.0, (monthly_realized / monthly_cap) * 100)) if monthly_cap > 0 else 0.0
                quick_items.append(
                    f"Cap usage: <strong>{cap_pct:.0f}%</strong> of {format_inr(monthly_cap)}/month ({html.escape(cap_type.replace('_', ' '))})."
                )
            else:
                quick_items.append("Cap usage: No meaningful monthly cap in this estimate.")

            annual_spend = float(calc_quick.get("annual_total_spend", 0) or 0)
            waiver_spend = float(calc_quick.get("fee_waiver_spend", 0) or 0)
            fee_waived = bool(calc_quick.get("fee_waived", False))
            if waiver_spend > 0 and waiver_spend < 9e8:
                if fee_waived:
                    quick_items.append(
                        f"Fee waiver progress: <strong>achieved</strong> ({format_inr(annual_spend)} vs threshold {format_inr(waiver_spend)})."
                    )
                else:
                    waiver_pct = max(0.0, min(100.0, (annual_spend / waiver_spend) * 100))
                    quick_items.append(
                        f"Fee waiver progress: <strong>{waiver_pct:.0f}%</strong> ({format_inr(annual_spend)} of {format_inr(waiver_spend)})."
                    )

            cat_rewards = calc_quick.get("category_monthly_reward", {}) or {}
            if isinstance(cat_rewards, dict) and cat_rewards:
                top_cat, top_val = max(cat_rewards.items(), key=lambda kv: float(kv[1] or 0))
                top_annual = float(top_val or 0) * 12
                if top_annual > 0:
                    quick_items.append(
                        f"Top reward driver: <strong>{html.escape(str(top_cat).title())}</strong> contributes about {format_inr(top_annual)}/year."
                    )

            if quick_items:
                quick_win_html = f'<ul class="compare-facts">{"".join(f"<li>{x}</li>" for x in quick_items[:3])}</ul>'

            truth_score_html = ""
            if truth_score is not None:
                truth_score_html = (
                    f'<div class="truth-score-line">'
                    f'<span class="truth-score-label">Truth Score</span>'
                    f'<span class="truth-score-value">{int(truth_score)}/100</span>'
                    f'</div>'
                )

            comparison_html = f"""
<div class="compare-shell">
  <div class="compare-card">
    <span class="compare-badge">Popularity</span>
    <div class="compare-title">Internet Rating</div>
    <div class="compare-value">{market_rating_value:.1f}/5 ⭐</div>
    <div class="compare-note">How people rate this card in public listings.</div>
    <div class="compare-source">Average public rating from affiliate listings (not personalized).</div>
  </div>

  <div class="compare-card">
    <span class="compare-badge">Personal Value</span>
    <div class="compare-title">CredLens Verdict</div>
    <div class="verdict-box {v_class}">{html.escape(str(truth_label))}</div>
    {truth_score_html}
    <div class="truth-badges">{truth_badges_html}</div>
    {quick_win_html}
    <div class="compare-note">Based on your spending, realistic reward value, caps, and annual fee impact.</div>
    {truth_facts_html}
    <div class="compare-source">Personalized estimate from reward math, redemption friction, cap rules, and fee waiver checks.</div>
  </div>
</div>
"""
            st.markdown(comparison_html, unsafe_allow_html=True)

    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    

    with st.container(border=False):
        
        st.markdown(
        """
            <div class="section-header">
                Current Card Comparison
            </div>
            """,unsafe_allow_html=True
                )
        st.markdown("""<div class="section-subtitle">Compare your current card with the top recommendation for you.</div>""", unsafe_allow_html=True)
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

        with st.expander("Should you switch your current card?", expanded=True):
            # --- NEW: SMART CONTEXTUAL ALERTS ---
            if comparison_data:
            
                # 1. THE "NO CARD" NUDGE
                if comparison_data['type'] == 'no_card':
                    st.info(f"""Choose your current card above, or start with **{best_card['Card Name']}** based on your spending.""")
                    #st.markdown(f"### Start your credit card journey with ***{best_card['Card Name']}***! ")


                # 2. THE "SAME CARD" VALIDATION
                elif comparison_data['type'] == 'same_card' and comparison_data.get("current_card_name") == best_card['Card Name']:
                    st.success(f"You already use **{best_card['Card Name']}**. It still looks like a strong fit for your current spending.")
                
                elif comparison_data['type'] == 'same_card' and comparison_data.get("current_card_name") != best_card['Card Name']:
                    curr_name = comparison_data.get("current_card_name", "current card")
                    st.success(f"Your current **{curr_name}** card is performing similarly for your current spending.")

                # 3. THE "lounge access CARD" VALIDATION
                elif comparison_data['type'] == 'no_card_lounge':
                    st.info(f"**{comparison_data['current_card_name']}** does not offer lounge access with your selected filter. **{best_card['Card Name']}** is the closest match that does.")

                # 3. THE "SWITCH" WARNING (Existing Logic)
                elif comparison_data['type'] == 'switch':
                    curr_name = comparison_data['current_card_name']
                    diff = comparison_data['diff']

                    # Dynamic analogy
                    if diff < 2000:
                        analogy = "Roughly offsets one to two casual dining bills."
                    elif diff < 5000:
                        analogy = "Roughly offsets a year of streaming and Wi-Fi bills."
                    elif diff < 10000:
                        analogy = "Roughly offsets a low-cost domestic flight."
                    elif diff < 25000:
                        analogy = "Roughly offsets a mid-range phone purchase."
                    elif diff == 0:
                        analogy = "Results are effectively similar."
                    else:
                        analogy = "Could materially offset a larger annual expense."

                    if diff > 0:
                        curr_name_safe = html.escape(str(curr_name))
                        best_card_name_safe = html.escape(str(best_card["Card Name"]))
                        diff_label = format_inr(diff)
                        current_savings_label = format_inr(comparison_data.get("current_savings", 0))
                        best_savings_label = format_inr(best_card.get("Net Savings", 0))
                        analogy_line = html.escape(str(analogy)).rstrip(".")

                        st.markdown(f"""
                        <div class="money-alert">
                            <div class="money-alert-title">Switch Opportunity</div>
                            <div class="opportunity-amount">{diff_label}/year</div>
                            <div class="opportunity-summary">
                                Switching from <span class="highlight-card">{curr_name_safe}</span> to <span class="highlight-card">{best_card_name_safe}</span> may add this value annually.
                            </div>
                            <ul class="opportunity-facts">
                                <li><span class="opportunity-label">Current card estimate:</span> {current_savings_label}/year</li>
                                <li><span class="opportunity-label">Recommended estimate:</span> {best_savings_label}/year</li>
                                <li><span class="opportunity-label">Likely impact:</span> {analogy_line} per year.</li>
                            </ul>
                            <div class="money-alert-muted">Based on current monthly inputs and reward-rate math.</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("""<div class="content-heading">Top 3 recommended cards for you</div>""", unsafe_allow_html=True)
                        render_top3_recommendation_cards(valid_cards_df)
                    else:
                        # Negative Diff = The Current Card is ACTUALLY BETTER than our algorithm's pick?
                        # (Rare, but happens if the user selected a Super Premium card we filtered out by salary, or logic quirks)
                        curr_name_safe = html.escape(str(curr_name))
                        best_name_safe = html.escape(str(best_card["Card Name"]))
                        current_savings = format_inr(comparison_data["current_savings"])
                        best_savings = format_inr(best_card["Net Savings"])
                        st.markdown(
                            f"""✅ <b>Current card remains competitive.</b> Your current card (<b>{curr_name_safe}</b>) is estimated at {current_savings} vs <b>{best_name_safe}</b> at {best_savings}.""",
                            unsafe_allow_html=True
                        )



    # 5. RESTORED: The Math Expander 
    # This now uses the 'spends' argument we added
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

    # End-of-flow CTA to keep users focused on the primary action.
    with st.container(border=False):
        link = best_card.get("Apply_Link")
        if pd.notna(link):
            color = get_brand_color(best_card["Card Name"])
            st.markdown(
                f"""
                <div class="final-cta-card">
                    <div class="final-cta-title">Ready to apply?</div>
                    <div class="final-cta-note"><strong>{html.escape(str(best_card['Card Name']))}</strong> is your best match based on your current inputs.</div>
                    <div class="apply-cta-wrap" style="--apply-btn-color: {color}; margin-top: 0;">
                        <a href="{link}" target="_blank" class="apply-cta-link">
                            <button class="apply-btn">Apply for {html.escape(str(best_card['Card Name']))}</button>
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("""<div class="assumption-note">Want to see how this was calculated? Open optional details below.</div>""", unsafe_allow_html=True)

    with st.expander("Optional: see full calculation details"):
        st.markdown(
            """<div class="assumption-note">These estimates use your monthly spending, published reward rates, annual fees, and simple cap assumptions.</div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            """<div class="muted-text">We calculate rewards category by category and then subtract the annual fee.</div>""",
            unsafe_allow_html=True
        )
        calc_details = logic.calculate_card_yield_details(best_card, spends)

        breakdown_rows = []

        def add_breakdown_row(label: str, monthly_spend: float, reward_rate: float):
            if monthly_spend <= 0:
                return
            annual_spend = monthly_spend * 12
            estimated_reward = annual_spend * reward_rate / 100
            breakdown_rows.append(
                {
                    "Category": label,
                    "Annual Spend": annual_spend,
                    "Reward Rate": reward_rate,
                    "Estimated Reward": estimated_reward,
                }
            )

        add_breakdown_row("Online", float(spends.get("online", 0)), float(best_card.get("Online Rate", 0)))
        add_breakdown_row(
            "Utilities",
            float(spends.get("utilities", 0)),
            float(best_card.get("Utility Rate", best_card.get("Base Rate", 0))),
        )
        add_breakdown_row("UPI", float(spends.get("upi", 0)), float(best_card.get("UPI Rate", 0)))
        add_breakdown_row("Travel", float(spends.get("travel", 0)), float(best_card.get("Travel Rate", 0)))
        add_breakdown_row("Offline", float(spends.get("offline", 0)), float(best_card.get("Base Rate", 0)))

        if breakdown_rows:
            breakdown_df = pd.DataFrame(breakdown_rows)
            # Use exact engine outputs (includes reward value, caps, exclusions, milestones, fee waiver).
            total_estimated_rewards = float(calc_details.get("annual_reward_before_fee", 0))
            annual_fee = float(calc_details.get("effective_fee", best_card.get("Fee", 0)))
            net_estimate = float(calc_details.get("net_savings", 0))

            m1, m2, m3 = st.columns(3)
            m1.metric("Estimated Rewards / Year", format_inr(total_estimated_rewards))
            m2.metric("Annual Fee", format_inr(annual_fee))
            m3.metric("Estimated Net Value", format_inr(net_estimate))

            # Audit strip: quick visibility into core cap/milestone/fee-waiver assumptions.
            monthly_realized = format_inr(calc_details.get("monthly_realized_reward", 0))
            monthly_cap_val = calc_details.get("monthly_cap", 0)
            cap_type_raw = str(calc_details.get("cap_type", "none") or "none")
            cap_type_label = cap_type_raw.replace("_", " ").title()
            cap_note = "No cap applied"
            try:
                monthly_cap_num = float(monthly_cap_val)
                if monthly_cap_num > 0 and monthly_cap_num < 900000:
                    cap_note = f"Cap: {format_inr(monthly_cap_num)}/month ({cap_type_label})"
                else:
                    cap_note = f"Cap: {cap_type_label}"
            except (TypeError, ValueError):
                cap_note = f"Cap: {cap_type_label}"

            milestone_bonus = float(calc_details.get("milestone_bonus_annual", 0))
            milestone_note = f"Milestone bonus: {format_inr(milestone_bonus)}/year"
            fee_waived = bool(calc_details.get("fee_waived", False))
            fee_note = "Fee waiver: Applied" if fee_waived else "Fee waiver: Not applied"

            st.markdown(
                f"""
                <div class="assumption-note">
                    <strong>Calculation audit:</strong> Realized reward {monthly_realized}/month • {html.escape(cap_note)} • {milestone_note} • {fee_note}
                </div>
                """,
                unsafe_allow_html=True
            )

            display_breakdown = breakdown_df.copy()
            display_breakdown["Annual Spend"] = display_breakdown["Annual Spend"].apply(format_inr)
            display_breakdown["Reward Rate"] = display_breakdown["Reward Rate"].apply(lambda x: f"{x:.2f}%")
            display_breakdown["Estimated Reward"] = display_breakdown["Estimated Reward"].apply(format_inr)

            st.dataframe(display_breakdown, use_container_width=True, hide_index=True)
        else:
            st.info("Add monthly spend inputs to see the calculation breakdown.")
