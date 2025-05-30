import streamlit as st

class UIComponents:
    """Class to handle UI styling and components"""
    
    @staticmethod
    def load_custom_css():
        
        """Load clean, modern CSS styling"""
        st.markdown("""
        <style>
    
            /* Remove default Streamlit styling */
            .stApp {
                background-color: #ffffff;
            }
            
            /* Header styling */
            .main-header {
                font-size: 2.5rem;
                font-weight: 600;
                color: #2c3e50;
                text-align: center;
                margin-bottom: 2rem;
                padding: 1rem 0;
                border-bottom: 2px solid #ecf0f1;
            }
            
            /* Form container */
            .form-container {
                background: #ffffff;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                border: 1px solid #e8eaed;
                margin-bottom: 2rem;
            }
            
            /* Input field styling */
            .stSelectbox > div > div {
                border-radius: 8px;
                border: 1px solid #d1d5db;
                background-color: #ffffff;
            }
            
            .stSlider > div > div {
                background-color: #f8f9fa;
            }
            
            .stNumberInput > div > div {
                border-radius: 8px;
                border: 1px solid #d1d5db;
            }
            
            /* Button styling - Changed to blue */
            .predict-button {
                background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
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
            }
            
            .predict-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            }
            
            /* Results container */
            .results-container {
                background: #ffffff;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                border: 1px solid #e8eaed;
                margin: 2rem 0;
            }
            
            /* Score display - Changed to blue gradient */
            .score-display {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
                border-radius: 12px;
                color: white;
                margin-bottom: 2rem;
            }
            
            .score-number {
                font-size: 3rem;
                font-weight: bold;
                margin: 1rem 0;
            }
            
            .score-level {
                font-size: 1.5rem;
                font-weight: 600;
            }
            
            /* Clean metric cards */
            .metric-card {
                background: #ffffff;
                padding: 1.5rem;
                border-radius: 8px;
                border: 1px solid #e8eaed;
                margin-bottom: 1rem;
                text-align: center;
            }
            
            .metric-title {
                font-size: 0.9rem;
                color: #6b7280;
                font-weight: 500;
                margin-bottom: 0.5rem;
            }
            
            .metric-value {
                font-size: 1.5rem;
                font-weight: 600;
                color: #374151;
            }
            
            /* Recommendations */
            .recommendation-card {
                background: #f8fafc;
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 4px solid #3b82f6;
                margin-bottom: 1rem;
            }
            
            .recommendation-title {
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 0.5rem;
            }
            
            .recommendation-text {
                color: #4b5563;
                line-height: 1.6;
            }
            
            /* AI Analysis section */
            .ai-section {
                background: #f0f9ff;
                padding: 2rem;
                border-radius: 12px;
                border: 1px solid #bfdbfe;
                margin: 2rem 0;
            }
            
            .ai-header {
                color: #1e40af;
                font-weight: 600;
                font-size: 1.2rem;
                margin-bottom: 1rem;
            }
            
            .ai-response {
                background: #ffffff;
                padding: 1.5rem;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                color: #374151;
                line-height: 1.6;
            }
            
            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Clean spacing */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            /* Input labels */
            .stSelectbox label, .stSlider label, .stNumberInput label {
                font-weight: 500;
                color: #374151;
                font-size: 0.95rem;
            }
            
            /* Section headers */
            .section-header {
                font-size: 1.3rem;
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #e5e7eb;
            }

            /* Additional Streamlit component styling for blue theme */
            .stButton > button {
                background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
            }
            
            .stButton > button:focus {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
            }
            
            /* Clean Number Input Styling */
            .stNumberInput button {
                background-color: transparent !important;
                color: #6b7280 !important;
                border: 1px solid #d1d5db !important;
                border-radius: 6px !important;
                transition: all 0.2s ease !important;
            }
            
            .stNumberInput button:hover {
                background-color: #3b82f6 !important;
                color: white !important;
                border-color: #3b82f6 !important;
            }
            
            .stNumberInput button:focus {
                background-color: #2563eb !important;
                color: white !important;
                border-color: #2563eb !important;
                outline: none !important;
            }
            
            /* Alternative selectors for number inputs */
            div[data-testid="stNumberInput"] button {
                background-color: transparent !important;
                color: #6b7280 !important;
                border: 1px solid #d1d5db !important;
                transition: all 0.2s ease !important;
            }
            
            div[data-testid="stNumberInput"] button:hover {
                background-color: #3b82f6 !important;
                color: white !important;
                border-color: #3b82f6 !important;
            }
            
            /* Keep sliders with default Streamlit styling */
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render clean main header"""
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