#!/usr/bin/env python3
"""
Data loading and cleaning utilities for Airbnb Host Dashboard
"""

import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

@st.cache_data
def load_booking_data(uploaded_files):
    """Load and process Airbnb booking data from multiple CSV files"""
    try:
        all_dfs = []
        all_date_columns = []
        all_price_columns = []
        
        for uploaded_file in uploaded_files:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Standardize column names
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            # Try to identify date columns
            date_columns = [col for col in df.columns if 'date' in col or 'check' in col or 'arrival' in col]
            
            if date_columns:
                # Convert date columns
                for col in date_columns:
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    except:
                        pass
            
            # Try to identify price/revenue columns
            price_columns = [col for col in df.columns if 'price' in col or 'revenue' in col or 'amount' in col or 'total' in col]
            
            if price_columns:
                # Clean price columns
                for col in price_columns:
                    try:
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
                    except:
                        pass
            
            all_dfs.append(df)
            all_date_columns.extend(date_columns)
            all_price_columns.extend(price_columns)
        
        # Combine all dataframes
        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            # Remove duplicates based on all columns
            combined_df = combined_df.drop_duplicates()
            return combined_df, list(set(all_date_columns)), list(set(all_price_columns))
        else:
            return None, [], []
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, [], []

@st.cache_data
def load_city_data():
    """Load Copenhagen city data for market insights"""
    try:
        # Load listings data
        if Path('listings.csv').exists():
            listings_df = pd.read_csv('listings.csv')
        elif Path('listings.csv.gz').exists():
            listings_df = pd.read_csv('listings.csv.gz', compression='gzip')
        else:
            return None, None, None
        
        # Clean listings data - remove completely NaN columns
        if listings_df is not None:
            # Remove columns that are completely NaN
            listings_df = listings_df.dropna(axis=1, how='all')
            
        
        # Load calendar data - only load a sample for initial stats
        if Path('calendar.csv.gz').exists():
            # Load only a sample for initial stats to improve performance
            calendar_df = pd.read_csv('calendar.csv.gz', compression='gzip', 
                                    usecols=['listing_id', 'date', 'available', 'price', 'minimum_nights', 'maximum_nights'],
                                    nrows=10000)  # Only load first 10k rows for initial stats
            # Clean calendar data
            if calendar_df is not None:
                calendar_df = calendar_df.dropna(axis=1, how='all')
                # Convert date column for better performance
                calendar_df['date'] = pd.to_datetime(calendar_df['date'])
        else:
            calendar_df = None
        
        
        # Load reviews data
        if Path('reviews.csv').exists():
            reviews_df = pd.read_csv('reviews.csv')
        elif Path('reviews.csv.gz').exists():
            reviews_df = pd.read_csv('reviews.csv.gz', compression='gzip')
        else:
            reviews_df = None
        
        return listings_df, calendar_df, reviews_df
    
    except Exception as e:
        st.error(f"Error loading city data: {e}")
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
def load_full_calendar_data():
    """Load the full calendar dataset for detailed analysis"""
    try:
        if Path('calendar.csv.gz').exists():
            calendar_df = pd.read_csv('calendar.csv.gz', compression='gzip', 
                                    usecols=['listing_id', 'date', 'available', 'price', 'minimum_nights', 'maximum_nights'])
            if calendar_df is not None:
                calendar_df = calendar_df.dropna(axis=1, how='all')
                calendar_df['date'] = pd.to_datetime(calendar_df['date'])
            return calendar_df
        else:
            return None
    except Exception as e:
        st.error(f"Error loading full calendar data: {e}")
        return None