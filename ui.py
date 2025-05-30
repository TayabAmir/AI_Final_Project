import streamlit as st

class UIComponents:
    """Class to handle UI styling and components"""
    
    @staticmethod
    def load_custom_css():
        """Load custom CSS styling"""
        st.markdown("""
        <style>
            .main-header {
                font-size: 3rem;
                color: #1f77b4;
                text-align: center;
                margin-bottom: 2rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            .prediction-box {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                color: white;
                text-align: center;
                margin: 1rem 0;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }
            .prediction-score {
                font-size: 3rem;
                font-weight: bold;
                margin: 1rem 0;
            }
            .metric-card {
                background: white;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-left: 4px solid #1f77b4;
            }
            .warning-box {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            }
            .success-box {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            }
            .chatbot-container {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
            }
            .chatbot-header {
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: bold;
            }
            .gemini-response {
                background: white;
                border-left: 4px solid #4285f4;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .user-query {
                background: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render main header"""
        st.markdown('<h1 class="main-header">📱 Social Media Addiction Predictor</h1>', unsafe_allow_html=True)
