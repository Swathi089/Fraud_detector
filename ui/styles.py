"""
ui/styles.py
============
Centralized design system and CSS styling for the Fraud Detection Portal.
Contains reusable CSS classes and design tokens for consistent theming.
"""

# Complete Design System CSS
DESIGN_SYSTEM_CSS = """
<style>
/* ========================================
   DESIGN SYSTEM - CSS VARIABLES
   ======================================== */
:root {
    /* Colors */
    --bg-primary: #0a0f1a;
    --bg-secondary: #151f2e;
    --bg-tertiary: #1b263b;
    --bg-card: rgba(21, 31, 46, 0.95);
    
    --accent-primary: #00d4ff;
    --accent-secondary: #6366f1;
    --accent-gradient: linear-gradient(135deg, #00d4ff 0%, #6366f1 100%);
    
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #3b82f6;
    
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    --border-color: rgba(0, 212, 255, 0.15);
    --border-hover: rgba(0, 212, 255, 0.3);
    
    /* Spacing */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    --spacing-2xl: 48px;
    
    /* Border Radius */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    
    /* Shadows */
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 30px rgba(0, 212, 255, 0.15);
    
    /* Transitions */
    --transition-fast: 0.2s ease;
    --transition-normal: 0.3s ease;
    --transition-slow: 0.5s ease;
}

/* ========================================
   GLOBAL STYLES
   ======================================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
.stDeployButton {display: none !important;}
header {visibility: hidden !important;}

/* Background */
.stApp {
    background: linear-gradient(135deg, var(--bg-primary) 0%, #162032 50%, var(--bg-primary) 100%) !important;
    min-height: 100vh;
}

/* Animated background pattern */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 15% 85%, rgba(0, 212, 255, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(99, 102, 241, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(0, 212, 255, 0.03) 0%, transparent 60%);
    pointer-events: none;
    z-index: -1;
}

/* Page fade-in animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.stApp > div {
    animation: fadeIn 0.5s ease forwards;
}

/* ========================================
   TYPOGRAPHY
   ======================================== */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2 { font-size: 1.5rem !important; }
h3 { font-size: 1.25rem !important; }

p, span, div {
    color: var(--text-secondary) !important;
}

/* ========================================
   CARDS - Glassmorphism
   ======================================== */
.glass-card {
    background: var(--bg-card) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: var(--radius-lg) !important;
    padding: var(--spacing-lg) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: var(--shadow-lg), var(--shadow-glow) !important;
    transition: all var(--transition-normal) !important;
}

.glass-card:hover {
    transform: translateY(-4px) !important;
    border-color: var(--border-hover) !important;
    box-shadow: var(--shadow-lg), 0 0 40px rgba(0, 212, 255, 0.2) !important;
}

/* Simple card without hover */
.simple-card {
    background: var(--bg-card) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--spacing-md) !important;
    border: 1px solid var(--border-color) !important;
}

/* ========================================
   METRIC CARDS
   ======================================== */
.metric-card {
    background: var(--bg-card) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--spacing-lg) !important;
    border: 1px solid var(--border-color) !important;
    position: relative;
    overflow: hidden;
    transition: all var(--transition-normal) !important;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--accent-gradient);
}

.metric-card:hover {
    transform: translateY(-2px) !important;
    border-color: var(--border-hover) !important;
}

.metric-icon {
    font-size: 24px;
    margin-bottom: var(--spacing-sm);
}

.metric-label {
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--spacing-xs);
}

.metric-value {
    color: var(--text-primary) !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    line-height: 1.2;
}

.metric-delta {
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    margin-top: var(--spacing-xs);
}

.metric-delta.positive { color: var(--success) !important; }
.metric-delta.negative { color: var(--danger) !important; }
.metric-delta.warning { color: var(--warning) !important; }

/* ========================================
   BUTTONS
   ======================================== */
/* Primary button */
.stButton > button[kind="primary"],
div.stButton > button {
    background: var(--accent-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    transition: all var(--transition-fast) !important;
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

.stButton > button:hover,
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
}

.stButton > button:active,
div.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"],
button.stSecondary {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 24px !important;
    font-weight: 500 !important;
    transition: all var(--transition-fast) !important;
}

.stButton > button[kind="secondary"]:hover,
button.stSecondary:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: var(--accent-primary) !important;
}

/* Danger button */
.stButton > button.danger-btn,
button.danger-btn {
    background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%) !important;
    color: white !important;
    border: none !important;
}

.stButton > button.danger-btn:hover {
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
}

/* Full width button */
.stButton > button.use-container-width {
    width: 100% !important;
}

/* ========================================
   FORM INPUTS
   ======================================== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 16px !important;
    font-size: 0.875rem !important;
    transition: all var(--transition-fast) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.15) !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-muted) !important;
}

.stTextInput > label,
.stTextArea > label,
.stNumberInput > label,
.stSelectbox > label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    margin-bottom: 6px !important;
}

/* Password input with icon */
.stTextInput > div > div:has(input[type="password"])::before {
    content: '🔒';
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 14px;
    opacity: 0.5;
    z-index: 10;
    pointer-events: none;
}

.stTextInput > div > div:has(input[type="password"]) input {
    padding-left: 38px !important;
}

/* ========================================
   SELECT / DROPDOWN
   ======================================== */
.stSelectbox > div > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
}

.stSelectbox > div > div > div:hover {
    border-color: var(--border-hover) !important;
}

/* ========================================
   CHECKBOX & RADIO
   ======================================== */
.stCheckbox > label,
.stRadio > label {
    color: var(--text-secondary) !important;
    font-size: 0.875rem !important;
}

/* ========================================
   ALERTS & MESSAGES
   ======================================== */
.stAlert {
    background: rgba(21, 31, 46, 0.9) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid !important;
    padding: 12px 16px !important;
}

.stSuccess {
    background: rgba(16, 185, 129, 0.15) !important;
    border-color: rgba(16, 185, 129, 0.3) !important;
    color: var(--success) !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.15) !important;
    border-color: rgba(245, 158, 11, 0.3) !important;
    color: var(--warning) !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    border-color: rgba(239, 68, 68, 0.3) !important;
    color: var(--danger) !important;
}

.stInfo {
    background: rgba(59, 130, 246, 0.15) !important;
    border-color: rgba(59, 130, 246, 0.3) !important;
    color: var(--info) !important;
}

/* ========================================
   SIDEBAR
   ======================================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%) !important;
    border-right: 1px solid var(--border-color) !important;
}

[data-testid="stSidebar"] .css-17lntkn {
    background: transparent !important;
}

/* Sidebar user profile */
.sidebar-profile {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    border: 1px solid var(--border-color);
    text-align: center;
}

.sidebar-avatar {
    font-size: 48px;
    margin-bottom: var(--spacing-sm);
}

.sidebar-name {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 1rem;
}

.sidebar-email {
    color: var(--text-secondary);
    font-size: 0.75rem;
    margin-top: 4px;
}

/* Sidebar navigation */
.sidebar-nav-item {
    padding: 12px 16px;
    border-radius: var(--radius-md);
    margin: 4px 0;
    transition: all var(--transition-fast);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
}

.sidebar-nav-item:hover {
    background: rgba(0, 212, 255, 0.1);
}

.sidebar-nav-item.active {
    background: rgba(0, 212, 255, 0.15);
    border-left: 3px solid var(--accent-primary);
}

/* ========================================
   TABLES & DATAFRAMES
   ======================================== */
.stDataFrame {
    background: var(--bg-card) !important;
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--border-color) !important;
    overflow: hidden;
}

/* DataFrame styling */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
}

/* ========================================
   TABS
   ======================================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    padding: 10px 20px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    transition: all var(--transition-fast);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--accent-gradient) !important;
    color: white !important;
    border-color: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: var(--border-hover) !important;
}

/* ========================================
   PROGRESS & SPINNER
   ======================================== */
.stProgress > div > div > div {
    background: var(--accent-gradient) !important;
}

.stSpinner > div {
    border-color: var(--accent-primary) transparent transparent !important;
}

/* ========================================
   EXPANDERS
   ======================================== */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(255, 255, 255, 0.08) !important;
}

/* ========================================
   FILE UPLOADER
   ======================================== */
.stFileUploader {
    background: var(--bg-card) !important;
    border-radius: var(--radius-lg) !important;
    border: 2px dashed var(--border-color) !important;
    padding: var(--spacing-xl) !important;
    transition: all var(--transition-normal);
}

.stFileUploader:hover {
    border-color: var(--accent-primary) !important;
    background: rgba(0, 212, 255, 0.05) !important;
}

.stFileUploader > div:first-child {
    color: var(--text-secondary) !important;
}

/* ========================================
   DIVIDERS
   ======================================== */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: var(--spacing-lg) 0;
}

/* ========================================
   CUSTOM SCROLLBAR
   ======================================== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--border-hover);
}

/* ========================================
   UTILITY CLASSES
   ======================================== */
.text-primary { color: var(--text-primary) !important; }
.text-secondary { color: var(--text-secondary) !important; }
.text-accent { color: var(--accent-primary) !important; }
.text-success { color: var(--success) !important; }
.text-warning { color: var(--warning) !important; }
.text-danger { color: var(--danger) !important; }

.bg-card { background: var(--bg-card) !important; }
.bg-secondary { background: var(--bg-secondary) !important; }

.border-accent { border-color: var(--border-color) !important; }

.rounded-md { border-radius: var(--radius-md) !important; }
.rounded-lg { border-radius: var(--radius-lg) !important; }

.p-sm { padding: var(--spacing-sm) !important; }
.p-md { padding: var(--spacing-md) !important; }
.p-lg { padding: var(--spacing-lg) !important; }

.m-sm { margin: var(--spacing-sm) !important; }
.m-md { margin: var(--spacing-md) !important; }
.m-lg { margin: var(--spacing-lg) !important; }

.flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
}

.flex-between {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.gap-sm { gap: var(--spacing-sm) !important; }
.gap-md { gap: var(--spacing-md) !important; }
.gap-lg { gap: var(--spacing-lg) !important; }

/* ========================================
   RESPONSIVE DESIGN
   ======================================== */
@media (max-width: 768px) {
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.25rem !important; }
    
    .glass-card {
        padding: var(--spacing-md) !important;
    }
    
    .metric-card {
        padding: var(--spacing-md) !important;
    }
    
    .metric-value {
        font-size: 1.25rem !important;
    }
}

/* ========================================
   ANIMATIONS
   ======================================== */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); }
    50% { box-shadow: 0 0 40px rgba(0, 212, 255, 0.4); }
}

.animate-slide-up {
    animation: slideUp 0.5s ease forwards;
}

.animate-pulse {
    animation: pulse 2s infinite;
}

.animate-glow {
    animation: glow 2s infinite;
}

/* Staggered animations for lists */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
.stagger-4 { animation-delay: 0.4s; }
.stagger-5 { animation-delay: 0.5s; }
</style>
"""


def inject_design_system():
    """
    Inject the design system CSS into the Streamlit app.
    Call this function at the beginning of each page.
    """
    import streamlit as st
    st.markdown(DESIGN_SYSTEM_CSS, unsafe_allow_html=True)


def card(html_content, hover=True):
    """
    Create a glassmorphism card with optional hover effect.

    Args:
        html_content: HTML content to display inside the card
        hover: Whether to add hover effect

    Returns:
        HTML string for the card
    """
    card_class = "glass-card" if hover else "simple-card"
    return f'<div class="{card_class}">{html_content}</div>'


def metric_card(icon, label, value, delta=None, delta_type="neutral"):
    """
    Create a styled metric card.

    Args:
        icon: Emoji or icon for the metric
        label: Label text
        value: Value to display
        delta: Optional delta value
        delta_type: "positive", "negative", "warning", or "neutral"

    Returns:
        HTML string for the metric card
    """
    delta_html = ""
    if delta:
        delta_class = f"metric-delta {delta_type}"
        delta_html = f'<div class="{delta_class}">{delta}</div>'

    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def section_header(title, icon=None, subtitle=None):
    """
    Create a styled section header.

    Args:
        title: Title text
        icon: Optional emoji icon
        subtitle: Optional subtitle text

    Returns:
        HTML string for the section header
    """
    icon_html = f"{icon} " if icon else ""
    subtitle_html = f'<p style="color: var(--text-secondary); font-size: 0.875rem; margin-top: 4px;">{subtitle}</p>' if subtitle else ""

    return f"""
    <div style="margin-bottom: var(--spacing-lg);">
        <h2 style="margin-bottom: 0;">{icon_html}{title}</h2>
        {subtitle_html}
    </div>
    """
