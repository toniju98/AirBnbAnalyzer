#!/usr/bin/env python3
"""
Analytics functions for Airbnb Host Dashboard
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import clean_price_data
import calendar


def analyze_occupancy(df, date_cols):
    """Analyze occupancy patterns"""
    if not date_cols:
        return None
    
    # Use the first date column found
    date_col = date_cols[0]
    
    # Create date range analysis
    df['date'] = pd.to_datetime(df[date_col])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_of_week'] = df['date'].dt.day_name()

    # Calculate occupancy metrics
    total_bookings = len(df)
    unique_dates = df['date'].nunique()

    # Monthly occupancy
    monthly_occupancy = df.groupby(['year', 'month']).size().reset_index(name='bookings')
    monthly_occupancy['date'] = pd.to_datetime(monthly_occupancy[['year', 'month']].assign(day=1))

    # Day of week occupancy
    dow_occupancy = df['day_of_week'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])

    return {
        'total_bookings': total_bookings,
        'unique_dates': unique_dates,
        'monthly_occupancy': monthly_occupancy,
        'dow_occupancy': dow_occupancy
    }

def analyze_revenue(df, price_cols):
    """Analyze revenue patterns"""
    if not price_cols:
        return None
    
    # Use the first price column found
    price_col = price_cols[0]
    
    # Calculate revenue metrics
    total_revenue = df[price_col].sum()
    avg_revenue_per_booking = df[price_col].mean()
    revenue_by_month = df.groupby([df['date'].dt.year, df['date'].dt.month])[price_col].sum().reset_index()
    revenue_by_month['date'] = pd.to_datetime(revenue_by_month[['year', 'month']].assign(day=1))
    
    return {
        'total_revenue': total_revenue,
        'avg_revenue_per_booking': avg_revenue_per_booking,
        'revenue_by_month': revenue_by_month
    }

def analyze_pricing(df, price_cols, date_cols):
    """Analyze pricing trends"""
    if not price_cols or not date_cols:
        return None
    
    price_col = price_cols[0]
    date_col = date_cols[0]
    
    # Calculate pricing metrics
    avg_price = df[price_col].mean()
    median_price = df[price_col].median()
    price_trend = df.groupby([df['date'].dt.year, df['date'].dt.month])[price_col].mean().reset_index()
    price_trend['date'] = pd.to_datetime(price_trend[['year', 'month']].assign(day=1))
    
    return {
        'avg_price': avg_price,
        'median_price': median_price,
        'price_trend': price_trend
    }

def analyze_city_market(listings_df, calendar_df):
    """Analyze city market statistics with comprehensive calendar analysis"""
    if listings_df is None:
        return None
    
    # Clean price data
    price_cols = [col for col in listings_df.columns if 'price' in col.lower()]
    if price_cols:
        listings_df = clean_price_data(listings_df, price_cols[0])
    
    # Basic market stats
    total_listings = len(listings_df)
    neighbourhoods = listings_df['neighbourhood'].nunique() if 'neighbourhood' in listings_df.columns else 0
    room_types = listings_df['room_type'].nunique() if 'room_type' in listings_df.columns else 0
    
    # Price analysis
    price_stats = {}
    if price_cols and f'{price_cols[0]}_clean' in listings_df.columns:
        price_data = listings_df[f'{price_cols[0]}_clean'].dropna()
        if len(price_data) > 0:
            price_stats = {
                'avg_price': price_data.mean(),
                'median_price': price_data.median(),
                'min_price': price_data.min(),
                'max_price': price_data.max(),
                'price_distribution': price_data
            }
    
    # Neighbourhood analysis
    neighbourhood_stats = {}
    if 'neighbourhood' in listings_df.columns and price_cols:
        neighbourhood_stats = listings_df.groupby('neighbourhood').agg({
            'id': 'count',
            f'{price_cols[0]}_clean': ['mean', 'median', 'count']
        }).round(2)
        neighbourhood_stats.columns = ['listings', 'avg_price', 'median_price', 'price_count']
    
    # Room type analysis
    room_type_stats = {}
    if 'room_type' in listings_df.columns and price_cols:
        room_type_stats = listings_df.groupby('room_type').agg({
            'id': 'count',
            f'{price_cols[0]}_clean': ['mean', 'median', 'count']
        }).round(2)
        room_type_stats.columns = ['listings', 'avg_price', 'median_price', 'price_count']
    
    # Enhanced Calendar Analysis - Only basic stats for performance
    calendar_analysis = {}
    if calendar_df is not None and 'available' in calendar_df.columns:
        # Only do basic stats for performance - detailed analysis will be done on-demand
        total_days = len(calendar_df)
        available_days = (calendar_df['available'] == 't').sum()
        booked_days = (calendar_df['available'] == 'f').sum()
        availability_rate = (available_days / total_days) * 100 if total_days > 0 else 0
        occupancy_rate = (booked_days / total_days) * 100 if total_days > 0 else 0
        
        calendar_analysis = {
            'basic_stats': {
                'total_days': total_days,
                'available_days': available_days,
                'booked_days': booked_days,
                'availability_rate': availability_rate,
                'occupancy_rate': occupancy_rate
            },
            'metadata': {
                'unique_listings': calendar_df['listing_id'].nunique()
            }
        }
    
    return {
        'total_listings': total_listings,
        'neighbourhoods': neighbourhoods,
        'room_types': room_types,
        'price_stats': price_stats,
        'neighbourhood_stats': neighbourhood_stats,
        'room_type_stats': room_type_stats,
        'calendar_analysis': calendar_analysis
    }

def create_calendar_events(calendar_df, listing_id=None, max_events=1000):
    """
    Create calendar events for streamlit-calendar from calendar data
    
    Args:
        calendar_df: DataFrame with calendar data
        listing_id: Specific listing ID to filter (optional)
        max_events: Maximum number of events to return (for performance)
    
    Returns:
        list: List of calendar events for streamlit-calendar
    """
    if calendar_df is None or calendar_df.empty:
        return []
    
    # Filter by listing_id if provided
    if listing_id is not None:
        calendar_df = calendar_df[calendar_df['listing_id'] == listing_id].copy()
    
    # Limit the number of events for performance
    if len(calendar_df) > max_events:
        calendar_df = calendar_df.head(max_events)
    
    # Convert date column to datetime if not already
    if 'date' in calendar_df.columns:
        calendar_df['date'] = pd.to_datetime(calendar_df['date'])
    
    # Clean price data if price column exists - do this vectorized
    if 'price' in calendar_df.columns:
        calendar_df['price_clean'] = pd.to_numeric(
            calendar_df['price'].str.replace('$', '').str.replace(',', ''), 
            errors='coerce'
        )
    
    # Vectorized event creation for better performance
    events = []
    
    # Create availability masks
    available_mask = calendar_df['available'] == 't'
    
    # Create events using vectorized operations
    for idx, (_, row) in enumerate(calendar_df.iterrows()):
        if idx >= max_events:  # Safety check
            break
            
        # Determine event color based on availability
        if row['available'] == 't':
            color = "#28a745"  # Green for available
            price_display = row.get('price_clean', row.get('price', 'N/A'))
            title = f"Available - ${price_display}"
        else:
            color = "#dc3545"  # Red for booked
            price_display = row.get('price_clean', row.get('price', 'N/A'))
            title = f"Booked - ${price_display}"
        
        event = {
            "title": title,
            "start": row['date'].strftime('%Y-%m-%d'),
            "end": row['date'].strftime('%Y-%m-%d'),
            "color": color,
            "resourceId": str(row.get('listing_id', '')),
            "extendedProps": {
                "available": row['available'] == 't',
                "price": row.get('price_clean', row.get('price', None)),
                "minimum_nights": row.get('minimum_nights', None),
                "maximum_nights": row.get('maximum_nights', None)
            }
        }
        events.append(event)
    
    return events

def analyze_review_patterns(reviews_df):
    """Analyze review patterns by day of the week"""
    if reviews_df is None or reviews_df.empty:
        return None
    
    # Convert date column to datetime
    if 'date' in reviews_df.columns:
        reviews_df['date'] = pd.to_datetime(reviews_df['date'])
        reviews_df['day_of_week'] = reviews_df['date'].dt.day_name()
        
        # Count reviews by day of week
        reviews_by_day = reviews_df['day_of_week'].value_counts().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        # Calculate percentages
        total_reviews = len(reviews_df)
        reviews_by_day_pct = (reviews_by_day / total_reviews * 100).round(1)
        
        return {
            'reviews_by_day': reviews_by_day,
            'reviews_by_day_pct': reviews_by_day_pct,
            'total_reviews': total_reviews,
            'avg_reviews_per_day': total_reviews / 7
        }
    
    return None