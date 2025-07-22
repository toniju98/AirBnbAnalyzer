#!/usr/bin/env python3
"""
Airbnb Host Advisor - Copenhagen Example
Provides insights for hosts on pricing, amenities, seasonal adjustments, and rating improvement.
Example application using Copenhagen Airbnb data.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Airbnb Host Advisor - Copenhagen Example",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.8rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        margin: 1rem 0 2rem 0;
    }
    
    /* Subheader styling */
    .subheader {
        font-size: 1.8rem;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding: 0.5rem 0;
        border-left: 4px solid #3498db;
        padding-left: 1rem;
        background: linear-gradient(90deg, #ecf0f1 0%, transparent 100%);
        border-radius: 0 5px 5px 0;
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    /* Insight box styling */
    .insight-box {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3498db;
        margin: 1.5rem 0;
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.1);
        border: 1px solid #bee5eb;
    }
    
    .insight-box h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .insight-box ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .insight-box li {
        margin: 0.5rem 0;
        color: #34495e;
        line-height: 1.6;
    }
    
    /* Data status styling */
    .data-status {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        border: 1px solid #dee2e6;
    }
    
    .data-available {
        color: #27ae60;
        font-weight: 600;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        border: 1px solid #c3e6cb;
    }
    
    .data-unavailable {
        color: #e74c3c;
        font-style: italic;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        border: 1px solid #f5c6cb;
    }
    
    /* Disabled option styling */
    .disabled-option {
        color: #95a5a6 !important;
        opacity: 0.7;
        font-style: italic;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px dashed #bdc3c7;
    }
    
    .disabled-option input {
        pointer-events: none;
    }
    
    /* Section styling */
    .section-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    
    /* Chart container styling */
    .chart-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    
    /* Metric grid styling */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    /* Success/Error message styling */
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
    
    .info-message {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    /* Warning message styling */
    .warning-message {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980b9 0%, #1f5f8b 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #3498db;
    }
    
    /* Overall page styling */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 0.8rem 0;
        }
        
        .subheader {
            font-size: 1.4rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .insight-box {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache Airbnb data"""
    try:
        # Load listings data
        if Path('listings.csv').exists():
            listings_df = pd.read_csv('listings.csv')
        elif Path('listings.csv.gz').exists():
            listings_df = pd.read_csv('listings.csv.gz', compression='gzip')
        else:
            st.error("No listings data found!")
            return None, None, None
        
        # Load reviews data
        if Path('reviews.csv').exists():
            reviews_df = pd.read_csv('reviews.csv')
        elif Path('reviews.csv.gz').exists():
            reviews_df = pd.read_csv('reviews.csv.gz', compression='gzip')
        else:
            reviews_df = None
        
        # Load calendar data
        if Path('calendar.csv.gz').exists():
            calendar_df = pd.read_csv('calendar.csv.gz', compression='gzip')
        else:
            calendar_df = None
        
        return listings_df, reviews_df, calendar_df
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

@st.cache_data
def clean_price_data(df, price_col):
    """Clean price data safely"""
    if price_col not in df.columns:
        return df
    
    def clean_price(price):
        try:
            if pd.isna(price):
                return np.nan
            elif isinstance(price, (int, float)):
                return float(price)
            elif isinstance(price, str):
                return float(price.replace('$', '').replace(',', ''))
            else:
                return np.nan
        except:
            return np.nan
    
    df[f'{price_col}_clean'] = df[price_col].apply(clean_price)
    return df

@st.cache_data
def extract_amenities(df):
    """Extract and analyze amenities"""
    amenities_cols = [col for col in df.columns if 'amenities' in col.lower()]
    if not amenities_cols:
        return pd.DataFrame()
    
    amenities_col = amenities_cols[0]
    
    # Extract individual amenities
    all_amenities = []
    for amenities_str in df[amenities_col].dropna():
        if isinstance(amenities_str, str):
            # Remove brackets and split by comma
            amenities = amenities_str.strip('[]').split(',')
            all_amenities.extend([amenity.strip().strip('"') for amenity in amenities])
    
    # Count amenities
    amenities_count = pd.Series(all_amenities).value_counts()
    return amenities_count

def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 Airbnb Host Advisor - MVP</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subheader">Your AI-powered guide to maximize your Airbnb success</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; font-style: italic; margin-bottom: 2rem;">📊 Copenhagen Airbnb Market Analysis • Focusing on occupancy, pricing, market comparison, and actionable recommendations</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading Airbnb data..."):
        listings_df, reviews_df, calendar_df = load_data()
    
    if listings_df is None:
        st.markdown('<div class="error-message">❌ Failed to load data. Please check your data files.</div>', unsafe_allow_html=True)
        return
    
    # Check data availability for MVP features
    has_calendar = calendar_df is not None
    has_price_data = any('price' in col.lower() for col in listings_df.columns)
    
    # MVP-focused options
    mvp_options = [
        "🏠 Main Dashboard",
        "📊 Occupancy Analysis", 
        "💰 Price Analysis", 
        "🏆 Market Comparison", 
        "🎯 Price Recommendations"
    ]
    
    # Sidebar for navigation
    st.sidebar.title("📊 MVP Analysis")
    
    # Create disabled options list for MVP
    disabled_options = []
    if not has_calendar:
        disabled_options.append("📊 Occupancy Analysis")
    if not has_price_data:
        disabled_options.append("💰 Price Analysis")
        disabled_options.append("🎯 Price Recommendations")
    
    # Create options list with disabled indicators
    selectbox_options = []
    for option in mvp_options:
        if option in disabled_options:
            selectbox_options.append(f"🔒 {option} (No data)")
        else:
            selectbox_options.append(option)
    
    # Sidebar selectbox
    st.sidebar.markdown("### Choose Analysis:")
    selected_option = st.sidebar.selectbox(
        "MVP Analysis Sections:",
        selectbox_options,
        index=0
    )
    
    # Extract the actual option name (remove the disabled indicator)
    if selected_option.startswith("🔒 "):
        # This is a disabled option, show warning and default to first available option
        st.sidebar.warning("⚠️ This option requires data that is not available")
        analysis_type = "📊 Occupancy Analysis"  # Default to first available option
    else:
        analysis_type = selected_option
    
    # Clean price data
    price_cols = [col for col in listings_df.columns if 'price' in col.lower()]
    if price_cols:
        listings_df = clean_price_data(listings_df, price_cols[0])
    
    # Main content based on MVP selection
    if analysis_type == "🏠 Main Dashboard":
        show_main_dashboard(listings_df, calendar_df)
    
    elif analysis_type == "📊 Occupancy Analysis":
        if has_calendar:
            show_occupancy_analysis(listings_df, calendar_df)
        else:
            st.markdown('<div class="error-message">❌ Occupancy Analysis requires calendar data that is not available.</div>', unsafe_allow_html=True)
            st.info("💡 To enable this feature, ensure you have a 'calendar.csv.gz' file in your data directory.")
    
    elif analysis_type == "💰 Price Analysis":
        if has_price_data:
            show_price_analysis(listings_df)
        else:
            st.markdown('<div class="error-message">❌ Price Analysis requires price data that is not available.</div>', unsafe_allow_html=True)
            st.info("💡 To enable this feature, ensure your listings data includes price columns.")
    
    elif analysis_type == "🏆 Market Comparison":
        show_market_comparison(listings_df)
    
    elif analysis_type == "🎯 Price Recommendations":
        if has_price_data:
            show_price_recommendations(listings_df)
        else:
            st.markdown('<div class="error-message">❌ Price Recommendations require price data that is not available.</div>', unsafe_allow_html=True)
            st.info("💡 To enable this feature, ensure your listings data includes price columns.")

def show_property_overview(listings_df, reviews_df, calendar_df):
    """Show property overview and market insights"""
    st.markdown('<h1 class="main-header">🏠 Property Overview & Market Insights</h1>', unsafe_allow_html=True)
    
    # Key metrics section
    st.markdown('<h2 class="subheader">📊 Key Market Metrics</h2>', unsafe_allow_html=True)
    
    # Calculate metrics first
    total_listings = len(listings_df)
    neighbourhood_count = listings_df['neighbourhood'].nunique() if 'neighbourhood' in listings_df.columns else 0
    room_type_count = listings_df['room_type'].nunique() if 'room_type' in listings_df.columns else 0
    
    price_cols = [col for col in listings_df.columns if 'price_clean' in col]
    avg_price = None
    if price_cols:
        price_data = listings_df[price_cols[0]].dropna()
        if len(price_data) > 0:
            avg_price = price_data.mean()
    
    # Only show metrics that have meaningful data
    metrics_to_show = []
    
    if total_listings > 0:
        metrics_to_show.append(("Total Listings", f"{total_listings:,}", True))
    
    if neighbourhood_count > 0:
        metrics_to_show.append(("Neighbourhoods", f"{neighbourhood_count}", True))
    
    if room_type_count > 0:
        metrics_to_show.append(("Room Types", f"{room_type_count}", True))
    
    if avg_price is not None:
        metrics_to_show.append(("Avg Price", f"${avg_price:.0f}", True))
    
    # Display metrics in columns
    if metrics_to_show:
        cols = st.columns(len(metrics_to_show))
        for i, (label, value, _) in enumerate(metrics_to_show):
            with cols[i]:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No meaningful metrics available for display.")

    # Market analysis section
    st.markdown('<h2 class="subheader">📈 Market Analysis</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Price distribution
        if price_cols and len(listings_df[price_cols[0]].dropna()) > 0:
            fig = px.histogram(listings_df, x=price_cols[0], nbins=30,
                              title="Price Distribution",
                              labels={price_cols[0]: "Price ($)"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No price data available for distribution chart.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Room type distribution
        if 'room_type' in listings_df.columns and listings_df['room_type'].nunique() > 0:
            room_counts = listings_df['room_type'].value_counts()
            fig = px.pie(values=room_counts.values, names=room_counts.index,
                        title="Room Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No room type data available for distribution chart.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Neighbourhood analysis section
    if 'neighbourhood' in listings_df.columns and listings_df['neighbourhood'].nunique() > 0:
        st.markdown('<h2 class="subheader">🏘️ Neighbourhood Analysis</h2>', unsafe_allow_html=True)
        
        neighbourhood_stats = listings_df.groupby('neighbourhood').agg({
            'id': 'count'
        }).rename(columns={'id': 'listing_count'})
        
        if price_cols and len(listings_df[price_cols[0]].dropna()) > 0:
            price_stats = listings_df.groupby('neighbourhood')[price_cols[0]].agg(['mean', 'median'])
            neighbourhood_stats = neighbourhood_stats.join(price_stats)
        
        fig = px.bar(neighbourhood_stats.reset_index(), x='neighbourhood', y='listing_count',
                     title="Listings by Neighbourhood")
        st.plotly_chart(fig, use_container_width=True)

def show_optimal_pricing(listings_df):
    """Show optimal pricing analysis"""
    st.markdown('<h1 class="main-header">💰 Optimal Pricing Analysis</h1>', unsafe_allow_html=True)
    
    # Filters section
    st.markdown('<h2 class="subheader">🔍 Filter Options</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Neighbourhood filter
        if 'neighbourhood' in listings_df.columns:
            neighbourhoods = ['All'] + sorted(listings_df['neighbourhood'].unique())
            selected_neighbourhood = st.selectbox("Select Neighbourhood:", neighbourhoods)
        else:
            selected_neighbourhood = "All"
    
    with col2:
        # Room type filter
        if 'room_type' in listings_df.columns:
            room_types = ['All'] + sorted(listings_df['room_type'].unique())
            selected_room_type = st.selectbox("Select Room Type:", room_types)
        else:
            selected_room_type = "All"
    
    # Filter data
    filtered_df = listings_df.copy()
    
    if selected_neighbourhood != "All":
        filtered_df = filtered_df[filtered_df['neighbourhood'] == selected_neighbourhood]
    
    if selected_room_type != "All":
        filtered_df = filtered_df[filtered_df['room_type'] == selected_room_type]
    
    # Price analysis
    price_cols = [col for col in filtered_df.columns if 'price_clean' in col]
    
    if price_cols and len(filtered_df) > 0:
        price_col = price_cols[0]
        price_data = filtered_df[price_col].dropna()
        
        if len(price_data) > 0:
            # Pricing insights section
            st.markdown('<h2 class="subheader">📊 Price Statistics</h2>', unsafe_allow_html=True)
            
            # Calculate meaningful metrics
            metrics_to_show = []
            
            avg_price = price_data.mean()
            median_price = price_data.median()
            min_price = price_data.min()
            max_price = price_data.max()
            
            if avg_price > 0:
                metrics_to_show.append(("Average Price", f"${avg_price:.0f}"))
            if median_price > 0:
                metrics_to_show.append(("Median Price", f"${median_price:.0f}"))
            if min_price > 0 and max_price > 0:
                metrics_to_show.append(("Price Range", f"${min_price:.0f} - ${max_price:.0f}"))
            
            # Display metrics in columns
            if metrics_to_show:
                cols = st.columns(len(metrics_to_show))
                for i, (label, value) in enumerate(metrics_to_show):
                    with cols[i]:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(label, value)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No meaningful price data available for statistics.")
            
            # Price distribution chart
            st.markdown('<h2 class="subheader">📈 Price Distribution</h2>', unsafe_allow_html=True)
            
            fig = px.histogram(filtered_df, x=price_col, nbins=20,
                              title=f"Price Distribution for {selected_room_type} in {selected_neighbourhood}",
                              labels={price_col: "Price ($)"})
            st.plotly_chart(fig, use_container_width=True)
            
            # Pricing recommendations section
            st.markdown('<h2 class="subheader">💡 Pricing Recommendations</h2>', unsafe_allow_html=True)
            
            # Calculate optimal price ranges
            q25, q50, q75 = price_data.quantile([0.25, 0.5, 0.75])
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>🎯 Optimal Price Ranges:</h4>
                <ul>
                    <li><strong>Budget Range:</strong> ${price_data.min():.0f} - ${q25:.0f}</li>
                    <li><strong>Competitive Range:</strong> ${q25:.0f} - ${q50:.0f}</li>
                    <li><strong>Premium Range:</strong> ${q50:.0f} - ${q75:.0f}</li>
                    <li><strong>Luxury Range:</strong> ${q75:.0f} - ${price_data.max():.0f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Market positioning
            st.markdown(f"""
            <div class="insight-box">
                <h4>📊 Market Positioning:</h4>
                <ul>
                    <li><strong>Market Average:</strong> ${price_data.mean():.0f}</li>
                    <li><strong>Median Price:</strong> ${price_data.median():.0f}</li>
                    <li><strong>Price Variance:</strong> ${price_data.std():.0f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="warning-message">⚠️ No price data available for the selected filters.</div>', unsafe_allow_html=True)

def show_amenity_analysis(listings_df):
    """Show amenity analysis and value impact"""
    st.header("🏆 Amenity Analysis & Value Impact")
    
    # Extract amenities
    amenities_count = extract_amenities(listings_df)
    
    if len(amenities_count) > 0:
        # Top amenities
        st.subheader("🏆 Most Popular Amenities")
        
        top_amenities = amenities_count.head(20)
        fig = px.bar(x=top_amenities.values, y=top_amenities.index, orientation='h',
                     title="Top 20 Amenities",
                     labels={'x': 'Number of Listings', 'y': 'Amenity'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Amenity value analysis
        st.subheader("💰 Amenity Value Analysis")
        
        # Analyze price impact of specific amenities
        price_cols = [col for col in listings_df.columns if 'price_clean' in col]
        amenities_cols = [col for col in listings_df.columns if 'amenities' in col.lower()]
        
        if price_cols and amenities_cols:
            price_col = price_cols[0]
            amenities_col = amenities_cols[0]
            
            # Analyze specific amenities
            key_amenities = ['WiFi', 'Kitchen', 'Air Conditioning', 'Pool', 'Gym', 'Parking', 'Balcony']
            
            amenity_analysis = []
            for amenity in key_amenities:
                # Check if amenity is present
                has_amenity = listings_df[amenities_col].str.contains(amenity, case=False, na=False)
                
                if has_amenity.sum() > 0:
                    with_amenity = listings_df[has_amenity][price_col].dropna()
                    without_amenity = listings_df[~has_amenity][price_col].dropna()
                    
                    if len(with_amenity) > 0 and len(without_amenity) > 0:
                        price_diff = with_amenity.mean() - without_amenity.mean()
                        price_diff_pct = (price_diff / without_amenity.mean()) * 100
                        
                        amenity_analysis.append({
                            'Amenity': amenity,
                            'With Amenity': with_amenity.mean(),
                            'Without Amenity': without_amenity.mean(),
                            'Price Difference': price_diff,
                            'Price Difference %': price_diff_pct,
                            'Listings with Amenity': len(with_amenity)
                        })
            
            if amenity_analysis:
                amenity_df = pd.DataFrame(amenity_analysis)
                
                # Sort by price impact
                amenity_df = amenity_df.sort_values('Price Difference %', ascending=False)
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(amenity_df, x='Amenity', y='Price Difference %',
                                 title="Price Impact of Amenities (%)",
                                 color='Price Difference %',
                                 color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### 💡 Amenity Insights")
                    for _, row in amenity_df.head(5).iterrows():
                        if row['Price Difference %'] > 0:
                            st.markdown(f"✅ **{row['Amenity']}**: +${row['Price Difference']:.0f} (+{row['Price Difference %']:.1f}%)")
                        else:
                            st.markdown(f"⚠️ **{row['Amenity']}**: ${row['Price Difference']:.0f} ({row['Price Difference %']:.1f}%)")
                
                # Detailed table
                st.subheader("📊 Detailed Amenity Analysis")
                st.dataframe(amenity_df.round(2))
    
    else:
        st.warning("No amenities data found in the dataset.")

def show_seasonal_pricing(listings_df, calendar_df):
    """Show seasonal pricing analysis"""
    st.header("📅 Seasonal Pricing Analysis")
    
    if calendar_df is not None:
        # Process calendar data
        if 'date' in calendar_df.columns:
            calendar_df['date'] = pd.to_datetime(calendar_df['date'])
            calendar_df['month'] = calendar_df['date'].dt.month
            calendar_df['season'] = calendar_df['date'].dt.month.map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            })
        
        # Price analysis by season
        price_cols = [col for col in calendar_df.columns if 'price' in col.lower()]
        
        if price_cols and 'season' in calendar_df.columns:
            price_col = price_cols[0]
            
            # Clean price data
            calendar_df[f'{price_col}_clean'] = pd.to_numeric(
                calendar_df[price_col].str.replace('$', '').str.replace(',', ''), 
                errors='coerce'
            )
            
            # Seasonal analysis
            seasonal_prices = calendar_df.groupby('season')[f'{price_col}_clean'].agg(['mean', 'median', 'std']).round(2)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(seasonal_prices, x=seasonal_prices.index, y='mean',
                             title="Average Price by Season",
                             labels={'mean': 'Average Price ($)', 'index': 'Season'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Monthly analysis
                monthly_prices = calendar_df.groupby('month')[f'{price_col}_clean'].mean()
                fig = px.line(x=monthly_prices.index, y=monthly_prices.values,
                             title="Price Trends by Month",
                             labels={'x': 'Month', 'y': 'Average Price ($)'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Seasonal recommendations
            st.subheader("💡 Seasonal Pricing Recommendations")
            
            best_season = seasonal_prices['mean'].idxmax()
            worst_season = seasonal_prices['mean'].idxmin()
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>📈 Seasonal Insights:</h4>
                <ul>
                    <li><strong>Highest Prices:</strong> {best_season} (${seasonal_prices.loc[best_season, 'mean']:.0f})</li>
                    <li><strong>Lowest Prices:</strong> {worst_season} (${seasonal_prices.loc[worst_season, 'mean']:.0f})</li>
                    <li><strong>Price Variation:</strong> ${seasonal_prices['mean'].max() - seasonal_prices['mean'].min():.0f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.warning("No calendar data available for seasonal analysis.")

def show_occupancy_analysis(listings_df, calendar_df):
    """Show occupancy analysis and recommendations"""
    st.markdown('<h1 class="main-header">📊 Occupancy Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; font-style: italic; margin-bottom: 2rem;">📊 Copenhagen Airbnb Occupancy Patterns • Booking trends and availability optimization</p>', unsafe_allow_html=True)
    
    if calendar_df is not None:
        # Process calendar data
        if 'date' in calendar_df.columns:
            calendar_df['date'] = pd.to_datetime(calendar_df['date'])
            calendar_df['month'] = calendar_df['date'].dt.month
            calendar_df['season'] = calendar_df['date'].dt.month.map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            })
        
        # Calculate occupancy metrics
        if 'available' in calendar_df.columns:
            # Overall occupancy statistics
            total_days = len(calendar_df)
            booked_days = (calendar_df['available'] == 'f').sum()
            available_days = (calendar_df['available'] == 't').sum()
            overall_occupancy_rate = (booked_days / total_days) * 100
            
            # Key metrics section
            st.markdown('<h2 class="subheader">📈 Overall Occupancy Statistics</h2>', unsafe_allow_html=True)
            
            # Calculate meaningful metrics
            metrics_to_show = []
            
            if total_days > 0:
                metrics_to_show.append(("Total Calendar Days", f"{total_days:,}"))
            if booked_days > 0:
                metrics_to_show.append(("Booked Days", f"{booked_days:,}"))
            if available_days > 0:
                metrics_to_show.append(("Available Days", f"{available_days:,}"))
            if overall_occupancy_rate > 0:
                metrics_to_show.append(("Overall Occupancy Rate", f"{overall_occupancy_rate:.1f}%"))
            
            # Display metrics in columns
            if metrics_to_show:
                cols = st.columns(len(metrics_to_show))
                for i, (label, value) in enumerate(metrics_to_show):
                    with cols[i]:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(label, value)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No meaningful occupancy data available for statistics.")
            
            # Occupancy by season section
            st.markdown('<h2 class="subheader">📅 Occupancy by Season</h2>', unsafe_allow_html=True)
            
            seasonal_occupancy = calendar_df.groupby('season')['available'].apply(
                lambda x: ((x == 'f').sum() / len(x)) * 100
            ).round(2)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = px.bar(x=seasonal_occupancy.index, y=seasonal_occupancy.values,
                             title="Occupancy Rate by Season",
                             labels={'x': 'Season', 'y': 'Occupancy Rate (%)'})
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                # Monthly occupancy trends
                monthly_occupancy = calendar_df.groupby('month')['available'].apply(
                    lambda x: ((x == 'f').sum() / len(x)) * 100
                ).round(2)
                
                fig = px.line(x=monthly_occupancy.index, y=monthly_occupancy.values,
                             title="Monthly Occupancy Trends",
                             labels={'x': 'Month', 'y': 'Occupancy Rate (%)'})
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Occupancy insights section
            st.markdown('<h2 class="subheader">💡 Occupancy Insights</h2>', unsafe_allow_html=True)
            
            best_season = seasonal_occupancy.idxmax()
            worst_season = seasonal_occupancy.idxmin()
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>📈 Occupancy Insights:</h4>
                <ul>
                    <li><strong>Highest Occupancy:</strong> {best_season} ({seasonal_occupancy[best_season]:.1f}%)</li>
                    <li><strong>Lowest Occupancy:</strong> {worst_season} ({seasonal_occupancy[worst_season]:.1f}%)</li>
                    <li><strong>Average Occupancy:</strong> {overall_occupancy_rate:.1f}%</li>
                    <li><strong>Peak Demand Period:</strong> {best_season} season</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Occupancy vs Price analysis section
            st.markdown('<h2 class="subheader">💰 Occupancy vs Price Analysis</h2>', unsafe_allow_html=True)
            
            price_cols = [col for col in calendar_df.columns if 'price' in col.lower()]
            if price_cols:
                price_col = price_cols[0]
                
                # Clean price data
                calendar_df[f'{price_col}_clean'] = pd.to_numeric(
                    calendar_df[price_col].str.replace('$', '').str.replace(',', ''), 
                    errors='coerce'
                )
                
                # Compare prices for booked vs available days
                booked_prices = calendar_df[calendar_df['available'] == 'f'][f'{price_col}_clean'].dropna()
                available_prices = calendar_df[calendar_df['available'] == 't'][f'{price_col}_clean'].dropna()
                
                if len(booked_prices) > 0 and len(available_prices) > 0:
                    # Calculate meaningful metrics
                    metrics_to_show = []
                    
                    booked_avg = booked_prices.mean()
                    available_avg = available_prices.mean()
                    
                    if booked_avg > 0:
                        metrics_to_show.append(("Average Price (Booked Days)", f"${booked_avg:.0f}"))
                    if available_avg > 0:
                        metrics_to_show.append(("Average Price (Available Days)", f"${available_avg:.0f}"))
                    
                    # Display metrics in columns
                    if metrics_to_show:
                        cols = st.columns(len(metrics_to_show))
                        for i, (label, value) in enumerate(metrics_to_show):
                            with cols[i]:
                                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                                st.metric(label, value)
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("No meaningful price data available for comparison.")
                    
                    # Price difference
                    price_diff = booked_prices.mean() - available_prices.mean()
                    price_diff_pct = (price_diff / available_prices.mean()) * 100
                    
                    st.markdown(f"""
                    <div class="insight-box">
                        <h4>💡 Price vs Occupancy Relationship:</h4>
                        <ul>
                            <li><strong>Price Difference:</strong> ${price_diff:.0f} ({price_diff_pct:+.1f}%)</li>
                            <li><strong>Booked days are ${abs(price_diff):.0f} {'higher' if price_diff > 0 else 'lower'} than available days</li>
                            <li><strong>This suggests:</strong> {'Higher prices may be reducing bookings' if price_diff > 0 else 'Lower prices may be driving more bookings'}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No meaningful price data available for occupancy vs price analysis.")
            
            # Recommendations section
            st.markdown('<h2 class="subheader">🚀 Strategic Recommendations</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="insight-box">
                    <h4>📈 For High Occupancy Periods:</h4>
                    <ul>
                        <li>Consider raising prices during peak seasons</li>
                        <li>Implement dynamic pricing strategies</li>
                        <li>Focus on premium guest experiences</li>
                        <li>Optimize for longer stays</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="insight-box">
                    <h4>📉 For Low Occupancy Periods:</h4>
                    <ul>
                        <li>Offer competitive pricing to attract guests</li>
                        <li>Consider special promotions and discounts</li>
                        <li>Target local or business travelers</li>
                        <li>Improve marketing during off-peak times</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="error-message">❌ No calendar data available for occupancy analysis.</div>', unsafe_allow_html=True)

def show_rating_improvement(listings_df, reviews_df):
    """Show rating improvement analysis"""
    st.markdown('<h1 class="main-header">⭐ Rating Improvement Analysis</h1>', unsafe_allow_html=True)
    
    # Rating analysis
    rating_cols = [col for col in listings_df.columns if 'rating' in col.lower() or 'score' in col.lower()]
    
    if rating_cols:
        rating_col = rating_cols[0]
        rating_data = listings_df[rating_col].dropna()
        
        if len(rating_data) > 0:
            # Calculate meaningful metrics
            metrics_to_show = []
            
            avg_rating = rating_data.mean()
            median_rating = rating_data.median()
            rating_count = len(rating_data)
            
            if avg_rating > 0:
                metrics_to_show.append(("Average Rating", f"{avg_rating:.1f}/5"))
            if median_rating > 0:
                metrics_to_show.append(("Median Rating", f"{median_rating:.1f}/5"))
            if rating_count > 0:
                metrics_to_show.append(("Rating Distribution", f"{rating_count} listings"))
            
            # Display metrics in columns
            if metrics_to_show:
                cols = st.columns(len(metrics_to_show))
                for i, (label, value) in enumerate(metrics_to_show):
                    with cols[i]:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(label, value)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No meaningful rating data available for statistics.")
            
            # Rating distribution
            st.markdown('<h2 class="subheader">📊 Rating Distribution</h2>', unsafe_allow_html=True)
            fig = px.histogram(listings_df, x=rating_col, nbins=20,
                              title="Rating Distribution",
                              labels={rating_col: "Rating"})
            st.plotly_chart(fig, use_container_width=True)
            
            # Rating vs Price analysis
            price_cols = [col for col in listings_df.columns if 'price_clean' in col]
            if price_cols:
                price_col = price_cols[0]
                
                # Filter data with both rating and price
                analysis_df = listings_df[[rating_col, price_col]].dropna()
                
                if len(analysis_df) > 0:
                    st.markdown('<h2 class="subheader">💰 Rating vs Price Analysis</h2>', unsafe_allow_html=True)
                    fig = px.scatter(analysis_df, x=price_col, y=rating_col,
                                    title="Rating vs Price",
                                    labels={price_col: "Price ($)", rating_col: "Rating"})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for rating vs price analysis.")
            
            # Rating improvement tips
            st.markdown('<h2 class="subheader">💡 Rating Improvement Tips</h2>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-box">
                <h4>🎯 Key Areas for Improvement:</h4>
                <ul>
                    <li><strong>Communication:</strong> Respond quickly to guest messages</li>
                    <li><strong>Cleanliness:</strong> Maintain high cleaning standards</li>
                    <li><strong>Accuracy:</strong> Ensure listing description matches reality</li>
                    <li><strong>Value:</strong> Provide amenities that exceed expectations</li>
                    <li><strong>Location:</strong> Highlight nearby attractions and convenience</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="warning-message">⚠️ No rating data available for analysis.</div>', unsafe_allow_html=True)

def show_host_insights(listings_df, reviews_df, calendar_df):
    """Show comprehensive host insights"""
    st.header("🎯 Comprehensive Host Insights")
    
    # Key insights dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Market Position")
        
        # Calculate market position metrics
        price_cols = [col for col in listings_df.columns if 'price_clean' in col]
        if price_cols:
            price_col = price_cols[0]
            avg_price = listings_df[price_col].mean()
            median_price = listings_df[price_col].median()
            
            st.metric("Market Average Price", f"${avg_price:.0f}")
            st.metric("Market Median Price", f"${median_price:.0f}")
            
            # Price positioning
            if avg_price > median_price:
                st.success("✅ Your market is premium-focused")
            else:
                st.info("ℹ️ Your market is value-focused")
    
    with col2:
        st.subheader("🏆 Competitive Advantages")
        
        # Analyze unique selling points
        amenities_cols = [col for col in listings_df.columns if 'amenities' in col.lower()]
        if amenities_cols:
            amenities_count = extract_amenities(listings_df)
            if len(amenities_count) > 0:
                top_amenities = amenities_count.head(5).index.tolist()
                st.write("**Most Valued Amenities:**")
                for amenity in top_amenities:
                    st.write(f"• {amenity}")
    
    # Strategic recommendations
    st.subheader("🚀 Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h4>💰 Pricing Strategy:</h4>
            <ul>
                <li>Start with competitive pricing</li>
                <li>Monitor competitor prices regularly</li>
                <li>Adjust based on demand and seasonality</li>
                <li>Consider dynamic pricing for peak periods</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h4>🏆 Guest Experience:</h4>
            <ul>
                <li>Provide exceptional communication</li>
                <li>Ensure spotless cleanliness</li>
                <li>Offer local recommendations</li>
                <li>Create memorable experiences</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance metrics
    st.subheader("📈 Performance Metrics")
    
    # Calculate key metrics
    metrics_data = []
    
    if 'neighbourhood' in listings_df.columns:
        neighbourhood_counts = listings_df['neighbourhood'].value_counts()
        metrics_data.append(("Most Popular Neighbourhood", neighbourhood_counts.index[0]))
    
    if 'room_type' in listings_df.columns:
        room_type_counts = listings_df['room_type'].value_counts()
        metrics_data.append(("Most Common Room Type", room_type_counts.index[0]))
    
    price_cols = [col for col in listings_df.columns if 'price_clean' in col]
    if price_cols:
        price_col = price_cols[0]
        price_data = listings_df[price_col].dropna()
        if len(price_data) > 0:
            metrics_data.append(("Price Range", f"${price_data.min():.0f} - ${price_data.max():.0f}"))
            metrics_data.append(("Average Price", f"${price_data.mean():.0f}"))
    
    # Display metrics
    for metric_name, metric_value in metrics_data:
        st.metric(metric_name, metric_value)

def show_geographic_analysis(listings_df):
    """Show comprehensive geographic analysis with interactive maps"""
    st.header("🗺️ Geographic Analysis")
    
    # Check if we have geographic data
    lat_cols = [col for col in listings_df.columns if 'lat' in col.lower()]
    lon_cols = [col for col in listings_df.columns if 'lon' in col.lower()]
    
    if not lat_cols or not lon_cols:
        st.warning("❌ No latitude/longitude data found for geographic analysis")
        return
    
    lat_col = lat_cols[0]
    lon_col = lon_cols[0]
    
    # Filter out listings without coordinates
    geo_df = listings_df.dropna(subset=[lat_col, lon_col]).copy()
    
    if len(geo_df) == 0:
        st.warning("❌ No valid geographic data available")
        return
    
    st.success(f"✅ Analyzing {len(geo_df)} properties with geographic data")
    
    # Create tabs for different map views
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Interactive Map", "💰 Price Heatmap", "⭐ Rating Map", "🏘️ Neighbourhood Analysis"])
    
    with tab1:
        st.subheader("Interactive Property Map")
        
        # Map controls
        col1, col2 = st.columns(2)
        with col1:
            map_type = st.selectbox("Map Style:", ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark_matter"])
        
        with col2:
            color_by = st.selectbox("Color by:", ["Price", "Rating", "Room Type", "Neighbourhood"])
        
        # Create interactive map
        map_obj = create_interactive_map(geo_df, lat_col, lon_col, color_by, map_type)
        
        # Display map
        st.components.v1.html(map_obj._repr_html_(), height=600)
        
        # Map statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Properties Mapped", len(geo_df))
        with col2:
            if 'neighbourhood' in geo_df.columns:
                st.metric("Neighbourhoods", geo_df['neighbourhood'].nunique())
            else:
                st.metric("Neighbourhoods", "N/A")
        with col3:
            price_cols = [col for col in geo_df.columns if 'price_clean' in col]
            if price_cols:
                avg_price = geo_df[price_cols[0]].mean()
                st.metric("Average Price", f"${avg_price:.0f}")
            else:
                st.metric("Average Price", "N/A")
    
    with tab2:
        st.subheader("Price Distribution by Location")
        
        # Price heatmap
        if 'price_clean' in geo_df.columns:
            fig = create_price_heatmap(geo_df, lat_col, lon_col)
            st.plotly_chart(fig, use_container_width=True)
            
            # Price statistics by area
            st.subheader("Price Statistics by Area")
            price_stats = geo_df.groupby('neighbourhood')['price_clean'].agg(['mean', 'median', 'count']).round(2)
            st.dataframe(price_stats)
        else:
            st.warning("No price data available for heatmap")
    
    with tab3:
        st.subheader("Rating Distribution by Location")
        
        # Rating map
        rating_cols = [col for col in geo_df.columns if 'rating' in col.lower() or 'score' in col.lower()]
        if rating_cols:
            rating_col = rating_cols[0]
            fig = create_rating_map(geo_df, lat_col, lon_col, rating_col)
            st.plotly_chart(fig, use_container_width=True)
            
            # Rating statistics
            st.subheader("Rating Statistics by Area")
            rating_stats = geo_df.groupby('neighbourhood')[rating_col].agg(['mean', 'count']).round(2)
            st.dataframe(rating_stats)
        else:
            st.warning("No rating data available for rating map")
    
    with tab4:
        st.subheader("Neighbourhood Performance Analysis")
        
        if 'neighbourhood' in geo_df.columns:
            # Neighbourhood statistics
            neighbourhood_analysis = analyze_neighbourhoods(geo_df)
            st.dataframe(neighbourhood_analysis)
            
            # Neighbourhood comparison chart
            fig = create_neighbourhood_comparison(neighbourhood_analysis)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No neighbourhood data available for analysis")

def create_interactive_map(df, lat_col, lon_col, color_by, map_type):
    """Create interactive Folium map"""
    import folium
    from folium.plugins import MarkerCluster
    
    # Calculate center
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()
    
    # Create base map
    if map_type == "OpenStreetMap":
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    elif map_type == "CartoDB Positron":
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB positron')
    else:
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB dark_matter')
    
    # Create marker clusters
    marker_cluster = MarkerCluster().add_to(m)
    
    # Color schemes
    if color_by == "Price":
        price_cols = [col for col in df.columns if 'price_clean' in col]
        if price_cols:
            price_col = price_cols[0]
            price_quartiles = df[price_col].quantile([0.25, 0.5, 0.75])
            colors = ['green', 'yellow', 'orange', 'red']
    elif color_by == "Rating":
        rating_cols = [col for col in df.columns if 'rating' in col.lower() or 'score' in col.lower()]
        if rating_cols:
            rating_col = rating_cols[0]
            rating_quartiles = df[rating_col].quantile([0.25, 0.5, 0.75])
            colors = ['red', 'orange', 'yellow', 'green']
    else:
        colors = ['blue'] * 4
    
    # Add markers
    for idx, row in df.iterrows():
        if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):
            # Determine color
            if color_by == "Price" and price_cols:
                price = row[price_col]
                if price <= price_quartiles[0.25]:
                    color = colors[0]
                elif price <= price_quartiles[0.5]:
                    color = colors[1]
                elif price <= price_quartiles[0.75]:
                    color = colors[2]
                else:
                    color = colors[3]
            elif color_by == "Rating" and rating_cols:
                rating = row[rating_col]
                if rating <= rating_quartiles[0.25]:
                    color = colors[0]
                elif rating <= rating_quartiles[0.5]:
                    color = colors[1]
                elif rating <= rating_quartiles[0.75]:
                    color = colors[2]
                else:
                    color = colors[3]
            elif color_by == "Room Type" and 'room_type' in row:
                room_type = row['room_type']
                if room_type == 'Entire home/apt':
                    color = 'green'
                elif room_type == 'Private room':
                    color = 'blue'
                elif room_type == 'Shared room':
                    color = 'orange'
                else:
                    color = 'gray'
            elif color_by == "Neighbourhood" and 'neighbourhood' in row:
                # Use hash of neighbourhood name for consistent colors
                import hashlib
                hash_object = hashlib.md5(row['neighbourhood'].encode())
                color_hash = int(hash_object.hexdigest(), 16)
                colors_list = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
                color = colors_list[color_hash % len(colors_list)]
            else:
                color = 'blue'
            
            # Create popup content
            popup_content = f"""
            <div style="width: 200px;">
                <h4>Property Details</h4>
                <p><b>Price:</b> ${row.get('price_clean', 'N/A'):,.0f}</p>
                <p><b>Room Type:</b> {row.get('room_type', 'N/A')}</p>
                <p><b>Rating:</b> {row.get('review_scores_rating', 'N/A')}</p>
                <p><b>Neighbourhood:</b> {row.get('neighbourhood', 'N/A')}</p>
                <p><b>Accommodates:</b> {row.get('accommodates', 'N/A')}</p>
            </div>
            """
            
            # Add marker
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=6,
                popup=folium.Popup(popup_content, max_width=300),
                color=color,
                fill=True,
                fillOpacity=0.7,
                weight=2
            ).add_to(marker_cluster)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def create_price_heatmap(df, lat_col, lon_col):
    """Create price heatmap"""
    import plotly.express as px
    
    # Sample data for performance (if too many points)
    if len(df) > 1000:
        df_sample = df.sample(n=1000, random_state=42)
    else:
        df_sample = df
    
    price_cols = [col for col in df_sample.columns if 'price_clean' in col]
    if not price_cols:
        return px.scatter()  # Empty plot
    
    price_col = price_cols[0]
    
    # Filter out rows with NaN values in required columns
    df_clean = df_sample.dropna(subset=[lat_col, lon_col, price_col])
    
    if len(df_clean) == 0:
        return px.scatter()  # Empty plot if no valid data
    
    # Check which columns exist for hover data
    available_hover_cols = []
    for col in ['room_type', 'accommodates', 'review_scores_rating', 'neighbourhood']:
        if col in df_clean.columns:
            available_hover_cols.append(col)
    
    fig = px.scatter_mapbox(
        df_clean,
        lat=lat_col,
        lon=lon_col,
        color=price_col,
        size=price_col,
        hover_name='neighbourhood' if 'neighbourhood' in df_clean.columns else None,
        hover_data=available_hover_cols,
        color_continuous_scale='Viridis',
        zoom=10,
        title="Price Distribution by Location"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    return fig

def create_rating_map(df, lat_col, lon_col, rating_col):
    """Create rating distribution map"""
    import plotly.express as px
    
    # Sample data for performance
    if len(df) > 1000:
        df_sample = df.sample(n=1000, random_state=42)
    else:
        df_sample = df
    
    # Filter out rows with NaN values in required columns
    df_clean = df_sample.dropna(subset=[lat_col, lon_col, rating_col])
    
    if len(df_clean) == 0:
        return px.scatter()  # Empty plot if no valid data
    
    # Check which columns exist for hover data
    available_hover_cols = []
    for col in ['room_type', 'price_clean', 'accommodates', 'neighbourhood']:
        if col in df_clean.columns:
            available_hover_cols.append(col)
    
    fig = px.scatter_mapbox(
        df_clean,
        lat=lat_col,
        lon=lon_col,
        color=rating_col,
        size=rating_col,
        hover_name='neighbourhood' if 'neighbourhood' in df_clean.columns else None,
        hover_data=available_hover_cols,
        color_continuous_scale='RdYlGn',
        zoom=10,
        title="Rating Distribution by Location"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    return fig

def analyze_neighbourhoods(df):
    """Analyze neighbourhood performance"""
    if 'neighbourhood' not in df.columns:
        return pd.DataFrame()
    
    # Check which columns exist for aggregation
    agg_dict = {'id': 'count'}
    
    price_cols = [col for col in df.columns if 'price_clean' in col]
    if price_cols:
        agg_dict[price_cols[0]] = ['mean', 'median', 'std']
    
    rating_cols = [col for col in df.columns if 'review_scores_rating' in col]
    if rating_cols:
        agg_dict[rating_cols[0]] = ['mean', 'count']
    
    if 'accommodates' in df.columns:
        agg_dict['accommodates'] = 'mean'
    
    analysis = df.groupby('neighbourhood').agg(agg_dict).round(2)
    
    # Flatten column names
    analysis.columns = ['_'.join(col).strip() for col in analysis.columns.values]
    
    # Rename columns for clarity
    column_mapping = {
        'id_count': 'Total_Listings'
    }
    
    if price_cols:
        column_mapping.update({
            f'{price_cols[0]}_mean': 'Avg_Price',
            f'{price_cols[0]}_median': 'Median_Price',
            f'{price_cols[0]}_std': 'Price_Std'
        })
    
    if rating_cols:
        column_mapping.update({
            f'{rating_cols[0]}_mean': 'Avg_Rating',
            f'{rating_cols[0]}_count': 'Rating_Count'
        })
    
    if 'accommodates' in df.columns:
        column_mapping['accommodates_mean'] = 'Avg_Accommodates'
    
    analysis = analysis.rename(columns=column_mapping)
    
    return analysis

def create_neighbourhood_comparison(neighbourhood_analysis):
    """Create neighbourhood comparison chart"""
    import plotly.express as px
    
    if neighbourhood_analysis.empty:
        return px.scatter()  # Empty plot
    
    # Reset index for plotting
    plot_data = neighbourhood_analysis.reset_index()
    
    # Check which columns exist for the plot
    x_col = 'Avg_Price' if 'Avg_Price' in plot_data.columns else None
    y_col = 'Avg_Rating' if 'Avg_Rating' in plot_data.columns else None
    size_col = 'Total_Listings' if 'Total_Listings' in plot_data.columns else None
    
    if not x_col or not y_col:
        return px.scatter()  # Empty plot if required columns don't exist
    
    hover_data = []
    for col in ['Median_Price', 'Price_Std']:
        if col in plot_data.columns:
            hover_data.append(col)
    
    fig = px.scatter(
        plot_data,
        x=x_col,
        y=y_col,
        size=size_col,
        color='neighbourhood',
        hover_data=hover_data,
        title="Neighbourhood Performance: Price vs Rating"
    )
    
    fig.update_layout(
        xaxis_title="Average Price ($)",
        yaxis_title="Average Rating"
    )
    
    return fig

def show_price_analysis(listings_df):
    """Show comprehensive price analysis for MVP"""
    st.markdown('<h1 class="main-header">💰 Price Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; font-style: italic; margin-bottom: 2rem;">📊 Copenhagen Airbnb Pricing Analysis • Market pricing trends and distribution patterns</p>', unsafe_allow_html=True)
    
    # Filters section
    st.markdown('<h2 class="subheader">🔍 Filter Options</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Neighbourhood filter
        if 'neighbourhood' in listings_df.columns:
            neighbourhoods = ['All'] + sorted(listings_df['neighbourhood'].unique())
            selected_neighbourhood = st.selectbox("Select Neighbourhood:", neighbourhoods)
        else:
            selected_neighbourhood = "All"
    
    with col2:
        # Room type filter
        if 'room_type' in listings_df.columns:
            room_types = ['All'] + sorted(listings_df['room_type'].unique())
            selected_room_type = st.selectbox("Select Room Type:", room_types)
        else:
            selected_room_type = "All"
    
    # Filter data
    filtered_df = listings_df.copy()
    
    if selected_neighbourhood != "All":
        filtered_df = filtered_df[filtered_df['neighbourhood'] == selected_neighbourhood]
    
    if selected_room_type != "All":
        filtered_df = filtered_df[filtered_df['room_type'] == selected_room_type]
    
    # Price analysis
    price_cols = [col for col in filtered_df.columns if 'price_clean' in col]
    
    if price_cols and len(filtered_df) > 0:
        price_col = price_cols[0]
        price_data = filtered_df[price_col].dropna()
        
        if len(price_data) > 0:
            # Price statistics
            st.markdown('<h2 class="subheader">📊 Price Statistics</h2>', unsafe_allow_html=True)
            
            # Calculate meaningful metrics
            metrics_to_show = []
            
            avg_price = price_data.mean()
            median_price = price_data.median()
            min_price = price_data.min()
            max_price = price_data.max()
            price_std = price_data.std()
            
            if avg_price > 0:
                metrics_to_show.append(("Average Price", f"${avg_price:.0f}"))
            if median_price > 0:
                metrics_to_show.append(("Median Price", f"${median_price:.0f}"))
            if min_price > 0 and max_price > 0:
                metrics_to_show.append(("Price Range", f"${min_price:.0f} - ${max_price:.0f}"))
            if price_std > 0:
                metrics_to_show.append(("Price Variance", f"${price_std:.0f}"))
            
            # Display metrics in columns
            if metrics_to_show:
                cols = st.columns(len(metrics_to_show))
                for i, (label, value) in enumerate(metrics_to_show):
                    with cols[i]:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(label, value)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No meaningful price data available for statistics.")
            
            # Price distribution chart
            st.markdown('<h2 class="subheader">📈 Price Distribution</h2>', unsafe_allow_html=True)
            
            fig = px.histogram(filtered_df, x=price_col, nbins=20,
                              title=f"Price Distribution for {selected_room_type} in {selected_neighbourhood}",
                              labels={price_col: "Price ($)"})
            st.plotly_chart(fig, use_container_width=True)
            
            # Price insights
            st.markdown('<h2 class="subheader">💡 Price Insights</h2>', unsafe_allow_html=True)
            
            # Calculate price quartiles
            q25, q50, q75 = price_data.quantile([0.25, 0.5, 0.75])
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>📊 Price Distribution Analysis:</h4>
                <ul>
                    <li><strong>Budget Tier (25th percentile):</strong> ${q25:.0f}</li>
                    <li><strong>Competitive Tier (50th percentile):</strong> ${q50:.0f}</li>
                    <li><strong>Premium Tier (75th percentile):</strong> ${q75:.0f}</li>
                    <li><strong>Price Spread:</strong> ${max_price - min_price:.0f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="warning-message">⚠️ No price data available for the selected filters.</div>', unsafe_allow_html=True)

def show_market_comparison(listings_df):
    """Show market comparison analysis for MVP"""
    st.markdown('<h1 class="main-header">🏆 Market Comparison</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; font-style: italic; margin-bottom: 2rem;">📊 Copenhagen Airbnb Market Comparison • Competitive positioning across neighbourhoods and room types</p>', unsafe_allow_html=True)
    
    # Market overview
    st.markdown('<h2 class="subheader">📊 Market Overview</h2>', unsafe_allow_html=True)
    
    # Calculate market metrics
    total_listings = len(listings_df)
    neighbourhood_count = listings_df['neighbourhood'].nunique() if 'neighbourhood' in listings_df.columns else 0
    room_type_count = listings_df['room_type'].nunique() if 'room_type' in listings_df.columns else 0
    
    price_cols = [col for col in listings_df.columns if 'price_clean' in col]
    market_avg_price = None
    if price_cols:
        price_data = listings_df[price_cols[0]].dropna()
        if len(price_data) > 0:
            market_avg_price = price_data.mean()
    
    # Display market metrics
    metrics_to_show = []
    
    if total_listings > 0:
        metrics_to_show.append(("Total Market Listings", f"{total_listings:,}"))
    if neighbourhood_count > 0:
        metrics_to_show.append(("Market Neighbourhoods", f"{neighbourhood_count}"))
    if room_type_count > 0:
        metrics_to_show.append(("Market Room Types", f"{room_type_count}"))
    if market_avg_price is not None:
        metrics_to_show.append(("Market Average Price", f"${market_avg_price:.0f}"))
    
    # Display metrics in columns
    if metrics_to_show:
        cols = st.columns(len(metrics_to_show))
        for i, (label, value) in enumerate(metrics_to_show):
            with cols[i]:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Neighbourhood comparison
    if 'neighbourhood' in listings_df.columns and listings_df['neighbourhood'].nunique() > 0:
        st.markdown('<h2 class="subheader">🏘️ Neighbourhood Comparison</h2>', unsafe_allow_html=True)
        
        neighbourhood_stats = listings_df.groupby('neighbourhood').agg({
            'id': 'count'
        }).rename(columns={'id': 'listing_count'})
        
        if price_cols and len(listings_df[price_cols[0]].dropna()) > 0:
            price_stats = listings_df.groupby('neighbourhood')[price_cols[0]].agg(['mean', 'median'])
            neighbourhood_stats = neighbourhood_stats.join(price_stats)
        
        fig = px.bar(neighbourhood_stats.reset_index(), x='neighbourhood', y='listing_count',
                     title="Listings by Neighbourhood")
        st.plotly_chart(fig, use_container_width=True)
    
    # Room type comparison
    if 'room_type' in listings_df.columns and listings_df['room_type'].nunique() > 0:
        st.markdown('<h2 class="subheader">🏠 Room Type Comparison</h2>', unsafe_allow_html=True)
        
        room_type_stats = listings_df.groupby('room_type').agg({
            'id': 'count'
        }).rename(columns={'id': 'listing_count'})
        
        if price_cols and len(listings_df[price_cols[0]].dropna()) > 0:
            price_stats = listings_df.groupby('room_type')[price_cols[0]].agg(['mean', 'median'])
            room_type_stats = room_type_stats.join(price_stats)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=room_type_stats['listing_count'], names=room_type_stats.index,
                        title="Room Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'mean' in room_type_stats.columns:
                fig = px.bar(room_type_stats.reset_index(), x='room_type', y='mean',
                             title="Average Price by Room Type")
                st.plotly_chart(fig, use_container_width=True)

def show_price_recommendations(listings_df):
    """Show actionable price recommendations for MVP"""
    st.markdown('<h1 class="main-header">🎯 Price Recommendations</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; font-style: italic; margin-bottom: 2rem;">📊 Copenhagen Airbnb Price Strategy • Actionable recommendations based on market analysis</p>', unsafe_allow_html=True)
    
    # Filters section
    st.markdown('<h2 class="subheader">🔍 Target Market</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Neighbourhood filter
        if 'neighbourhood' in listings_df.columns:
            neighbourhoods = ['All'] + sorted(listings_df['neighbourhood'].unique())
            selected_neighbourhood = st.selectbox("Select Neighbourhood:", neighbourhoods)
        else:
            selected_neighbourhood = "All"
    
    with col2:
        # Room type filter
        if 'room_type' in listings_df.columns:
            room_types = ['All'] + sorted(listings_df['room_type'].unique())
            selected_room_type = st.selectbox("Select Room Type:", room_types)
        else:
            selected_room_type = "All"
    
    # Filter data
    filtered_df = listings_df.copy()
    
    if selected_neighbourhood != "All":
        filtered_df = filtered_df[filtered_df['neighbourhood'] == selected_neighbourhood]
    
    if selected_room_type != "All":
        filtered_df = filtered_df[filtered_df['room_type'] == selected_room_type]
    
    # Price analysis
    price_cols = [col for col in filtered_df.columns if 'price_clean' in col]
    
    if price_cols and len(filtered_df) > 0:
        price_col = price_cols[0]
        price_data = filtered_df[price_col].dropna()
        
        if len(price_data) > 0:
            # Calculate price recommendations
            q25, q50, q75 = price_data.quantile([0.25, 0.5, 0.75])
            avg_price = price_data.mean()
            median_price = price_data.median()
            
            # Price positioning analysis
            st.markdown('<h2 class="subheader">📊 Market Positioning</h2>', unsafe_allow_html=True)
            
            # Calculate meaningful metrics
            metrics_to_show = []
            
            if avg_price > 0:
                metrics_to_show.append(("Market Average", f"${avg_price:.0f}"))
            if median_price > 0:
                metrics_to_show.append(("Market Median", f"${median_price:.0f}"))
            if q25 > 0:
                metrics_to_show.append(("Budget Tier", f"${q25:.0f}"))
            if q75 > 0:
                metrics_to_show.append(("Premium Tier", f"${q75:.0f}"))
            
            # Display metrics in columns
            if metrics_to_show:
                cols = st.columns(len(metrics_to_show))
                for i, (label, value) in enumerate(metrics_to_show):
                    with cols[i]:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(label, value)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            # Price recommendations
            st.markdown('<h2 class="subheader">💡 Strategic Price Recommendations</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="insight-box">
                    <h4>🎯 Competitive Pricing Strategy:</h4>
                    <ul>
                        <li><strong>Budget Range:</strong> ${price_data.min():.0f} - ${q25:.0f}</li>
                        <li><strong>Competitive Range:</strong> ${q25:.0f} - ${q50:.0f}</li>
                        <li><strong>Premium Range:</strong> ${q50:.0f} - ${q75:.0f}</li>
                        <li><strong>Luxury Range:</strong> ${q75:.0f} - ${price_data.max():.0f}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="insight-box">
                    <h4>📈 Pricing Strategy Tips:</h4>
                    <ul>
                        <li><strong>Start Competitive:</strong> Price at ${q25:.0f} - ${q50:.0f}</li>
                        <li><strong>Monitor Demand:</strong> Adjust based on booking rates</li>
                        <li><strong>Seasonal Adjustments:</strong> ±15% for peak/off-peak</li>
                        <li><strong>Dynamic Pricing:</strong> Use market data for optimization</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # Market insights
            st.markdown('<h2 class="subheader">📊 Market Insights</h2>', unsafe_allow_html=True)
            
            price_spread = price_data.max() - price_data.min()
            price_variance = price_data.std()
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>💡 Market Analysis:</h4>
                <ul>
                    <li><strong>Price Spread:</strong> ${price_spread:.0f} (${price_data.min():.0f} - ${price_data.max():.0f})</li>
                    <li><strong>Price Variance:</strong> ${price_variance:.0f}</li>
                    <li><strong>Market Concentration:</strong> {len(price_data)} listings analyzed</li>
                    <li><strong>Recommendation:</strong> {'High variance suggests room for premium pricing' if price_variance > avg_price * 0.3 else 'Low variance suggests competitive pricing needed'}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="warning-message">⚠️ No price data available for recommendations.</div>', unsafe_allow_html=True)

def show_main_dashboard(listings_df, calendar_df):
    """Show main dashboard with key insights and quick access to MVP features"""
    st.markdown('<h1 class="main-header">🏠 Airbnb Host Advisor - Main Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subheader">Your comprehensive overview of occupancy, pricing, and market insights</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; font-style: italic; margin-bottom: 2rem;">📊 Analyzing Copenhagen Airbnb market data • Focus on occupancy, pricing, market comparison, and actionable recommendations</p>', unsafe_allow_html=True)
    
    # Quick stats section
    st.markdown('<h2 class="subheader">📊 Quick Market Overview</h2>', unsafe_allow_html=True)
    
    # Calculate key metrics
    total_listings = len(listings_df)
    neighbourhood_count = listings_df['neighbourhood'].nunique() if 'neighbourhood' in listings_df.columns else 0
    room_type_count = listings_df['room_type'].nunique() if 'room_type' in listings_df.columns else 0
    
    price_cols = [col for col in listings_df.columns if 'price_clean' in col]
    market_avg_price = None
    if price_cols:
        price_data = listings_df[price_cols[0]].dropna()
        if len(price_data) > 0:
            market_avg_price = price_data.mean()
    
    # Occupancy metrics
    occupancy_rate = None
    total_days = None
    if calendar_df is not None and 'available' in calendar_df.columns:
        total_days = len(calendar_df)
        booked_days = (calendar_df['available'] == 'f').sum()
        occupancy_rate = (booked_days / total_days) * 100 if total_days > 0 else 0
    
    # Display key metrics
    metrics_to_show = []
    
    if total_listings > 0:
        metrics_to_show.append(("Total Listings", f"{total_listings:,}", "📈"))
    if neighbourhood_count > 0:
        metrics_to_show.append(("Neighbourhoods", f"{neighbourhood_count}", "🏘️"))
    if room_type_count > 0:
        metrics_to_show.append(("Room Types", f"{room_type_count}", "🏠"))
    if market_avg_price is not None:
        metrics_to_show.append(("Market Avg Price", f"${market_avg_price:.0f}", "💰"))
    if occupancy_rate is not None:
        metrics_to_show.append(("Occupancy Rate", f"{occupancy_rate:.1f}%", "📅"))
    if total_days is not None:
        metrics_to_show.append(("Calendar Days", f"{total_days:,}", "📊"))
    
    # Display metrics in a grid
    if metrics_to_show:
        cols = st.columns(len(metrics_to_show))
        for i, (label, value, icon) in enumerate(metrics_to_show):
            with cols[i]:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature cards section
    st.markdown('<h2 class="subheader">🚀 Quick Access to Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h4>📊 Occupancy Analysis</h4>
            <p>Analyze booking patterns, seasonal trends, and occupancy rates to optimize your availability strategy.</p>
            <ul>
                <li>Overall occupancy statistics</li>
                <li>Seasonal occupancy trends</li>
                <li>Occupancy vs price analysis</li>
                <li>Strategic recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <h4>💰 Price Analysis</h4>
            <p>Understand current market pricing, distribution patterns, and price positioning in your market.</p>
            <ul>
                <li>Comprehensive price statistics</li>
                <li>Price distribution analysis</li>
                <li>Market price quartiles</li>
                <li>Price variance insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h4>🏆 Market Comparison</h4>
            <p>Compare your position against competitors and understand market dynamics across neighbourhoods and room types.</p>
            <ul>
                <li>Market overview metrics</li>
                <li>Neighbourhood comparison</li>
                <li>Room type analysis</li>
                <li>Competitive positioning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <h4>🎯 Price Recommendations</h4>
            <p>Get actionable pricing strategies and recommendations based on market analysis and competitive positioning.</p>
            <ul>
                <li>Strategic pricing ranges</li>
                <li>Market positioning analysis</li>
                <li>Pricing strategy tips</li>
                <li>Dynamic pricing insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick insights section
    st.markdown('<h2 class="subheader">💡 Quick Insights</h2>', unsafe_allow_html=True)
    
    insights = []
    
    # Price insights
    if price_cols and len(listings_df[price_cols[0]].dropna()) > 0:
        price_data = listings_df[price_cols[0]].dropna()
        price_range = price_data.max() - price_data.min()
        price_variance = price_data.std()
        
        if price_variance > price_data.mean() * 0.3:
            insights.append("💰 <strong>High price variance</strong> suggests opportunities for premium pricing strategies")
        else:
            insights.append("💰 <strong>Low price variance</strong> indicates need for competitive pricing")
    
    # Occupancy insights
    if occupancy_rate is not None:
        if occupancy_rate > 70:
            insights.append("📊 <strong>High occupancy rate</strong> suggests strong demand - consider raising prices")
        elif occupancy_rate < 30:
            insights.append("📊 <strong>Low occupancy rate</strong> indicates need for competitive pricing or marketing")
        else:
            insights.append("📊 <strong>Moderate occupancy rate</strong> - focus on optimizing pricing strategy")
    
    # Market insights
    if neighbourhood_count > 0:
        insights.append(f"🏘️ <strong>{neighbourhood_count} neighbourhoods</strong> analyzed for market comparison")
    
    if room_type_count > 0:
        insights.append(f"🏠 <strong>{room_type_count} room types</strong> available for detailed analysis")
    
    # Display insights
    if insights:
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box" style="margin: 0.5rem 0;">
                <p>{insight}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No insights available with current data. Add more data to get personalized insights.")
    
    # Data status section
    st.markdown('<h2 class="subheader">📋 Data Status</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if calendar_df is not None:
            st.success("✅ Calendar data available for occupancy analysis")
        else:
            st.warning("⚠️ Calendar data not available - occupancy analysis disabled")
    
    with col2:
        if price_cols and len(listings_df[price_cols[0]].dropna()) > 0:
            st.success("✅ Price data available for pricing analysis")
        else:
            st.warning("⚠️ Price data not available - pricing analysis disabled")
    
    # Data source information
    st.markdown('<h2 class="subheader">📊 Data Source Information</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <h4>🌍 Copenhagen Airbnb Market Data</h4>
        <p>This analysis is based on comprehensive Airbnb market data from Copenhagen, Denmark, including:</p>
        <ul>
            <li><strong>Listings Data:</strong> Property details, pricing, amenities, and host information</li>
            <li><strong>Calendar Data:</strong> Availability and booking patterns over time</li>
            <li><strong>Geographic Coverage:</strong> Multiple neighbourhoods across Copenhagen</li>
            <li><strong>Property Types:</strong> Various room types and accommodation styles</li>
        </ul>
        <p><em>Note: This is a demonstration application using Copenhagen Airbnb data to showcase data analysis capabilities.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 