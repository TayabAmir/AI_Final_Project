import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Social Media Addiction Predictor",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        background: #d1e7dd;
        border: 1px solid #badbcc;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the trained model package"""
    try:
        model_package = joblib.load('best_addiction_model.pkl')
        return model_package
    except FileNotFoundError:
        st.error("❌ Model file 'best_addiction_model.pkl' not found. Please run the training script first.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

def get_addiction_level(score):
    """Categorize addiction level based on score"""
    if score <= 3:
        return "Low", "🟢", "#28a745"
    elif score <= 6:
        return "Moderate", "🟡", "#ffc107"
    elif score <= 8:
        return "High", "🟠", "#fd7e14"
    else:
        return "Very High", "🔴", "#dc3545"

def create_gauge_chart(score):
    """Create a gauge chart for addiction score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Addiction Score"},
        delta = {'reference': 5},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 3], 'color': "lightgreen"},
                {'range': [3, 6], 'color': "yellow"},
                {'range': [6, 8], 'color': "orange"},
                {'range': [8, 10], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 8
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_comparison_chart(user_data, avg_data):
    """Create comparison chart between user and average"""
    categories = ['Daily Usage', 'Sleep Hours', 'Mental Health', 'Conflicts']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=user_data,
        theta=categories,
        fill='toself',
        name='Your Profile',
        line_color='#1f77b4'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=avg_data,
        theta=categories,
        fill='toself',
        name='Average User',
        line_color='#ff7f0e'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        height=400
    )
    
    return fig

def make_prediction(model_package, user_input):
    """Make prediction using the loaded model"""
    try:
        input_df = pd.DataFrame([user_input])
        
        encoders = model_package['encoders']
        
        input_df['Gender'] = encoders['gender'].transform([user_input['Gender']])[0]
        input_df['Academic_Level'] = encoders['academic'].transform([user_input['Academic_Level']])[0]
        input_df['Country'] = encoders['country'].transform([user_input['Country']])[0]
        input_df['Most_Used_Platform'] = encoders['platform'].transform([user_input['Most_Used_Platform']])[0]
        input_df['Affects_Academic_Performance'] = encoders['affects'].transform([user_input['Affects_Academic_Performance']])[0]
        
        feature_order = model_package['feature_names']
        input_features = input_df[feature_order]
        
        if model_package['scaler'] is not None:
            input_features = model_package['scaler'].transform(input_features)
        
        prediction = model_package['model'].predict(input_features)[0]
        
        return max(0, min(10, prediction))  
        
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        return None

def main():
    st.markdown('<h1 class="main-header">📱 Social Media Addiction Predictor</h1>', unsafe_allow_html=True)
    
    model_package = load_model()
    if model_package is None:
        st.stop()
    
    st.success(f"✅ Loaded Model: **{model_package['model_name']}**")
    
    st.sidebar.header("📋 User Information")
    st.sidebar.markdown("Please fill in your details below:")
    
    with st.sidebar:
        age = st.slider("Age", min_value=15, max_value=30, value=20, help="Your current age")
        
        gender = st.selectbox("Gender", ["Male", "Female"], help="Select your gender")
        
        academic_level = st.selectbox(
            "Academic Level", 
            ["High School", "Undergraduate", "Graduate"],
            help="Your current academic level"
        )
        
        country = st.selectbox(
            "Country",
            ["USA", "UK", "Canada", "Australia", "Germany", "France", "India", "Japan", "Other"],
            help="Your country of residence"
        )
        
        daily_usage = st.slider(
            "Average Daily Usage (Hours)", 
            min_value=0.5, max_value=12.0, value=4.0, step=0.5,
            help="How many hours do you spend on social media daily?"
        )
        
        platform = st.selectbox(
            "Most Used Platform",
            ["Instagram", "TikTok", "Facebook", "YouTube", "Twitter", "Snapchat", "LinkedIn"],
            help="Which platform do you use most?"
        )
        
        affects_academic = st.selectbox(
            "Affects Academic Performance?",
            ["Yes", "No"],
            help="Do you feel social media affects your academic performance?"
        )
        
        sleep_hours = st.slider(
            "Sleep Hours Per Night",
            min_value=4.0, max_value=10.0, value=7.0, step=0.5,
            help="How many hours do you sleep per night?"
        )
        
        mental_health = st.slider(
            "Mental Health Score",
            min_value=1, max_value=10, value=6,
            help="Rate your mental health (1=Poor, 10=Excellent)"
        )
        
        conflicts = st.slider(
            "Conflicts Over Social Media",
            min_value=0, max_value=5, value=1,
            help="How often do you have conflicts due to social media use?"
        )
    
    predict_button = st.sidebar.button("🔮 Predict Addiction Score", type="primary")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if predict_button:
            user_input = {
                'Age': age,
                'Gender': gender,
                'Academic_Level': academic_level,
                'Country': country,
                'Avg_Daily_Usage_Hours': daily_usage,
                'Most_Used_Platform': platform,
                'Affects_Academic_Performance': affects_academic,
                'Sleep_Hours_Per_Night': sleep_hours,
                'Mental_Health_Score': mental_health,
                'Conflicts_Over_Social_Media': conflicts
            }
            
            with st.spinner("🔄 Analyzing your social media habits..."):
                prediction = make_prediction(model_package, user_input)
            
            if prediction is not None:
                st.session_state['prediction'] = prediction
                st.session_state['user_input'] = user_input
                
                level, emoji, color = get_addiction_level(prediction)
                
                st.markdown(f"""
                <div class="prediction-box">
                    <h2>🎯 Prediction Results</h2>
                    <div class="prediction-score">{emoji} {prediction:.1f}/10</div>
                    <h3>Addiction Level: {level}</h3>
                    <p>Based on your social media usage patterns and personal characteristics</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.plotly_chart(create_gauge_chart(prediction), use_container_width=True)
                
                if prediction <= 3:
                    st.markdown("""
                    <div class="success-box">
                        <h4>✅ Great News!</h4>
                        <p>Your social media usage appears to be well-controlled. You maintain a healthy balance between online and offline activities.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif prediction <= 6:
                    st.markdown("""
                    <div class="warning-box">
                        <h4>⚠️ Moderate Usage</h4>
                        <p>Your social media usage is moderate. Consider monitoring your habits to prevent them from becoming problematic.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                        <h4>🚨 High Usage Detected</h4>
                        <p>Your social media usage patterns suggest potential addiction. Consider seeking support or implementing digital wellness strategies.</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        if predict_button and 'prediction' in st.session_state:
            st.markdown("### 📊 Your Profile")
            
            profile_data = [
                ["Age", f"{age} years"],
                ["Daily Usage", f"{daily_usage} hours"],
                ["Sleep", f"{sleep_hours} hours"],
                ["Mental Health", f"{mental_health}/10"],
                ["Platform", platform],
                ["Academic Impact", affects_academic]
            ]
            
            for label, value in profile_data:
                st.markdown(f"**{label}:** {value}")
            
            st.markdown("### 📈 Profile Comparison")
            user_radar = [daily_usage, sleep_hours, mental_health, conflicts]
            avg_radar = [4.5, 6.5, 6.5, 2.0] 
            
            fig_radar = create_comparison_chart(user_radar, avg_radar)
            st.plotly_chart(fig_radar, use_container_width=True)
    
    if predict_button and 'prediction' in st.session_state:
        st.markdown("---")
        st.markdown("### 💡 Insights & Recommendations")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            if daily_usage > 6:
                st.warning("📱 **High Usage Alert**\nConsider setting daily time limits")
            else:
                st.success("📱 **Usage Normal**\nGood control over screen time")
        
        with col4:
            if sleep_hours < 6:
                st.warning("😴 **Sleep Concern**\nTry to get 7-8 hours of sleep")
            else:
                st.success("😴 **Sleep Healthy**\nGood sleep patterns maintained")
        
        with col5:
            if mental_health < 5:
                st.warning("🧠 **Mental Health**\nConsider professional support")
            else:
                st.success("🧠 **Mental Health**\nPositive mental wellbeing")
        
        st.markdown("### 🎯 Personalized Recommendations")
        if st.session_state['prediction'] > 7:
            st.markdown("""
            - 🕒 Set specific times for social media use
            - 📵 Use app timers and notifications
            - 🏃‍♂️ Engage in offline physical activities
            - 👥 Spend more time with friends and family in person
            - 📚 Focus on academic/professional goals
            """)
        elif st.session_state['prediction'] > 4:
            st.markdown("""
            - ⏰ Monitor your daily usage patterns
            - 🔕 Turn off non-essential notifications
            - 🌱 Develop new hobbies outside of social media
            - 💤 Avoid social media before bedtime
            """)
        else:
            st.markdown("""
            - ✅ Continue your healthy usage patterns
            - 🎯 Share your strategies with others
            - 📈 Consider helping friends with social media balance
            """)
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Model Used:** {model_package['model_name']} | **Prediction Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()