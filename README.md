# Airbnb Data Analysis Project

This project analyzes Airbnb data including listings, reviews, calendar, and neighbourhood information.

## 📁 Project Structure

```
AirBnbAnalyzer/
├── requirements.txt          # Python dependencies
├── setup.py                 # Setup script
├── airbnb_analysis.ipynb    # Main analysis notebook
├── README.md               # This file
├── data/                   # Data directory (created automatically)
├── listings.csv.gz         # Property listings
├── reviews.csv.gz          # Guest reviews
├── calendar.csv.gz         # Availability data
├── neighbourhoods.csv      # Neighbourhood info
└── neighbourhoods.geojson  # Geographic boundaries
```

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python setup.py
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment (optional but recommended)
python -m venv airbnb_env
source airbnb_env/bin/activate  # On Windows: airbnb_env\Scripts\activate

# 2. Install requirements
pip install -r requirements.txt

# 3. Start Jupyter
jupyter notebook
```

## 📦 Required Packages

The `requirements.txt` includes:

### Core Analysis
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** - Basic plotting
- **seaborn** - Statistical visualizations
- **plotly** - Interactive visualizations

### Geographic Analysis
- **geopandas** - Geographic data handling
- **folium** - Interactive maps

### Text Analysis
- **nltk** - Natural language processing
- **textblob** - Sentiment analysis

### Machine Learning
- **scikit-learn** - Machine learning algorithms
- **xgboost** - Gradient boosting
- **lightgbm** - Light gradient boosting

## 🎯 Usage

1. **Start Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

2. **Open the analysis notebook:**
   - Open `airbnb_analysis.ipynb`
   - Run cells sequentially

3. **Follow the analysis:**
   - Data loading and exploration
   - Quality assessment
   - Statistical analysis
   - Visualizations

## 📊 Analysis Features

- **Data Loading:** Handles compressed (.gz) and uncompressed files
- **Quality Assessment:** Missing values, duplicates, data types
- **Statistical Analysis:** Descriptive statistics, correlations
- **Visualizations:** Charts, maps, interactive plots
- **Geographic Analysis:** Location-based insights
- **Text Analysis:** Review sentiment analysis

## 🔧 Troubleshooting

### Common Issues:

1. **Package Installation Errors:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

2. **Jupyter Kernel Issues:**
   ```bash
   python -m ipykernel install --user --name=airbnb_analysis
   ```

3. **Memory Issues with Large Files:**
   - Use sampling: `sample_size=10000` in load_csv_data()
   - Process files in chunks

4. **Geographic Package Issues:**
   ```bash
   # On Windows, you might need:
   conda install -c conda-forge geopandas
   ```

## 📈 Next Steps

After running the initial analysis:

1. **Data Cleaning:** Handle missing values and outliers
2. **Feature Engineering:** Create new variables
3. **Advanced Analysis:** Machine learning models
4. **Visualization:** Interactive dashboards
5. **Insights:** Generate business recommendations

## 🤝 Contributing

Feel free to extend the analysis with:
- Additional visualizations
- Machine learning models
- Geographic analysis
- Time series analysis
- Sentiment analysis

## 📝 License

This project is for educational and analysis purposes. 