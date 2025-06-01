import streamlit as st

class UIComponents:
    """Class to handle UI styling and components with theme support"""
    
    @staticmethod
    def initialize_theme():
        """Initialize theme state if not already set"""
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
    
    @staticmethod
    def render_theme_toggle():
        """Render the theme toggle button in the sidebar"""
        with st.sidebar:
            st.markdown("### Settings")
            current_theme = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
            if st.button(current_theme, use_container_width=True):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
    
    @staticmethod
    def get_theme_colors():
        """Get color scheme based on current theme"""
        if st.session_state.dark_mode:
            return {
                'bg_primary': '#1a1a1a',
                'bg_secondary': '#2d2d2d',
                'bg_tertiary': '#3a3a3a',
                'text_primary': '#ffffff',
                'text_secondary': '#e0e0e0',
                'text_muted': '#a0a0a0',
                'border': '#4a4a4a',
                'accent': '#3b82f6',
                'accent_hover': '#2563eb',
                'accent_light': '#1e3a8a',
                'card_bg': '#2d2d2d',
                'form_bg': '#333333',
                'recommendation_bg': '#2a2a2a',
                'ai_section_bg': '#1f2937',
                'ai_response_bg': '#374151'
            }
        else:
            return {
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8f9fa',
                'bg_tertiary': '#ffffff',
                'text_primary': '#2c3e50',
                'text_secondary': '#374151',
                'text_muted': '#6b7280',
                'border': '#e8eaed',
                'accent': '#3b82f6',
                'accent_hover': '#2563eb',
                'accent_light': '#1e40af',
                'card_bg': '#ffffff',
                'form_bg': '#ffffff',
                'recommendation_bg': '#f8fafc',
                'ai_section_bg': '#f0f9ff',
                'ai_response_bg': '#ffffff'
            }
    
    @staticmethod
    def load_custom_css():
        """Load theme-aware CSS styling"""
        UIComponents.initialize_theme()
        colors = UIComponents.get_theme_colors()
        
        st.markdown(f"""
        <style>
            /* Remove default Streamlit styling */
            .stApp {{
                background-color: {colors['bg_primary']};
                color: {colors['text_primary']};
            }}
            
            /* Sidebar styling */
            .css-1d391kg {{
                background-color: {colors['bg_secondary']};
            }}
            
            /* Header styling */
            .main-header {{
                font-size: 2.5rem;
                font-weight: 600;
                color: {colors['text_primary']};
                text-align: center;
                margin-bottom: 2rem;
                padding: 1rem 0;
                border-bottom: 2px solid {colors['border']};
            }}
            
            /* Form container */
            .form-container {{
                background: {colors['form_bg']};
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                border: 1px solid {colors['border']};
                margin-bottom: 2rem;
            }}
            
            /* Input field styling */
            .stSelectbox > div > div {{
                border-radius: 8px;
                border: 1px solid {colors['border']};
                background-color: {colors['card_bg']};
                color: {colors['text_primary']};
            }}
            
            .stSelectbox label {{
                color: {colors['text_secondary']} !important;
            }}
            
            .stSlider > div > div {{
                background-color: {colors['bg_secondary']};
            }}
            
            .stSlider label {{
                color: {colors['text_secondary']} !important;
            }}
            
            .stNumberInput > div > div {{
                border-radius: 8px;
                border: 1px solid {colors['border']};
                background-color: {colors['card_bg']};
                color: {colors['text_primary']};
            }}
            
            .stNumberInput label {{
                color: {colors['text_secondary']} !important;
            }}
            
            .stTextInput > div > div {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                color: {colors['text_primary']};
            }}
            
            .stTextInput label {{
                color: {colors['text_secondary']} !important;
            }}
            
            /* Button styling */
            .predict-button {{
                background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_light']} 100%);
                color: white;
                padding: 0.75rem 2rem;
                border: none;
                border-radius: 8px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                margin-top: 1rem;
                transition: all 0.3s ease;
            }}
            
            .predict-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
                background: linear-gradient(135deg, {colors['accent_hover']} 0%, {colors['accent_light']} 100%);
            }}
            
            /* Results container */
            .results-container {{
                background: {colors['card_bg']};
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                border: 1px solid {colors['border']};
                margin: 2rem 0;
            }}
            
            /* Score display */
            .score-display {{
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_light']} 100%);
                border-radius: 12px;
                color: white;
                margin-bottom: 2rem;
            }}
            
            .score-number {{
                font-size: 3rem;
                font-weight: bold;
                margin: 1rem 0;
            }}
            
            .score-level {{
                font-size: 1.5rem;
                font-weight: 600;
            }}
            
            /* Clean metric cards */
            .metric-card {{
                background: {colors['card_bg']};
                padding: 1.5rem;
                border-radius: 8px;
                border: 1px solid {colors['border']};
                margin-bottom: 1rem;
                text-align: center;
            }}
            
            .metric-title {{
                font-size: 0.9rem;
                color: {colors['text_muted']};
                font-weight: 500;
                margin-bottom: 0.5rem;
            }}
            
            .metric-value {{
                font-size: 1.5rem;
                font-weight: 600;
                color: {colors['text_secondary']};
            }}
            
            /* Recommendations */
            .recommendation-card {{
                background: {colors['recommendation_bg']};
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 4px solid {colors['accent']};
                margin-bottom: 1rem;
            }}
            
            .recommendation-title {{
                font-weight: 600;
                color: {colors['text_primary']};
                margin-bottom: 0.5rem;
            }}
            
            .recommendation-text {{
                color: {colors['text_secondary']};
                line-height: 1.6;
            }}
            
            /* AI Analysis section */
            .ai-section {{
                background: {colors['ai_section_bg']};
                padding: 2rem;
                border-radius: 12px;
                border: 1px solid {colors['border']};
                margin: 2rem 0;
            }}
            
            .ai-header {{
                color: {colors['accent']};
                font-weight: 600;
                font-size: 1.2rem;
                margin-bottom: 1rem;
            }}
            
            .ai-response {{
                background: {colors['ai_response_bg']};
                padding: 1.5rem;
                border-radius: 8px;
                border: 1px solid {colors['border']};
                color: {colors['text_secondary']};
                line-height: 1.6;
            }}
            
            /* Hide Streamlit branding */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
            
            /* Clean spacing */
            .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
            }}
            
            /* Section headers */
            .section-header {{
                font-size: 1.3rem;
                font-weight: 600;
                color: {colors['text_primary']};
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid {colors['border']};
            }}

            /* Streamlit component styling */
            .stButton > button {{
                background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_light']} 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                background: linear-gradient(135deg, {colors['accent_hover']} 0%, {colors['accent_light']} 100%);
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
            }}
            
            .stButton > button:focus {{
                background: linear-gradient(135deg, {colors['accent_hover']} 0%, {colors['accent_light']} 100%);
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
            }}
            
            /* Number Input Styling */
            .stNumberInput button {{
                background-color: transparent !important;
                color: {colors['text_muted']} !important;
                border: 1px solid {colors['border']} !important;
                border-radius: 6px !important;
                transition: all 0.2s ease !important;
            }}
            
            .stNumberInput button:hover {{
                background-color: {colors['accent']} !important;
                color: white !important;
                border-color: {colors['accent']} !important;
            }}
            
            .stNumberInput button:focus {{
                background-color: {colors['accent_hover']} !important;
                color: white !important;
                border-color: {colors['accent_hover']} !important;
                outline: none !important;
            }}
            
            /* Alternative selectors for number inputs */
            div[data-testid="stNumberInput"] button {{
                background-color: transparent !important;
                color: {colors['text_muted']} !important;
                border: 1px solid {colors['border']} !important;
                transition: all 0.2s ease !important;
            }}
            
            div[data-testid="stNumberInput"] button:hover {{
                background-color: {colors['accent']} !important;
                color: white !important;
                border-color: {colors['accent']} !important;
            }}
            
            /* Spinner styling */
            .stSpinner > div {{
                border-top-color: {colors['accent']} !important;
            }}
            
            /* Download button styling */
            .stDownloadButton > button {{
                background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_light']} 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            
            .stDownloadButton > button:hover {{
                background: linear-gradient(135deg, {colors['accent_hover']} 0%, {colors['accent_light']} 100%);
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
            }}
            
            /* Sidebar button styling */
            .css-1d391kg .stButton > button {{
                background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_light']} 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
                width: 100%;
            }}
            
            .css-1d391kg .stButton > button:hover {{
                background: linear-gradient(135deg, {colors['accent_hover']} 0%, {colors['accent_light']} 100%);
                transform: translateY(-2px);
            }}
            
            /* Sidebar text styling */
            .css-1d391kg h3 {{
                color: {colors['text_primary']} !important;
            }}
            
            /* Error and success message styling */
            .stError {{
                background-color: #fee2e2 !important;
                color: #dc2626 !important;
                border: 1px solid #fecaca !important;
            }}
            
            .stSuccess {{
                background-color: #dcfce7 !important;
                color: #16a34a !important;
                border: 1px solid #bbf7d0 !important;
            }}
            
            /* Dark mode adjustments for error/success */
            {f'''
            .stError {{
                background-color: #7f1d1d !important;
                color: #fca5a5 !important;
                border: 1px solid #991b1b !important;
            }}
            
            .stSuccess {{
                background-color: #14532d !important;
                color: #86efac !important;
                border: 1px solid #166534 !important;
            }}
            ''' if st.session_state.dark_mode else ''}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render clean main header with theme toggle"""
        UIComponents.render_theme_toggle()
        st.markdown('<h1 class="main-header">Social Media Addiction Prediction</h1>', unsafe_allow_html=True)
    
    @staticmethod
    def create_form_container():
        """Create a form container"""
        return st.container()
    
    @staticmethod
    def create_results_container():
        """Create a results container"""
        return st.container()
    
    @staticmethod
    def display_score(score, level, emoji):
        """Display prediction score in a clean format"""
        st.markdown(f"""
        <div class="score-display">
            <div class="score-level">{emoji} {level}</div>
            <div class="score-number">{score:.1f}/10</div>
            <div style="font-size: 1rem; opacity: 0.9;">Addiction Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_metric_card(title, value):
        """Display a clean metric card"""
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_recommendation(title, text):
        """Display a recommendation card"""
        st.markdown(f"""
        <div class="recommendation-card">
            <div class="recommendation-title">{title}</div>
            <div class="recommendation-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_section_header(title):
        """Display a section header"""
        st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)