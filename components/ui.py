#!/usr/bin/env python3
"""
UI components and styling for Airbnb Host Dashboard
"""

import streamlit as st

def get_custom_css():
    """Return custom CSS styling"""
    return """
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 0.8rem 0;
            border: 1px solid #e9ecef;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        .insight-box {
            background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #3498db;
            margin: 1.5rem 0;
            box-shadow: 0 4px 8px rgba(52, 152, 219, 0.1);
        }
        
        .success-message {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #c3e6cb;
            margin: 1rem 0;
        }
        
        .error-message {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            color: #721c24;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #f5c6cb;
            margin: 1rem 0;
        }
    </style>
    """

def render_metric_card(label, value, icon=""):
    """Render a metric card with consistent styling"""
    st.markdown(f"""
    <div class="metric-card">
        {icon} <strong>{label}:</strong> {value}
    </div>
    """, unsafe_allow_html=True)

def render_insight_box(title, content):
    """Render an insight box with consistent styling"""
    st.markdown(f"""
    <div class="insight-box">
        <h4>{title}</h4>
        {content}
    </div>
    """, unsafe_allow_html=True)

def render_success_message(message):
    """Render a success message"""
    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)

def render_error_message(message):
    """Render an error message"""
    st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)



def render_upload_instructions():
    """Render upload instructions"""
    st.markdown("### 📋 How to Get Your Airbnb Data")
    st.markdown("""
    <div class="insight-box">
        <h4>📥 Download Your Airbnb Data:</h4>
        <ol>
            <li>Log into your Airbnb account</li>
            <li>Go to your hosting dashboard</li>
            <li>Navigate to "Analytics" or "Reports"</li>
            <li>Export your booking data as CSV</li>
            <li>Upload one or more CSV files here</li>
        </ol>
        <p><strong>💡 Tip:</strong> You can upload multiple CSV files to combine data from different time periods or properties.</p>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard_features():
    """Render dashboard features overview"""
    st.markdown("### 🎯 What This Dashboard Shows")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Occupancy Analysis</h4>
            <ul>
                <li>Booking trends over time</li>
                <li>Peak and off-peak periods</li>
                <li>Day-of-week patterns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>💰 Revenue Insights</h4>
            <ul>
                <li>Total revenue tracking</li>
                <li>Revenue per booking</li>
                <li>Monthly revenue trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>💵 Pricing Analysis</h4>
            <ul>
                <li>Price distribution</li>
                <li>Pricing trends</li>
                <li>Revenue optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True) 