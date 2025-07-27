#!/usr/bin/env python3
"""
Airbnb Host Dashboard - Analytics and Market Insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_calendar import calendar

# Import our modules
from utils.data_loader import load_booking_data, load_city_data
from analytics.analysis import analyze_occupancy, analyze_revenue, analyze_pricing, analyze_city_market, analyze_review_patterns, analyze_copenhagen_occupancy, analyze_enhanced_review_patterns
from components.ui import get_custom_css, render_success_message, render_error_message, render_upload_instructions, render_dashboard_features

# Page configuration
st.set_page_config(
    page_title="Airbnb Host Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Page rendering functions
def render_data_analysis_page(df, uploaded_files, date_cols, price_cols):
    """Render the main data analysis page"""
    if not uploaded_files:
        st.markdown("### 📁 Upload Your Airbnb Data")
        st.markdown("Upload one or more CSV exports of your Airbnb bookings. The app will automatically detect date and price columns.")
        render_upload_instructions()
        return
    
    if df is not None and len(df) > 0:
        st.markdown(f'<div class="success-message">✅ Successfully loaded {len(uploaded_files)} file(s) with {len(df)} total bookings!</div>', unsafe_allow_html=True)
        
        # Show data preview
        st.markdown("### 📊 Data Preview")
        st.write(f"**Files uploaded:** {len(uploaded_files)}")
        st.write(f"**Total bookings:** {len(df)}")
        st.write(f"**Date columns found:** {date_cols}")
        st.write(f"**Price columns found:** {price_cols}")
        
        # Show file names
        if len(uploaded_files) > 1:
            st.write("**Files processed:**")
            for i, file in enumerate(uploaded_files, 1):
                st.write(f"  {i}. {file.name}")
        
        # Data preview
        st.dataframe(df.head(), use_container_width=True)
        
        # Quick overview of all analyses
        st.markdown("### 🎯 Quick Overview")
        render_dashboard_features()
    else:
        st.error("❌ Failed to load data. Please check your CSV files.")

def render_occupancy_analysis_page(df, date_cols, uploaded_files):
    """Render occupancy analysis page"""
    if not uploaded_files:
        st.warning("📁 Please upload your data first using the sidebar.")
        return
    
    if df is None or not date_cols:
        st.error("❌ No date columns found in your data. Please upload files with date information.")
        return
    
    st.markdown("### 📈 Occupancy Analysis")
    
    occupancy_data = analyze_occupancy(df, date_cols)
    if occupancy_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Bookings", f"{occupancy_data['total_bookings']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Unique Dates", f"{occupancy_data['unique_dates']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            avg_bookings_per_date = occupancy_data['total_bookings'] / occupancy_data['unique_dates']
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Bookings/Day", f"{avg_bookings_per_date:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Monthly occupancy chart
        if not occupancy_data['monthly_occupancy'].empty:
            fig = px.line(occupancy_data['monthly_occupancy'], 
                        x='date', y='bookings',
                        title="Monthly Booking Trends")
            st.plotly_chart(fig, use_container_width=True)
        
        # Day of week occupancy
        if not occupancy_data['dow_occupancy'].empty:
            fig = px.bar(x=occupancy_data['dow_occupancy'].index, 
                       y=occupancy_data['dow_occupancy'].values,
                       title="Bookings by Day of Week")
            st.plotly_chart(fig, use_container_width=True)

def render_revenue_analysis_page(df, price_cols, uploaded_files):
    """Render revenue analysis page"""
    if not uploaded_files:
        st.warning("📁 Please upload your data first using the sidebar.")
        return
    
    if df is None or not price_cols:
        st.error("❌ No price columns found in your data. Please upload files with price information.")
        return
    
    st.markdown("### 💰 Revenue Analysis")
    
    revenue_data = analyze_revenue(df, price_cols)
    if revenue_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Revenue", f"${revenue_data['total_revenue']:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Revenue/Booking", f"${revenue_data['avg_revenue_per_booking']:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Bookings", f"{len(df):,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Monthly revenue chart
        if not revenue_data['revenue_by_month'].empty:
            fig = px.line(revenue_data['revenue_by_month'], 
                        x='date', y='price',
                        title="Monthly Revenue Trends")
            st.plotly_chart(fig, use_container_width=True)

def render_pricing_analysis_page(df, date_cols, price_cols, uploaded_files):
    """Render pricing analysis page"""
    if not uploaded_files:
        st.warning("📁 Please upload your data first using the sidebar.")
        return
    
    if df is None or not price_cols or not date_cols:
        st.error("❌ Need both date and price columns for pricing analysis.")
        return
    
    st.markdown("### 💵 Pricing Analysis")
    
    pricing_data = analyze_pricing(df, price_cols, date_cols)
    if pricing_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Average Price", f"${pricing_data['avg_price']:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Median Price", f"${pricing_data['median_price']:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Bookings", f"{len(df):,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Price trend chart
        if not pricing_data['price_trend'].empty:
            fig = px.line(pricing_data['price_trend'], 
                        x='date', y='price',
                        title="Price Trends Over Time")
            st.plotly_chart(fig, use_container_width=True)

def render_city_market_page(listings_df, calendar_df, city_data_loaded):
    """Render city market insights page"""
    if not city_data_loaded:
        st.error("❌ Copenhagen market data not available. Please ensure the data files are in the project directory.")
        st.markdown("""
        <div class="insight-box">
            <h4>📋 Required Data Files:</h4>
            <ul>
                <li><strong>listings.csv</strong> or <strong>listings.csv.gz</strong> - Property listings</li>
                <li><strong>calendar.csv.gz</strong> - Availability data (optional)</li>
                <li><strong>reviews.csv</strong> or <strong>reviews.csv.gz</strong> - Guest reviews (optional)</li>
            </ul>
            <p><em>These files should be placed in the same directory as the application.</em></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("### 🏙️ Copenhagen Market Insights")
    st.markdown("Explore market statistics and trends for Copenhagen to understand the competitive landscape.")
    
    # Analyze city market
    city_stats = analyze_city_market(listings_df, calendar_df)
    
    if city_stats:
        # Market overview
        st.markdown("### 📊 Market Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Listings", f"{city_stats['total_listings']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Neighbourhoods", f"{city_stats['neighbourhoods']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Room Types", f"{city_stats['room_types']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            if city_stats['calendar_analysis'] and 'basic_stats' in city_stats['calendar_analysis']:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Occupancy Rate", f"{city_stats['calendar_analysis']['basic_stats']['occupancy_rate']:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Occupancy Rate", "N/A")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Price analysis
        if city_stats['price_stats']:
            st.markdown("### 💰 Market Pricing")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Average Price", f"${city_stats['price_stats']['avg_price']:.0f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Median Price", f"${city_stats['price_stats']['median_price']:.0f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Min Price", f"${city_stats['price_stats']['min_price']:.0f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Max Price", f"${city_stats['price_stats']['max_price']:.0f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Price distribution
            fig = px.histogram(x=city_stats['price_stats']['price_distribution'], nbins=30,
                             title="Copenhagen Price Distribution",
                             labels={'x': 'Price ($)', 'y': 'Number of Listings'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Neighbourhood analysis
        if not city_stats['neighbourhood_stats'].empty:
            st.markdown("### 🏘️ Neighbourhood Analysis")
            
            # Top neighbourhoods by listings
            top_neighbourhoods = city_stats['neighbourhood_stats'].sort_values('listings', ascending=False).head(10)
            
            fig = px.bar(top_neighbourhoods.reset_index(), x='neighbourhood', y='listings',
                       title="Top 10 Neighbourhoods by Listings")
            st.plotly_chart(fig, use_container_width=True)
            
            # Neighbourhood price comparison
            if 'avg_price' in top_neighbourhoods.columns:
                fig = px.bar(top_neighbourhoods.reset_index(), x='neighbourhood', y='avg_price',
                           title="Average Price by Neighbourhood")
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed neighbourhood table
            st.markdown("#### 📋 Neighbourhood Statistics")
            st.dataframe(city_stats['neighbourhood_stats'].round(2), use_container_width=True)
        
        # Room type analysis
        if not city_stats['room_type_stats'].empty:
            st.markdown("### 🏠 Room Type Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Room type distribution
                fig = px.pie(values=city_stats['room_type_stats']['listings'], 
                           names=city_stats['room_type_stats'].index,
                           title="Room Type Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Room type pricing
                if 'avg_price' in city_stats['room_type_stats'].columns:
                    fig = px.bar(city_stats['room_type_stats'].reset_index(), x='room_type', y='avg_price',
                               title="Average Price by Room Type")
                    st.plotly_chart(fig, use_container_width=True)
            
            # Detailed room type table
            st.markdown("#### 📋 Room Type Statistics")
            st.dataframe(city_stats['room_type_stats'].round(2), use_container_width=True)

def render_review_analysis_page(reviews_df, listings_df, city_data_loaded):
    """Render enhanced review analysis page"""
    if not city_data_loaded:
        st.error("❌ Copenhagen market data not available. Please ensure the data files are in the project directory.")
        return
    
    st.markdown("### 📝 Enhanced Review Analysis")
    st.markdown("Analyzing review patterns and listing review metrics to understand guest feedback trends.")
    
    review_data = analyze_enhanced_review_patterns(reviews_df, listings_df)
    
    if review_data:
        # Review statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Reviews", f"{review_data['total_reviews']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Reviews/Day", f"{review_data['avg_reviews_per_day']:.1f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            # Find the day with most reviews
            most_reviews_day = review_data['reviews_by_day'].idxmax()
            most_reviews_count = review_data['reviews_by_day'].max()
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Peak Review Day", f"{most_reviews_day}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Reviews by day of week chart
        st.markdown("#### 📊 Reviews by Day of Week")
        
        # Create the chart
        fig = px.bar(
            x=review_data['reviews_by_day'].index,
            y=review_data['reviews_by_day'].values,
            title="Number of Reviews by Day of Week",
            labels={'x': 'Day of Week', 'y': 'Number of Reviews'},
            color=review_data['reviews_by_day'].values,
            color_continuous_scale='viridis'
        )
        
        # Update layout for better presentation
        fig.update_layout(
            xaxis={'categoryorder': 'array', 'categoryarray': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Review insights
        st.markdown("#### 💡 Review Insights")
        
        review_insights = []
        
        # Find peak and lowest review days
        peak_day = review_data['reviews_by_day'].idxmax()
        peak_count = review_data['reviews_by_day'].max()
        peak_pct = review_data['reviews_by_day_pct'].max()
        
        lowest_day = review_data['reviews_by_day'].idxmin()
        lowest_count = review_data['reviews_by_day'].min()
        lowest_pct = review_data['reviews_by_day_pct'].min()
        
        review_insights.append(f"📈 **Peak Review Day:** {peak_day} with {peak_count:,} reviews ({peak_pct}% of total)")
        review_insights.append(f"📉 **Lowest Review Day:** {lowest_day} with {lowest_count:,} reviews ({lowest_pct}% of total)")
        
        # Weekend vs weekday analysis
        weekend_days = ['Saturday', 'Sunday']
        weekday_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        weekend_reviews = review_data['reviews_by_day'][weekend_days].sum()
        weekday_reviews = review_data['reviews_by_day'][weekday_days].sum()
        
        weekend_pct = (weekend_reviews / review_data['total_reviews'] * 100).round(1)
        weekday_pct = (weekday_reviews / review_data['total_reviews'] * 100).round(1)
        
        review_insights.append(f"📅 **Weekend vs Weekday:** {weekend_pct}% of reviews on weekends, {weekday_pct}% on weekdays")
        
        # Display review insights
        for insight in review_insights:
            st.markdown(f"""
            <div class="insight-box">
                <p>{insight}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Review Analysis - New Features from Listings Data
        if 'review_stats' in review_data and review_data['review_stats']:
            st.markdown("### 📊 Enhanced Review Metrics Analysis")
            st.markdown("Analysis of review-related features from listings data to understand review patterns and distribution.")
            
            # Review statistics overview
            st.markdown("#### 📈 Review Statistics Overview")
            
            review_stats = review_data['review_stats']
            available_features = list(review_stats.keys())
            
            if available_features:
                # Create metrics for each feature
                num_features = len(available_features)
                cols = st.columns(min(num_features, 4))
                
                for i, feature in enumerate(available_features):
                    with cols[i % 4]:
                        stats = review_stats[feature]
                        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                        st.metric(
                            f"{feature.replace('_', ' ').title()}",
                            f"{stats['mean']:.1f}",
                            help=f"Mean: {stats['mean']:.1f}, Median: {stats['median']:.1f}, Std: {stats['std']:.1f}"
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Zero reviews analysis
                st.markdown("#### 🔍 Zero Reviews Analysis")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if 'number_of_reviews' in review_stats:
                        stats = review_stats['number_of_reviews']
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Listings with 0 Reviews", f"{stats['zero_reviews']:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    if 'number_of_reviews' in review_stats:
                        stats = review_stats['number_of_reviews']
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("0 Reviews %", f"{stats['zero_reviews_pct']:.1f}%")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    if 'number_of_reviews' in review_stats:
                        stats = review_stats['number_of_reviews']
                        active_listings = stats['total_listings'] - stats['zero_reviews']
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Active Listings", f"{active_listings:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Distribution plots for review features
                if 'review_distributions' in review_data and review_data['review_distributions']:
                    st.markdown("#### 📊 Review Distributions")
                    
                    distributions = review_data['review_distributions']
                    
                    # Create distribution charts
                    for feature, distribution in distributions.items():
                        if not distribution.empty:
                            fig = px.bar(
                                x=distribution.index,
                                y=distribution.values,
                                title=f"{feature.replace('_', ' ').title()} Distribution",
                                labels={'x': 'Range', 'y': 'Number of Listings'},
                                color=distribution.values,
                                color_continuous_scale='viridis'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                

                
                # Room type analysis
                if 'room_type_reviews' in review_data and review_data['room_type_reviews']:
                    st.markdown("#### 🏠 Review Metrics by Room Type")
                    
                    room_type_data = review_data['room_type_reviews']
                    
                    for feature, room_stats in room_type_data.items():
                        if not room_stats.empty:
                            # Create bar chart for mean values
                            fig = px.bar(
                                x=room_stats.index,
                                y=room_stats['mean'],
                                title=f"Average {feature.replace('_', ' ').title()} by Room Type",
                                labels={'x': 'Room Type', 'y': f'Average {feature.replace("_", " ").title()}'},
                                color=room_stats['mean'],
                                color_continuous_scale='viridis'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Display detailed table
                            st.markdown(f"**Detailed Statistics for {feature.replace('_', ' ').title()}:**")
                            st.dataframe(room_stats.round(2), use_container_width=True)
                
                # Neighbourhood analysis
                if 'neighbourhood_reviews' in review_data and review_data['neighbourhood_reviews']:
                    st.markdown("#### 🏘️ Review Metrics by Neighbourhood")
                    
                    neighbourhood_data = review_data['neighbourhood_reviews']
                    
                    for feature, neighbourhood_stats in neighbourhood_data.items():
                        if not neighbourhood_stats.empty:
                            # Create bar chart for mean values (top 10)
                            top_neighbourhoods = neighbourhood_stats.sort_values('mean', ascending=False).head(10)
                            
                            fig = px.bar(
                                x=top_neighbourhoods.index,
                                y=top_neighbourhoods['mean'],
                                title=f"Top 10 Neighbourhoods by Average {feature.replace('_', ' ').title()}",
                                labels={'x': 'Neighbourhood', 'y': f'Average {feature.replace("_", " ").title()}'},
                                color=top_neighbourhoods['mean'],
                                color_continuous_scale='viridis'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Display detailed table
                            st.markdown(f"**Detailed Statistics for {feature.replace('_', ' ').title()}:**")
                            st.dataframe(neighbourhood_stats.round(2), use_container_width=True)
                
                # Key insights for enhanced review analysis
                st.markdown("#### 💡 Enhanced Review Insights")
                
                enhanced_insights = []
                
                # Zero reviews insight
                if 'number_of_reviews' in review_stats:
                    stats = review_stats['number_of_reviews']
                    enhanced_insights.append(f"📊 **{stats['zero_reviews_pct']:.1f}% of listings have no reviews** ({stats['zero_reviews']:,} out of {stats['total_listings']:,} listings)")
                
                # Reviews per month insight
                if 'reviews_per_month' in review_stats:
                    stats = review_stats['reviews_per_month']
                    enhanced_insights.append(f"📅 **Average reviews per month:** {stats['mean']:.1f} (median: {stats['median']:.1f})")
                
                # Last 12 months reviews insight
                if 'number_of_reviews_ltm' in review_stats:
                    stats = review_stats['number_of_reviews_ltm']
                    enhanced_insights.append(f"📈 **Last 12 months:** Average {stats['mean']:.1f} reviews per listing (median: {stats['median']:.1f})")
                
                # Room type insights
                if 'room_type_reviews' in review_data and 'number_of_reviews' in review_data['room_type_reviews']:
                    room_stats = review_data['room_type_reviews']['number_of_reviews']
                    if not room_stats.empty:
                        best_room_type = room_stats['mean'].idxmax()
                        best_avg = room_stats['mean'].max()
                        enhanced_insights.append(f"🏠 **{best_room_type}** has the highest average reviews ({best_avg:.1f})")
                
                # Neighbourhood insights
                if 'neighbourhood_reviews' in review_data and 'number_of_reviews' in review_data['neighbourhood_reviews']:
                    neighbourhood_stats = review_data['neighbourhood_reviews']['number_of_reviews']
                    if not neighbourhood_stats.empty:
                        best_neighbourhood = neighbourhood_stats['mean'].idxmax()
                        best_avg = neighbourhood_stats['mean'].max()
                        enhanced_insights.append(f"🏘️ **{best_neighbourhood}** has the highest average reviews ({best_avg:.1f})")
                
                # Display enhanced insights
                for insight in enhanced_insights:
                    st.markdown(f"""
                    <div class="insight-box">
                        <p>{insight}</p>
                    </div>
                    """, unsafe_allow_html=True)

def render_copenhagen_occupancy_page(calendar_df, listings_df, city_data_loaded):
    """Render Copenhagen occupancy analysis page"""
    if not city_data_loaded:
        st.error("❌ Copenhagen market data not available. Please ensure the data files are in the project directory.")
        return
    
    st.markdown("### 📊 Copenhagen Market Occupancy Analysis")
    st.markdown("Analyze which days have more bookings and which have fewer in the Copenhagen market.")
    
    # Load full calendar data for comprehensive analysis
    with st.spinner("Loading Copenhagen occupancy data..."):
        from utils.data_loader import load_full_calendar_data
        full_calendar_df = load_full_calendar_data()
        
        if full_calendar_df is not None:
            calendar_df = full_calendar_df
    
    if calendar_df is None or calendar_df.empty:
        st.error("❌ No calendar data available for occupancy analysis.")
        return
    
    # Analyze Copenhagen occupancy with listings data for availability_365 analysis
    occupancy_data = analyze_copenhagen_occupancy(calendar_df, listings_df)
    
    if occupancy_data:
        # Overview metrics
        st.markdown("### 📈 Market Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Days Analyzed", f"{occupancy_data['total_days']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Booked Days", f"{occupancy_data['booked_days']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Available Days", f"{occupancy_data['available_days']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Occupancy Rate", f"{occupancy_data['occupancy_rate']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Peak and low occupancy insights
        st.markdown("### 🎯 Peak & Low Occupancy Days")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"""
            <h4>📈 Peak Occupancy Day</h4>
            <p><strong>{occupancy_data['peak_day']}</strong> with {occupancy_data['peak_bookings']:,} bookings</p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"""
            <h4>📉 Lowest Occupancy Day</h4>
            <p><strong>{occupancy_data['low_day']}</strong> with {occupancy_data['low_bookings']:,} bookings</p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Weekend vs Weekday analysis
        st.markdown("### 📅 Weekend vs Weekday Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Weekend Bookings", f"{occupancy_data['weekend_bookings']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Weekday Bookings", f"{occupancy_data['weekday_bookings']:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Weekend vs Weekday percentage
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Weekend %", f"{occupancy_data['weekend_pct']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Weekday %", f"{occupancy_data['weekday_pct']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Day of week occupancy chart
        st.markdown("### 📊 Occupancy by Day of Week")
        
        if not occupancy_data['dow_occupancy'].empty:
            fig = px.bar(
                x=occupancy_data['dow_occupancy'].index,
                y=occupancy_data['dow_occupancy'].values,
                title="Copenhagen Market: Bookings by Day of Week",
                labels={'x': 'Day of Week', 'y': 'Number of Bookings'},
                color=occupancy_data['dow_occupancy'].values,
                color_continuous_scale='viridis'
            )
            
            # Update layout for better presentation
            fig.update_layout(
                xaxis={'categoryorder': 'array', 'categoryarray': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Monthly occupancy trends
        st.markdown("### 📈 Monthly Occupancy Trends")
        
        if not occupancy_data['monthly_occupancy'].empty:
            fig = px.line(
                occupancy_data['monthly_occupancy'],
                x='date',
                y='booked_days',
                title="Copenhagen Market: Monthly Booking Trends"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Day of month occupancy (shows patterns within months)
        st.markdown("### 📅 Occupancy by Day of Month")
        
        if not occupancy_data['day_of_month_occupancy'].empty:
            fig = px.bar(
                x=occupancy_data['day_of_month_occupancy'].index,
                y=occupancy_data['day_of_month_occupancy'].values,
                title="Copenhagen Market: Bookings by Day of Month",
                labels={'x': 'Day of Month', 'y': 'Number of Bookings'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Quarterly analysis
        st.markdown("### 🍂 Seasonal Occupancy Analysis")
        
        if not occupancy_data['quarterly_occupancy'].empty:
            fig = px.bar(
                occupancy_data['quarterly_occupancy'],
                x='quarter',
                y='booked_days',
                title="Copenhagen Market: Quarterly Booking Trends",
                labels={'x': 'Quarter', 'y': 'Number of Bookings'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.markdown("### 💡 Key Insights")
        
        insights = []
        
        # Peak day insight
        if occupancy_data['peak_day']:
            peak_pct = (occupancy_data['peak_bookings'] / occupancy_data['booked_days'] * 100).round(1)
            insights.append(f"📈 **{occupancy_data['peak_day']}** is the busiest day with {occupancy_data['peak_bookings']:,} bookings ({peak_pct}% of total)")
        
        # Low day insight
        if occupancy_data['low_day']:
            low_pct = (occupancy_data['low_bookings'] / occupancy_data['booked_days'] * 100).round(1)
            insights.append(f"📉 **{occupancy_data['low_day']}** is the quietest day with {occupancy_data['low_bookings']:,} bookings ({low_pct}% of total)")
        
        # Weekend vs weekday insight
        if occupancy_data['weekend_pct'] > occupancy_data['weekday_pct']:
            insights.append(f"🎉 **Weekends are busier** with {occupancy_data['weekend_pct']:.1f}% of bookings vs {occupancy_data['weekday_pct']:.1f}% on weekdays")
        else:
            insights.append(f"💼 **Weekdays are busier** with {occupancy_data['weekday_pct']:.1f}% of bookings vs {occupancy_data['weekend_pct']:.1f}% on weekends")
        
        # Overall occupancy insight
        if occupancy_data['occupancy_rate'] > 50:
            insights.append(f"🔥 **High occupancy market** with {occupancy_data['occupancy_rate']:.1f}% overall occupancy rate")
        else:
            insights.append(f"📊 **Moderate occupancy market** with {occupancy_data['occupancy_rate']:.1f}% overall occupancy rate")
        
        # Display insights
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box">
                <p>{insight}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced analysis with availability_365
        if occupancy_data.get('availability_analysis'):
            st.markdown("### 🏠 Availability 365 Analysis")
            st.markdown("Analysis of listing availability patterns for the next 365 days.")
            
            availability_data = occupancy_data['availability_analysis']
            
            # Overview metrics
            st.markdown("#### 📊 Availability Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Total Listings", f"{availability_data['total_listings']:,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("High Availability", f"{availability_data['high_availability_count']:,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Low Availability", f"{availability_data['low_availability_count']:,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                avg_availability = availability_data['stats']['mean']
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Avg Availability", f"{avg_availability:.0f} days")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Availability distribution
            st.markdown("#### 📈 Availability Distribution")
            
            if not availability_data['distribution'].empty:
                fig = px.pie(
                    values=availability_data['distribution'].values,
                    names=availability_data['distribution'].index,
                    title="Distribution of Listings by Availability Level"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Availability by room type
            if availability_data['by_room_type'] is not None:
                st.markdown("#### 🏘️ Availability by Room Type")
                
                room_availability = availability_data['by_room_type'].reset_index()
                fig = px.bar(
                    room_availability,
                    x='room_type',
                    y='mean',
                    title="Average Availability by Room Type",
                    labels={'mean': 'Average Days Available', 'room_type': 'Room Type'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Top neighbourhoods by availability
            if availability_data['top_neighbourhoods'] is not None:
                st.markdown("#### 🏙️ Top Neighbourhoods by Availability")
                
                top_neighbourhoods = availability_data['top_neighbourhoods'].reset_index()
                fig = px.bar(
                    top_neighbourhoods,
                    x='neighbourhood',
                    y='mean',
                    title="Top 10 Neighbourhoods by Average Availability",
                    labels={'mean': 'Average Days Available', 'neighbourhood': 'Neighbourhood'}
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            # Key availability insights
            st.markdown("#### 💡 Availability Insights")
            
            availability_insights = []
            
            # High availability insight
            if availability_data['high_availability_pct'] > 20:
                availability_insights.append(f"📈 **High availability market**: {availability_data['high_availability_pct']:.1f}% of listings are available for 300+ days")
            else:
                availability_insights.append(f"📊 **Moderate availability market**: {availability_data['high_availability_pct']:.1f}% of listings are available for 300+ days")
            
            # Low availability insight
            if availability_data['low_availability_pct'] > 30:
                availability_insights.append(f"🔥 **High demand market**: {availability_data['low_availability_pct']:.1f}% of listings are available for less than 30 days")
            else:
                availability_insights.append(f"📉 **Moderate demand market**: {availability_data['low_availability_pct']:.1f}% of listings are available for less than 30 days")
            
            # Average availability insight
            if avg_availability > 200:
                availability_insights.append(f"🏠 **High availability**: Average listing is available for {avg_availability:.0f} days")
            elif avg_availability > 100:
                availability_insights.append(f"🏠 **Moderate availability**: Average listing is available for {avg_availability:.0f} days")
            else:
                availability_insights.append(f"🏠 **Low availability**: Average listing is available for {avg_availability:.0f} days")
            
            # Display availability insights
            for insight in availability_insights:
                st.markdown(f"""
                <div class="insight-box">
                    <p>{insight}</p>
                </div>
                """, unsafe_allow_html=True)

def render_calendar_analysis_page(calendar_df, listings_df, city_data_loaded):
    """Render calendar analysis page"""
    if not city_data_loaded:
        st.error("❌ Copenhagen market data not available. Please ensure the data files are in the project directory.")
        return
    
    st.markdown("### 📅 Calendar Analysis")
    st.markdown("Analyze availability patterns and booking trends across the market.")
    
    # Individual Listing Calendar Analysis
    if calendar_df is not None and 'listing_id' in calendar_df.columns:
        st.markdown("### 🏠 Individual Listing Calendar Analysis")
        st.markdown("Select a specific listing to view its detailed calendar and availability patterns.")
        
        with st.spinner("Loading listing data..."):
            # Get unique listings for dropdown from the sample data
            unique_listings = calendar_df['listing_id'].unique()
        
        # Create a mapping of listing IDs to display names
        if listings_df is not None and 'id' in listings_df.columns and 'name' in listings_df.columns:
            # Create a mapping from listing ID to name
            listing_names = {}
            for _, row in listings_df.iterrows():
                if pd.notna(row['id']) and pd.notna(row['name']):
                    listing_names[row['id']] = f"{row['name'][:50]}..." if len(str(row['name'])) > 50 else str(row['name'])
            
            # Create dropdown options
            dropdown_options = []
            for listing_id in unique_listings[:100]:  # Limit to first 100 for performance
                if listing_id in listing_names:
                    dropdown_options.append(f"{listing_id} - {listing_names[listing_id]}")
                else:
                    dropdown_options.append(f"Listing {listing_id}")
            
            # Add "All Listings" option
            dropdown_options.insert(0, "All Listings (Market Overview)")
            
            # Create dropdown
            selected_option = st.selectbox(
                "Select a listing to analyze:",
                dropdown_options,
                help="Choose a specific listing to view its calendar data, or select 'All Listings' for market overview"
            )
            
            # Parse selected listing ID
            if selected_option == "All Listings (Market Overview)":
                selected_listing_id = None
                st.info("📊 Showing market-wide calendar analysis")
            else:
                # Handle both string and integer cases
                if isinstance(selected_option, str):
                    selected_listing_id = int(selected_option.split(" - ")[0])
                    st.success(f"🏠 Analyzing calendar for: {selected_option}")
                else:
                    # If selected_option is already an integer (listing ID)
                    selected_listing_id = selected_option
                    st.success(f"🏠 Analyzing calendar for listing {selected_option}")
            
            # Create listing-specific calendar analysis
            if selected_listing_id is not None:
                # Load full calendar data for detailed analysis
                from utils.data_loader import load_full_calendar_data
                full_calendar_df = load_full_calendar_data()
                
                if full_calendar_df is not None:
                    # Filter calendar data for selected listing
                    listing_calendar = full_calendar_df[full_calendar_df['listing_id'] == selected_listing_id].copy()
                else:
                    # Fallback to sample data
                    listing_calendar = calendar_df[calendar_df['listing_id'] == selected_listing_id].copy()
                
                if not listing_calendar.empty:
                    # Get listing details
                    listing_details = listings_df[listings_df['id'] == selected_listing_id]
                    
                    if not listing_details.empty:
                        listing_detail = listing_details.iloc[0]
                        
                        # Display listing info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Listing ID", selected_listing_id)
                        with col2:
                            if 'neighbourhood' in listing_detail:
                                st.metric("Neighbourhood", listing_detail['neighbourhood'])
                            else:
                                st.metric("Neighbourhood", "N/A")
                        with col3:
                            if 'room_type' in listing_detail:
                                st.metric("Room Type", listing_detail['room_type'])
                            else:
                                st.metric("Room Type", "N/A")
                    
                    # Create listing-specific calendar visualizations
                    from analytics.analysis import create_calendar_events
                    
                    with st.spinner("Generating calendar events..."):
                        # Create calendar events for this listing only
                        listing_events = create_calendar_events(listing_calendar, selected_listing_id, max_events=500)
                    
                    if listing_events:
                        st.markdown("#### 📅 Listing Calendar")
                        
                        # Calendar configuration
                        calendar_options = {
                            "headerToolbar": {
                                "left": "prev,next today",
                                "center": "title",
                                "right": "dayGridMonth,timeGridWeek,timeGridDay"
                            },
                            "initialView": "dayGridMonth",
                            "height": 600,
                            "selectable": True,
                            "editable": False,
                            "eventDisplay": "block",
                            "eventColor": "#28a745"
                        }
                        
                        # Display calendar
                        calendar_result = calendar(
                            events=listing_events,
                            options=calendar_options,
                            key=f"listing_calendar_{selected_listing_id}"
                        )
                        
                        # Calendar statistics
                        available_days = sum(1 for event in listing_events if event.get('extendedProps', {}).get('available', False))
                        booked_days = sum(1 for event in listing_events if not event.get('extendedProps', {}).get('available', True))
                        avg_price = sum(event.get('extendedProps', {}).get('price', 0) or 0 for event in listing_events) / len(listing_events) if listing_events else 0
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Available Days", available_days)
                        
                        with col2:
                            st.metric("Booked Days", booked_days)
                        
                        with col3:
                            if avg_price > 0:
                                st.metric("Avg Price", f"${avg_price:.0f}")
                            else:
                                st.metric("Avg Price", "N/A")
                else:
                    st.warning(f"No calendar data found for listing {selected_listing_id}")
            
            # Calendar Analysis (Market Overview) - Only show if not viewing individual listing
            if selected_listing_id is None:
                st.markdown("### 📅 Market Calendar Analysis")
                st.markdown("*This shows the overall market calendar patterns across all listings.*")
                
                # Analyze city market for calendar data
                city_stats = analyze_city_market(listings_df, calendar_df)
                
                if city_stats and city_stats['calendar_analysis'] and 'basic_stats' in city_stats['calendar_analysis']:
                    # Basic calendar stats
                    basic_stats = city_stats['calendar_analysis']['basic_stats']
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Total Days", f"{basic_stats['total_days']:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Available Days", f"{basic_stats['available_days']:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Booked Days", f"{basic_stats['booked_days']:,}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Availability Rate", f"{basic_stats['availability_rate']:.1f}%")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Market calendar view
                st.markdown("#### 📅 Market Calendar")
                
                with st.spinner("Generating market calendar events..."):
                    # Load full calendar data for market overview
                    from utils.data_loader import load_full_calendar_data
                    full_calendar_df = load_full_calendar_data()
                    
                    if full_calendar_df is not None:
                        # Create market-wide calendar events on-demand
                        from analytics.analysis import create_calendar_events
                        market_events = create_calendar_events(full_calendar_df, None, max_events=1000)
                    else:
                        # Fallback to sample data
                        from analytics.analysis import create_calendar_events
                        market_events = create_calendar_events(calendar_df, None, max_events=1000)
                
                if market_events:
                    # Calendar configuration
                    calendar_options = {
                        "headerToolbar": {
                            "left": "prev,next today",
                            "center": "title",
                            "right": "dayGridMonth,timeGridWeek,timeGridDay"
                        },
                        "initialView": "dayGridMonth",
                        "height": 600,
                        "selectable": True,
                        "editable": False,
                        "eventDisplay": "block"
                    }
                    
                    # Display calendar
                    calendar_result = calendar(
                        events=market_events,
                        options=calendar_options,
                        key="market_calendar"
                    )
                    
                    # Calendar statistics
                    available_days = sum(1 for event in market_events if event.get('extendedProps', {}).get('available', False))
                    booked_days = sum(1 for event in market_events if not event.get('extendedProps', {}).get('available', True))
                    avg_price = sum(event.get('extendedProps', {}).get('price', 0) or 0 for event in market_events) / len(market_events) if market_events else 0
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Available Days", available_days)
                    
                    with col2:
                        st.metric("Booked Days", booked_days)
                    
                    with col3:
                        if avg_price > 0:
                            st.metric("Avg Price", f"${avg_price:.0f}")
                        else:
                            st.metric("Avg Price", "N/A")

def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 Airbnb Host Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d; margin-bottom: 2rem;">Analyze your booking data and city market insights</p>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.markdown("## 🧭 Navigation")
    
    # Main navigation options
    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        [
            "📊 Your Data Overview",
            "📈 Your Occupancy Analysis", 
            "💰 Your Revenue Analysis",
            "💵 Your Pricing Analysis",
            "🏙️ Copenhagen Market Insights",
            "📊 Copenhagen Market Occupancy",
            "📝 Copenhagen Review Patterns",
            "📅 Copenhagen Calendar Analysis"
        ],
        help="Select the type of analysis you want to perform"
    )
    
    # File upload section (always available)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📁 Upload Your Data")
    uploaded_files = st.sidebar.file_uploader(
        "Choose your Airbnb booking CSV files",
        type=['csv'],
        accept_multiple_files=True,
        help="Download your booking data from Airbnb and upload one or more CSV files here"
    )
    
    # Load data if files are uploaded
    df = None
    date_cols = []
    price_cols = []
    
    if uploaded_files:
        with st.spinner(f"Processing {len(uploaded_files)} file(s)..."):
            df, date_cols, price_cols = load_booking_data(uploaded_files)
        
        if df is not None and len(df) > 0:
            st.sidebar.success(f"✅ Loaded {len(df)} bookings")
        else:
            st.sidebar.error("❌ Failed to load data")
    
    # Load city data for market insights
    city_data_loaded = False
    listings_df = None
    calendar_df = None
    reviews_df = None
    
    if page in ["🏙️ Copenhagen Market Insights", "📊 Copenhagen Market Occupancy", "📝 Copenhagen Review Patterns", "📅 Copenhagen Calendar Analysis"]:
        with st.spinner("Loading Copenhagen market data..."):
            listings_df, calendar_df, reviews_df = load_city_data()
            city_data_loaded = listings_df is not None
    
    # Main content area based on selected page
    if page == "📊 Your Data Overview":
        render_data_analysis_page(df, uploaded_files, date_cols, price_cols)
    
    elif page == "📈 Your Occupancy Analysis":
        render_occupancy_analysis_page(df, date_cols, uploaded_files)
    
    elif page == "💰 Your Revenue Analysis":
        render_revenue_analysis_page(df, price_cols, uploaded_files)
    
    elif page == "💵 Your Pricing Analysis":
        render_pricing_analysis_page(df, date_cols, price_cols, uploaded_files)
    
    elif page == "🏙️ Copenhagen Market Insights":
        render_city_market_page(listings_df, calendar_df, city_data_loaded)
    
    elif page == "📊 Copenhagen Market Occupancy":
        render_copenhagen_occupancy_page(calendar_df, listings_df, city_data_loaded)
    
    elif page == "📝 Copenhagen Review Patterns":
        render_review_analysis_page(reviews_df, listings_df, city_data_loaded)
    
    elif page == "📅 Copenhagen Calendar Analysis":
        render_calendar_analysis_page(calendar_df, listings_df, city_data_loaded)

if __name__ == "__main__":
    main() 