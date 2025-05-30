import plotly.graph_objects as go

class AddictionAnalyzer:
    """Class to handle addiction level analysis"""
    
    @staticmethod
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

class ChartGenerator:
    """Class to handle chart generation"""
    
    @staticmethod
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
    
    @staticmethod
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
