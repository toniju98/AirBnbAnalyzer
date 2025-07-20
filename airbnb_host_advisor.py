#!/usr/bin/env python3
"""
Airbnb Host Advisor - Streamlit Application
Provides insights for hosts on pricing, amenities, seasonal adjustments, and rating improvement.
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
    page_title="Airbnb Host Advisor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
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
    st.markdown('<h1 class="main-header">🏠 Airbnb Host Advisor</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-powered guide to maximize your Airbnb success")
    
    # Load data
    with st.spinner("Loading Airbnb data..."):
        listings_df, reviews_df, calendar_df = load_data()
    
    if listings_df is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Sidebar for navigation
    st.sidebar.title("📊 Analysis Sections")
    analysis_type = st.sidebar.selectbox(
        "Choose your analysis:",
        ["🏠 Property Overview", "💰 Optimal Pricing", "🏆 Amenity Analysis", 
         "📅 Seasonal Pricing", "⭐ Rating Improvement", "🗺️ Geographic Analysis", "🎯 Host Insights"]
    )
    
    # Clean price data
    price_cols = [col for col in listings_df.columns if 'price' in col.lower()]
    if price_cols:
        listings_df = clean_price_data(listings_df, price_cols[0])
    
    # Main content based on selection
    if analysis_type == "🏠 Property Overview":
        show_property_overview(listings_df, reviews_df, calendar_df)
    elif analysis_type == "💰 Optimal Pricing":
        show_optimal_pricing(listings_df)
    elif analysis_type == "🏆 Amenity Analysis":
        show_amenity_analysis(listings_df)
    elif analysis_type == "📅 Seasonal Pricing":
        show_seasonal_pricing(listings_df, calendar_df)
    elif analysis_type == "⭐ Rating Improvement":
        show_rating_improvement(listings_df, reviews_df)
    elif analysis_type == "🗺️ Geographic Analysis":
        show_geographic_analysis(listings_df)
    elif analysis_type == "🎯 Host Insights":
        show_host_insights(listings_df, reviews_df, calendar_df)

def show_property_overview(listings_df, reviews_df, calendar_df):
    """Show property overview and market insights"""
    st.header("🏠 Property Overview & Market Insights")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Listings", len(listings_df))
    
    with col2:
        if 'neighbourhood' in listings_df.columns:
            st.metric("Neighbourhoods", listings_df['neighbourhood'].nunique())
        else:
            st.metric("Neighbourhoods", "N/A")
    
    with col3:
        if 'room_type' in listings_df.columns:
            st.metric("Room Types", listings_df['room_type'].nunique())
        else:
            st.metric("Room Types", "N/A")
    
    with col4:
        price_cols = [col for col in listings_df.columns if 'price_clean' in col]
        if price_cols:
            avg_price = listings_df[price_cols[0]].mean()
            st.metric("Avg Price", f"${avg_price:.0f}")
        else:
            st.metric("Avg Price", "N/A")
    
    # Market analysis
    st.subheader("📊 Market Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution
        price_cols = [col for col in listings_df.columns if 'price_clean' in col]
        if price_cols:
            fig = px.histogram(listings_df, x=price_cols[0], nbins=30,
                              title="Price Distribution",
                              labels={price_cols[0]: "Price ($)"})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Room type distribution
        if 'room_type' in listings_df.columns:
            room_counts = listings_df['room_type'].value_counts()
            fig = px.pie(values=room_counts.values, names=room_counts.index,
                        title="Room Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    # Neighbourhood analysis
    if 'neighbourhood' in listings_df.columns:
        st.subheader("🏘️ Neighbourhood Analysis")
        
        neighbourhood_stats = listings_df.groupby('neighbourhood').agg({
            'id': 'count'
        }).rename(columns={'id': 'listing_count'})
        
        if price_cols:
            price_stats = listings_df.groupby('neighbourhood')[price_cols[0]].agg(['mean', 'median'])
            neighbourhood_stats = neighbourhood_stats.join(price_stats)
        
        fig = px.bar(neighbourhood_stats.reset_index(), x='neighbourhood', y='listing_count',
                     title="Listings by Neighbourhood")
        st.plotly_chart(fig, use_container_width=True)

def show_optimal_pricing(listings_df):
    """Show optimal pricing analysis"""
    st.header("💰 Optimal Pricing Analysis")
    
    # Filters
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
            # Pricing insights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Average Price", f"${price_data.mean():.0f}")
            
            with col2:
                st.metric("Median Price", f"${price_data.median():.0f}")
            
            with col3:
                st.metric("Price Range", f"${price_data.min():.0f} - ${price_data.max():.0f}")
            
            # Price distribution
            fig = px.histogram(filtered_df, x=price_col, nbins=20,
                              title=f"Price Distribution for {selected_room_type} in {selected_neighbourhood}",
                              labels={price_col: "Price ($)"})
            st.plotly_chart(fig, use_container_width=True)
            
            # Pricing recommendations
            st.subheader("💡 Pricing Recommendations")
            
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
        st.warning("No price data available for the selected filters.")

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

def show_rating_improvement(listings_df, reviews_df):
    """Show rating improvement analysis"""
    st.header("⭐ Rating Improvement Analysis")
    
    # Rating analysis
    rating_cols = [col for col in listings_df.columns if 'rating' in col.lower() or 'score' in col.lower()]
    
    if rating_cols:
        rating_col = rating_cols[0]
        rating_data = listings_df[rating_col].dropna()
        
        if len(rating_data) > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Average Rating", f"{rating_data.mean():.1f}/5")
            
            with col2:
                st.metric("Median Rating", f"{rating_data.median():.1f}/5")
            
            with col3:
                st.metric("Rating Distribution", f"{len(rating_data)} listings")
            
            # Rating distribution
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
                    fig = px.scatter(analysis_df, x=price_col, y=rating_col,
                                    title="Rating vs Price",
                                    labels={price_col: "Price ($)", rating_col: "Rating"})
                    st.plotly_chart(fig, use_container_width=True)
            
            # Rating improvement tips
            st.subheader("💡 Rating Improvement Tips")
            
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
        st.warning("No rating data available for analysis.")

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

if __name__ == "__main__":
    main() 