# 🏠 Airbnb Host Dashboard

> **Analyze your Airbnb booking data and Copenhagen market insights with advanced analytics**

## 🎯 The Problem

Airbnb hosts struggle to understand their own performance data and market positioning:

- **Data Overload**: Raw CSV exports from Airbnb are difficult to analyze and interpret
- **Missing Insights**: No clear view of occupancy patterns, revenue trends, or pricing performance
- **Market Blindness**: No way to compare performance against local market data
- **Manual Analysis**: Time-consuming spreadsheet work to understand booking patterns
- **Limited Visualization**: No easy way to see trends and patterns in booking data
- **Performance Blindness**: Difficulty identifying peak periods, pricing opportunities, and revenue optimization

Hosts need a simple, visual way to understand their booking data, compare with market data, and make data-driven decisions.

## 💡 The Solution

**Airbnb Host Dashboard** is a comprehensive analytics tool that transforms your Airbnb booking CSV exports into actionable insights and provides Copenhagen market intelligence:

### 🎯 Core Capabilities

#### **📊 Your Personal Data Analysis**
- **📈 Occupancy Analysis**: Visualize your booking patterns, peak periods, and day-of-week trends
- **💰 Revenue Tracking**: Track your total revenue, average revenue per booking, and monthly trends
- **💵 Pricing Analysis**: Understand your price distribution, trends, and optimization opportunities
- **📊 Performance Metrics**: Key metrics and insights to improve your hosting business

#### **🏙️ Copenhagen Market Intelligence**
- **🏙️ Market Insights**: Comprehensive Copenhagen market statistics and competitive analysis
- **📝 Review Patterns**: Analyze when guests typically leave reviews (day-of-week patterns)
- **📅 Calendar Analysis**: Interactive calendar views for individual listings and market-wide availability
- **🏘️ Neighbourhood Analysis**: Compare performance across different Copenhagen neighbourhoods
- **🏠 Room Type Analysis**: Understand pricing and demand by room type

### 🚀 Key Features

- **🧭 Smart Navigation**: Clean sidebar navigation separating personal data from market insights
- **📁 Simple Upload**: Just upload your Airbnb CSV export and get instant insights
- **🔍 Automatic Detection**: Automatically detects date and price columns from your data
- **📊 Visual Analytics**: Beautiful interactive charts and graphs to understand performance
- **📈 Review Analysis**: Understand guest review patterns and timing
- **📅 Interactive Calendars**: Visualize availability and booking patterns
- **🏙️ Market Comparison**: Compare your performance with Copenhagen market data
- **🎯 Data-Driven Decisions**: Make informed decisions based on your actual booking data

## 🎮 Demo & Getting Started

### Live Demo
Experience the Airbnb Host Dashboard in action:

🌐 **Live Demo**: [https://airbnbanalyzer-mrb2fmhxynr6mqynwvrdvu.streamlit.app/](https://airbnbanalyzer-mrb2fmhxynr6mqynwvrdvu.streamlit.app/)

Or run locally:
```bash
# Run the Streamlit application
streamlit run airbnb_host_advisor.py
```

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AirBnbAnalyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   streamlit run airbnb_host_advisor.py
   ```

4. **Access the dashboard:**
   - Open your browser to `http://localhost:8501`
   - Explore the interactive analytics dashboard with sidebar navigation

### 📊 Dashboard Sections

#### **Your Personal Data Analysis**
- **📊 Your Data Overview**: Main overview and data preview of your uploaded bookings
- **📈 Your Occupancy Analysis**: Detailed booking patterns and occupancy trends
- **💰 Your Revenue Analysis**: Revenue tracking and monthly trends
- **💵 Your Pricing Analysis**: Pricing patterns and optimization insights

#### **Copenhagen Market Intelligence**
- **🏙️ Copenhagen Market Insights**: Market statistics, neighbourhood analysis, and room type insights
- **📝 Copenhagen Review Patterns**: Day-of-week review patterns with interactive charts
- **📅 Copenhagen Calendar Analysis**: Interactive calendar views for individual listings and market-wide availability

## 🛠️ Technical Stack

- **Frontend**: Streamlit for interactive web application
- **Data Processing**: Pandas, NumPy for data manipulation
- **Visualization**: Plotly for interactive charts and graphs
- **Calendar Integration**: Streamlit-calendar for interactive calendar views
- **Geographic Analysis**: Folium for interactive maps
- **Machine Learning**: Scikit-learn for predictive analytics

## 📁 Project Structure

```
AirBnbAnalyzer/
├── airbnb_host_advisor.py      # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                   # This file
├── analytics/
│   ├── __init__.py
│   └── analysis.py             # Analytics functions
├── components/
│   ├── __init__.py
│   └── ui.py                   # UI components and styling
├── utils/
│   ├── __init__.py
│   └── data_loader.py          # Data loading utilities
├── data/                       # Data directory
├── listings.csv.gz             # Property listings
├── reviews.csv.gz              # Guest reviews
├── calendar.csv.gz             # Availability data
├── neighbourhoods.csv          # Neighbourhood info
└── neighbourhoods.geojson      # Geographic boundaries
```

## 🎯 Use Cases

### For Individual Hosts
- Analyze your own booking performance and trends
- Understand peak booking periods and pricing opportunities
- Track revenue and occupancy patterns over time
- Compare your performance with Copenhagen market data
- Understand guest review patterns and timing

### For Property Managers
- Monitor multiple properties' performance
- Identify revenue optimization opportunities
- Track pricing effectiveness across different properties
- Market analysis for competitive positioning

### For New Hosts
- Understand your initial performance data
- Identify patterns in your early bookings
- Optimize pricing based on your actual data
- Learn from Copenhagen market insights

## 🚀 Roadmap

- [ ] **Machine Learning Integration**: Predictive pricing models
- [ ] **Real-time Data**: Live market data integration
- [ ] **Multi-city Support**: Expand beyond Copenhagen
- [ ] **Advanced Analytics**: Deep learning for pattern recognition
- [ ] **API Integration**: Connect with Airbnb API for real-time data
- [ ] **Export Features**: PDF/Excel report generation
- [ ] **Mobile Optimization**: Better mobile experience

## 🤝 Contributing

We welcome contributions! Areas of interest:

- **New Analytics Features**: Additional insights and visualizations
- **UI/UX Improvements**: Enhanced user experience
- **Data Integration**: Support for additional data sources
- **Performance Optimization**: Faster data processing and analysis
- **Market Expansion**: Support for additional cities and markets

## 📝 License

This project is for educational and analysis purposes. The Airbnb Host Dashboard demonstrates advanced data analytics capabilities for the hospitality industry.

---

**Ready to optimize your Airbnb performance and understand market dynamics?** 🚀

[Get Started](#demo--getting-started) | [View Demo](#live-demo) | [Learn More](#the-solution) 