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
        font-size: var(--fs-xs);
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

    .section-divider {
        height: 1px;
        margin: var(--space-2) 0 var(--space-3) 0;
        background: linear-gradient(90deg, transparent, rgba(156, 163, 175, 0.35), transparent);
    }

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
        margin: 0 0 var(--space-2) 14px;
        max-width: 62ch;
    }

    .best-card-name {
        display: inline-block;
        max-width: 100%;
        word-break: break-word;
        font-size: var(--fs-xl);
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

    .best-card-confidence {
        color: rgba(156, 163, 175, 0.75);
        font-size: 0.68rem;
        line-height: 1.3;
        margin: 2px 0 var(--space-2) 0;
    }

    .best-card-fit {
        color: var(--text-primary);
        font-size: var(--fs-md);
        font-weight: var(--fw-medium);
        line-height: 1.5;
        margin: var(--space-3) 0 var(--space-2) 0;
    }

    .best-card-caution {
        color: #FDE68A;
        font-size: var(--fs-sm);
        line-height: 1.45;
        margin: 0 0 var(--space-2) 0;
    }

    .hero-context-line {
        color: var(--text-secondary);
        font-size: var(--fs-sm);
        line-height: 1.4;
        margin: 0 0 var(--space-3) 0;
    }

    .hero-story {
        display: grid;
        gap: 8px;
        margin: var(--space-2) 0 var(--space-2) 0;
    }

    .hero-story-card {
        border: 1px solid rgba(156, 163, 175, 0.2);
        background: rgba(17, 24, 39, 0.34);
        border-radius: 12px;
        padding: 8px 10px;
    }

    .hero-story-card--compact {
        padding: 6px 8px;
    }

    .hero-story-card--accent {
        border-color: rgba(59, 130, 246, 0.36);
        background: rgba(30, 58, 138, 0.18);
    }

    .hero-story-kicker {
        color: #BFDBFE;
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin: 0 0 6px 0;
    }

    .hero-story-copy {
        color: var(--text-primary);
        font-size: var(--fs-md);
        line-height: 1.5;
        margin: 0;
    }

    .hero-story-copy strong {
        color: #F9FAFB;
        font-weight: var(--fw-semibold);
    }

    .hero-story-context {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.35;
        margin-top: 4px;
        font-style: italic;
    }

    .hero-mini-table {
        width: 100%;
        table-layout: fixed;
        border-collapse: separate;
        border-spacing: 0;
        border: 1px solid rgba(156, 163, 175, 0.18);
        background: rgba(17, 24, 39, 0.2);
        margin-top: 0;
        overflow: hidden;
        border-radius: 10px;
    }

    .hero-mini-table th,
    .hero-mini-table td {
        border-bottom: 1px solid rgba(156, 163, 175, 0.12);
        padding: 6px 9px;
        vertical-align: middle;
        text-align: left;
    }

    .hero-mini-table tr:last-child th,
    .hero-mini-table tr:last-child td {
        border-bottom: none;
        padding-bottom: 0;
    }

    .hero-mini-table th {
        width: 18%;
        color: var(--text-secondary);
        font-size: 0.68rem;
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        white-space: nowrap;
        border-right: 1px solid rgba(156, 163, 175, 0.1);
    }

    .hero-mini-table td {
        color: var(--text-primary);
        font-size: 0.85rem;
        font-weight: var(--fw-medium);
        line-height: 1.3;
    }

    .hero-mini-value {
        color: #F9FAFB;
        font-weight: var(--fw-semibold);
    }

    .hero-mini-sub {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.3;
        margin-top: 2px;
    }

    .hero-mini-sub--muted {
        color: rgba(229, 231, 235, 0.7);
        font-style: italic;
    }

    .hero-inline-badge {
        display: inline-block;
        border-radius: 999px;
        padding: 3px 8px;
        border: 1px solid rgba(59, 130, 246, 0.35);
        background: rgba(30, 58, 138, 0.22);
        color: #DBEAFE;
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        line-height: 1.2;
        white-space: nowrap;
    }

    @media (max-width: 900px) {
        .hero-mini-table th {
            width: 24%;
        }
        div[class*="st-key-styled_container_"] {
            padding: 20px 16px;
        }
        div[class*="st-key-styled_container_feature_"] {
            padding: 18px 14px;
        }
        .hero-story-card {
            padding: 7px 8px;
        }
        .hero-story-card--compact {
            padding: 5px 7px;
        }
        .apply-cta-wrap {
            padding: var(--space-2) var(--space-3);
        }
        .apply-btn {
            width: 100%;
            padding: 11px 16px;
        }
        .final-cta-card {
            padding: 12px;
        }
        .final-cta-note {
            font-size: var(--fs-sm);
        }
    }

    .hero-secondary-link {
        display: inline-block;
        color: #BFDBFE;
        font-size: var(--fs-sm);
        font-weight: var(--fw-medium);
        line-height: 1.35;
        text-decoration: none;
        margin-top: var(--space-2);
    }

    .hero-secondary-link:hover {
        color: #DBEAFE;
        text-decoration: underline;
    }

    .hero-note-chip {
        display: inline-block;
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #BBF7D0;
        background: rgba(20, 83, 45, 0.35);
        border-radius: 999px;
        font-size: var(--fs-xs);
        font-weight: var(--fw-medium);
        line-height: 1.25;
        padding: 4px 9px;
        margin: 0 0 var(--space-2) 0;
    }

    .method-note {
        color: var(--text-tertiary);
        font-size: var(--fs-xs);
        font-style: italic;
        line-height: 1.4;
        margin: var(--space-2) 2px 0 2px;
    }

    .secondary-note {
        color: var(--text-tertiary);
        font-size: var(--fs-xs);
        line-height: 1.4;
        margin: var(--space-3) 2px 0 2px;
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

    .hero-snapshot-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: var(--space-2);
        margin: 0 0 var(--space-2) 0;
    }

    .hero-snapshot-card {
        border: 1px solid rgba(156, 163, 175, 0.2);
        background: rgba(31, 41, 55, 0.42);
        border-radius: 10px;
        padding: 8px 10px;
    }

    .hero-snapshot-title {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin: 0 0 6px 0;
    }

    .hero-snapshot-line {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.35;
        margin: 0 0 4px 0;
    }

    .hero-snapshot-line strong {
        color: var(--text-primary);
        font-weight: var(--fw-semibold);
    }

    .hero-snapshot-metrics {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 8px;
        margin: 0 0 8px 0;
    }

    .hero-snapshot-metric {
        border: 1px solid rgba(156, 163, 175, 0.18);
        background: rgba(17, 24, 39, 0.46);
        border-radius: 8px;
        padding: 7px 8px;
    }

    .hero-snapshot-metric-label {
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        line-height: 1.2;
        margin: 0 0 2px 0;
    }

    .hero-snapshot-metric-value {
        color: var(--text-primary);
        font-size: var(--fs-sm);
        font-weight: var(--fw-semibold);
        line-height: 1.3;
        margin: 0;
    }

    .hero-pref-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 0;
    }

    .hero-pref-chip {
        display: inline-block;
        border-radius: 999px;
        padding: 3px 8px;
        font-size: var(--fs-xs);
        line-height: 1.25;
        border: 1px solid rgba(156, 163, 175, 0.2);
        color: var(--text-secondary);
        background: rgba(17, 24, 39, 0.45);
    }

    .hero-pref-chip--active {
        color: #BFDBFE;
        border-color: rgba(59, 130, 246, 0.45);
        background: rgba(30, 58, 138, 0.25);
    }

    .card-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 8px 0 10px 0;
        justify-content: center;
    }

    .card-meta-chip {
        display: inline-block;
        border: 1px solid rgba(156, 163, 175, 0.24);
        background: rgba(31, 41, 55, 0.45);
        color: var(--text-secondary);
        font-size: var(--fs-xs);
        font-weight: var(--fw-medium);
        border-radius: 999px;
        padding: 3px 9px;
        line-height: 1.25;
        white-space: nowrap;
    }

    @media (max-width: 900px) {
        .hero-snapshot-grid {
            grid-template-columns: 1fr;
        }
        .hero-snapshot-metrics {
            grid-template-columns: 1fr;
        }
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
        padding: 10px 12px;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.18);
        background: linear-gradient(180deg, rgba(31, 41, 55, 0.72), rgba(17, 24, 39, 0.52));
    }

    .total-spend-label {
        color: #BFDBFE;
        font-size: 0.72rem;
        font-weight: var(--fw-semibold);
        line-height: 1.3;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .total-spend-value {
        color: #F9FAFB;
        font-size: var(--fs-lg);
        font-weight: var(--fw-bold);
        line-height: 1.2;
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

    .money-alert-title--verdict {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 10px;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.18);
        border: 1px solid rgba(96, 165, 250, 0.35);
        color: #DBEAFE;
        font-size: var(--fs-xs);
        font-weight: var(--fw-semibold);
        letter-spacing: 0.02em;
        text-transform: uppercase;
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

    .compare-note--quiet {
        margin-top: 6px;
        font-size: 0.72rem;
        color: rgba(226, 232, 240, 0.6);
        font-style: italic;
        line-height: 1.35;
    }

    .compare-progress {
        margin-top: 6px;
        width: 50%;
        min-width: 180px;
    }

    .compare-progress-label {
        font-size: var(--fs-xs);
        color: var(--text-tertiary);
        line-height: 1.2;
        margin-bottom: 4px;
    }

    .compare-progress-track {
        height: 8px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        overflow: hidden;
    }

    .compare-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #60A5FA, #34D399);
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

    .truth-gauge-wrap {
        position: relative;
        margin: 6px 0 2px 0;
    }

    .truth-gauge {
        position: relative;
        width: 100%;
        height: 8px;
        border-radius: 999px;
        overflow: hidden;
        border: 1px solid rgba(156, 163, 175, 0.22);
        background: rgba(17, 24, 39, 0.55);
    }

    .truth-gauge-fill {
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            rgba(239, 68, 68, 0.9) 0%,
            rgba(239, 68, 68, 0.9) 49%,
            rgba(245, 158, 11, 0.9) 50%,
            rgba(245, 158, 11, 0.9) 69%,
            rgba(34, 197, 94, 0.9) 70%,
            rgba(34, 197, 94, 0.9) 100%
        );
    }

    .truth-gauge-marker {
        position: absolute;
        top: -12px;
        width: 0;
        height: 0;
        border-left: 7px solid transparent;
        border-right: 7px solid transparent;
        border-top: 10px solid #F9FAFB;
        filter: drop-shadow(0 0 2px rgba(17, 24, 39, 0.9));
        transform: translateX(-7px);
        z-index: 2;
    }

    .truth-gauge-marker::after {
        content: "";
        position: absolute;
        left: 50%;
        top: 12px;
        width: 10px;
        height: 10px;
        border-radius: 999px;
        background: #F9FAFB;
        border: 1px solid rgba(17, 24, 39, 0.75);
        transform: translateX(-50%);
    }

    .truth-gauge-scale {
        display: flex;
        justify-content: space-between;
        color: var(--text-tertiary);
        font-size: 0.7rem;
        line-height: 1.2;
        margin: 0 0 4px 0;
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
        """<div class="muted-text">Estimates are perfectly fine — no need to be exact.</div>""",
        unsafe_allow_html=True
        )
        #st.caption("Rough estimates are perfectly fine. We optimise for patterns, not precision.")
        with st.container(border=False):
            salary = st.number_input("💰 Monthly income ₹", min_value=0, step=5000, key = "salary",format="%d", help="Your take-home pay after taxes and deductions.")
            
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
                """<div class="muted-text">Not sure? Just give a rough idea. You can fine-tune later.</div>""",
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
            with st.expander("More spends"):
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
                    <div class="total-spend-label">Total monthly spend</div>
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
                "Compare against current card", 
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
    
    # Top recommendation card code starts here
    with st.container(key="styled_container_feature_1" , border=False):
        st.markdown(
        """
            <div class="title-card">
                Your Top Recommendation
            </div>
            """,unsafe_allow_html=True
                )
    
        hero_content = logic.build_hero_content(
            best_card,
            spends,
            max_spend_dict=max_spend_dict,
            wants_lounge=wants_lounge,
            truth_insight=truth_insight,
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
                f"""<div><span class="best-card-value {value_class}">{html.escape(hero_content["headline_value"])}</span></div>""",
                unsafe_allow_html=True
            )
            st.markdown(
                f"""<div class="best-card-support">{html.escape(hero_content["value_subline"])}</div>""",
                unsafe_allow_html=True
            )
            realization_label = html.escape(str(hero_content.get("hero_realization_label", "") or "Not set"))
            fee_display = html.escape(str(hero_content.get("fee_display", "") or ""))
            fee_detail = hero_content.get("fee_detail")
            fee_hook = hero_content.get("fee_hook")
            fee_detail_html = (
                f'<div class="hero-mini-sub">{html.escape(str(fee_detail))}</div>' if fee_detail else ""
            )
            fee_hook_html = (
                f'<div class="hero-mini-sub hero-mini-sub--muted">{html.escape(str(fee_hook))}</div>' if fee_hook else ""
            )
            st.markdown(
                f"""
                <div class="hero-story">
                    <div class="hero-story-card hero-story-card--accent">
                        <div class="hero-story-kicker">1. Why this card</div>
                        <div class="hero-story-copy"><strong>{html.escape(hero_content["why_this_card"])}</strong></div>
                    </div>
                    <div class="hero-story-card">
                        <div class="hero-story-kicker">2. Why it fits you</div>
                        <div class="hero-story-copy">{html.escape(hero_content["fit_reason"])}</div>
                        <div class="hero-story-context"><em>{html.escape(hero_content["context_line"])}</em></div>
                    </div>
                    <div class="hero-story-card hero-story-card--compact">
                        <div class="hero-story-kicker">3. Card snapshot</div>
                        <table class="hero-mini-table">
                            <tr>
                                <th>Payout</th>
                                <td><span class="hero-inline-badge">{realization_label}</span></td>
                            </tr>
                            <tr>
                                <th>Fee</th>
                                <td>
                                    <span class="hero-mini-value">{fee_display}</span>
                                    {fee_detail_html}
                                    {fee_hook_html}
                                </td>
                            </tr>
                        </table>
                    </div>
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
                    """<div class="best-card-confidence" style = "text-align:center;"><b>Affiliate link, no extra cost to you.</b></div>""",
                    unsafe_allow_html=True
                    )
                st.markdown(
                    """<div style="text-align:center;"><a href="#why-this-card-fits" class="hero-secondary-link">See why this fits</a></div>""",
                    unsafe_allow_html=True
                )
                st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

            # 4. CARD: Link 
            #st.markdown(f"For detailed reviews, [click here](https://www.google.com/search?q={best_card['Card Name'].replace(' ', '+')}+reviews).")
            
    
    #st.divider()
    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

    # Section 2 (restored): Why This Card Fits
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    with st.container(border=False):
        st.markdown('<div id="why-this-card-fits"></div>', unsafe_allow_html=True)
        explanation = logic.build_recommendation_explanation(
            best_card,
            spends,
            max_spend_dict=max_spend_dict,
            truth_insight=truth_insight,
        )
        st.markdown(
        """
            <div class="section-header">
            Why this card fits you
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            """<div class="section-subtitle">Why it fits and what to watch.</div>""",
            unsafe_allow_html=True
        )
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

        with st.container(border=False):
            st.markdown("""<div class="content-heading">Rewards</div>""", unsafe_allow_html=True)
            st.markdown(
                f"""<div class="money-alert--box money-alert-success"><div><strong>{html.escape(explanation["primary_reason"])}</strong></div><div class="money-alert-muted">{html.escape(explanation["supporting_reason"])}</div></div>""",
                unsafe_allow_html=True
            )
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            st.markdown("""<div class="content-heading">Things to consider</div>""", unsafe_allow_html=True)
            caution_body = f"<b>Watch out:</b> {html.escape(explanation['primary_caution'])}"
            if explanation.get("secondary_caution"):
                caution_body += f"<br><span class=\"money-alert-muted\">{html.escape(explanation['secondary_caution'])}</span>"
            st.markdown(
                f"""<div class="money-alert--box money-alert-warning">{caution_body}</div>""",
                unsafe_allow_html=True
            )
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            st.markdown("""<div class="content-heading">Is the fee worth it?</div>""", unsafe_allow_html=True)
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
                    <div class="fee-outlook-title">{html.escape(explanation["fee_verdict"])}</div>
                        <div class="{status_class}">{status_label}</div>
                    </div>
                    <div class="fee-outlook-percent">Estimated value recovered this year: <strong>{recovered_value}</strong> of <strong>{fee_label}</strong></div>
                    <!-- <div class="fee-outlook-bar">
                        <div class="fee-outlook-fill" style="width: {recovered_pct}%;"></div>
                    </div> -->
                    <div class="fee-outlook-timebox">
                        <div class="fee-outlook-timebox-value">{month_estimate_line}</div>
                    </div>
                    <div class="method-note">{html.escape(explanation["methodology_line"])}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

    #st.divider()
    with st.container( border=False):
        value_reality = logic.build_value_reality_insight(
            best_card,
            spends,
            truth_insight=truth_insight,
        )
        st.markdown(
        """
            <div class="section-header">
                Real-world checks
            </div>
            """,unsafe_allow_html=True
                )
        st.markdown(
            f"""<div class="section-subtitle">{html.escape(value_reality["lead_line"])}</div>""",
            unsafe_allow_html=True
        )
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
        with st.container(border=False):
            market_rating_raw = best_card.get("Market_Rating", 4.5)
            try:
                market_rating_value = float(market_rating_raw)
                if pd.isna(market_rating_value):
                    market_rating_value = 4.5
            except (TypeError, ValueError):
                market_rating_value = 4.5
            card_html = []
            for item in value_reality["cards"]:
                progress_html = ""
                progress_pct = item.get("progress_pct")
                if progress_pct is not None:
                    progress_int = max(0, min(100, int(round(progress_pct))))
                    progress_label = html.escape(str(item.get("progress_label") or f"{progress_int}% reached"))
                    progress_html = f"""
<div class="compare-progress">
  <div class="compare-progress-label">{progress_label}</div>
  <div class="compare-progress-track">
    <div class="compare-progress-fill" style="width: {progress_int}%"></div>
  </div>
</div>
"""
                note_html = ""
                if item.get("note"):
                    note_html = f'<div class="compare-note compare-note--quiet">{html.escape(item["note"])}</div>'
                card_html.append(
                    f"""<div class="compare-card">
<div class="compare-title">{html.escape(item["title"])}</div>
<div class="compare-note">{html.escape(item["body"])}</div>
{progress_html}
{note_html}
</div>"""
                )

            comparison_html = f"""
<div class="compare-shell">
  {''.join(card_html)}
</div>
<div class="secondary-note">Public rating: {market_rating_value:.1f}/5 from general listings</div>
"""
            st.markdown(comparison_html, unsafe_allow_html=True)

    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    

    with st.container(border=False):
        
        st.markdown(
        """
            <div class="section-header">
                Switch or stay?
            </div>
            """,unsafe_allow_html=True
                )
        st.markdown(
            """<div class="section-subtitle">A plain yes/no on switching.</div>""",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

        if comparison_data:

            if comparison_data['type'] == 'no_card':
                st.info(
                    f"You can start with **{best_card['Card Name']}**. It is a strong fit for your current spending."
                )

            elif comparison_data['type'] == 'same_card' and comparison_data.get("current_card_name") == best_card['Card Name']:
                st.success(
                    f"Stay with **{best_card['Card Name']}**. It still looks like the best fit for your current spending."
                )

            elif comparison_data['type'] == 'same_card' and comparison_data.get("current_card_name") != best_card['Card Name']:
                curr_name = comparison_data.get("current_card_name", "current card")
                st.success(
                    f"Stay with **{curr_name}** for now. The top card is not clearly better yet."
                )

            elif comparison_data['type'] == 'no_card_lounge':
                st.info(
                    f"Your selected **{comparison_data['current_card_name']}** does not match the lounge filter. **{best_card['Card Name']}** is the closest fit."
                )

            elif comparison_data['type'] == 'switch':
                curr_name = comparison_data['current_card_name']
                diff = comparison_data['diff']

                if diff < 2000:
                    verdict_title = "Close call"
                elif diff < 5000:
                    verdict_title = "Worth considering"
                elif diff < 25000:
                    verdict_title = "Strong case to switch"
                else:
                    verdict_title = "Worth switching?"

                if diff > 0:
                    curr_name_safe = html.escape(str(curr_name))
                    best_card_name_safe = html.escape(str(best_card["Card Name"]))
                    diff_label = format_inr(diff)
                    current_savings_label = format_inr(comparison_data.get("current_savings", 0))
                    best_savings_label = format_inr(best_card.get("Net Savings", 0))

                    st.markdown(f"""
                    <div class="money-alert">
                        <div class="money-alert-title money-alert-title--verdict">{verdict_title}</div>
                        <div class="opportunity-summary">
                            You could gain <span class="highlight-card">{diff_label}/year</span> by moving from <span class="highlight-card">{curr_name_safe}</span> to <span class="highlight-card">{best_card_name_safe}</span>.
                        </div>
                        <ul class="opportunity-facts">
                            <li><span class="opportunity-label">Your card:</span> {current_savings_label}/year</li>
                            <li><span class="opportunity-label">Recommended card:</span> {best_savings_label}/year</li>
                        </ul>
                        <div class="money-alert-muted">Based on your current spending.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""<div class="content-heading">Also consider these alternatives</div>""", unsafe_allow_html=True)
                    render_top3_recommendation_cards(valid_cards_df)
                else:
                    curr_name_safe = html.escape(str(curr_name))
                    best_name_safe = html.escape(str(best_card["Card Name"]))
                    current_savings = format_inr(comparison_data["current_savings"])
                    best_savings = format_inr(best_card["Net Savings"])
                    st.success(
                        f"Stay with **{curr_name_safe}** for now. It is estimated at {current_savings}/year versus {best_name_safe} at {best_savings}/year."
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
                    <div class="final-cta-note"><strong>{html.escape(str(best_card['Card Name']))}</strong> fits your current spending best.</div>
                    <div class="apply-cta-wrap" style="--apply-btn-color: {color}; margin-top: 0;">
                        <a href="{link}" target="_blank" class="apply-cta-link">
                            <button class="apply-btn">Apply for {html.escape(str(best_card['Card Name']))}</button>
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("""<div class="assumption-note">The full calculation is below.</div>""", unsafe_allow_html=True)

    with st.expander("Optional: see how this was calculated"):
        st.markdown(
            """<div class="assumption-note">Here is how we estimated this.</div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            """<div class="muted-text">We estimate rewards by category, then subtract the fee.</div>""",
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
            top_row = max(breakdown_rows, key=lambda row: row["Estimated Reward"])
            top_category = str(top_row["Category"])
            top_reward = format_inr(top_row["Estimated Reward"])
            top_spend = format_inr(top_row["Annual Spend"])

            m1, m2, m3 = st.columns(3)
            m1.metric("Estimated rewards", format_inr(total_estimated_rewards))
            m2.metric("Fee", format_inr(annual_fee))
            m3.metric("After fee", format_inr(net_estimate))

            st.markdown(
                f"""
                <div class="assumption-note">
                    <strong>Quick summary:</strong> Your strongest category is <strong>{html.escape(top_category)}</strong> at {top_reward} a year on {top_spend} of spend.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("""<div class="content-heading">Detailed breakdown</div>""", unsafe_allow_html=True)
            display_breakdown = breakdown_df.copy()
            display_breakdown["Annual Spend"] = display_breakdown["Annual Spend"].apply(format_inr)
            display_breakdown["Reward Rate"] = display_breakdown["Reward Rate"].apply(lambda x: f"{x:.2f}%")
            display_breakdown["Estimated Reward"] = display_breakdown["Estimated Reward"].apply(format_inr)

            st.dataframe(display_breakdown, use_container_width=True, hide_index=True)

            # Audit strip: quick visibility into core cap/milestone/fee-waiver assumptions.
            monthly_realized = format_inr(calc_details.get("monthly_realized_reward", 0))
            monthly_cap_val = calc_details.get("monthly_cap", 0)
            cap_type_raw = str(calc_details.get("cap_type", "none") or "none")
            cap_type_label = cap_type_raw.replace("_", " ").title()
            cap_note = "Reward limit: none"
            try:
                monthly_cap_num = float(monthly_cap_val)
                if monthly_cap_num > 0 and monthly_cap_num < 900000:
                    cap_note = f"Reward limit: {format_inr(monthly_cap_num)}/month ({cap_type_label})"
                else:
                    cap_note = f"Reward limit: {cap_type_label}"
            except (TypeError, ValueError):
                cap_note = f"Reward limit: {cap_type_label}"

            milestone_bonus = float(calc_details.get("milestone_bonus_annual", 0))
            milestone_note = f"Milestone bonus: {format_inr(milestone_bonus)}/year"
            fee_waived = bool(calc_details.get("fee_waived", False))
            fee_note = "Fee waiver: applied" if fee_waived else "Fee waiver: not applied"

            st.markdown(
                f"""
                <div class="assumption-note">
                    <strong>Quick audit:</strong> {monthly_realized}/month realized • {html.escape(cap_note)} • {milestone_note} • {fee_note}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Add monthly spend inputs to see the calculation breakdown.")
