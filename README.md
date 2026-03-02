# Financial Fraud Detection System

A professional, production-ready web application for detecting financial fraud using Apache Spark, Machine Learning, and Streamlit.

## 🛡️ Features

### Core Features

- **📤 Upload Any CSV** - Upload your own transaction datasets for analysis
- **🔒 Authentication** - Secure Login & Signup system
- **📊 Dataset Overview** - View rows, columns, types, and data preview
- **🔍 Data Quality Report** - Analyze missing values, duplicates, and invalid data
- **📈 Statistical Summary** - Comprehensive statistics with visualizations
- **🛡️ Fraud Distribution** - Visual analysis of fraud vs legitimate transactions
- **📊 Risk Percentiles** - View risk scores at 90th, 95th, and 99th percentiles
- **📋 Rule-Based Detection** - Detect fraud using predefined rules
- **🌲 Isolation Forest** - ML-based anomaly detection
- **🤖 ML Results** - Train and evaluate Random Forest, Logistic Regression, and Gradient Boosting models
- **🔢 Confusion Matrix** - Visual confusion matrix with detailed metrics
- **📉 Precision-Recall** - Interactive precision-recall curves
- **📑 Download Reports** - Generate and download PDF, CSV, or TXT reports

### Technical Stack

- **Apache Spark (PySpark)** - Big data processing
- **Streamlit** - Web UI framework
- **scikit-learn** - Machine learning models
- **Plotly** - Interactive visualizations
- **ReportLab** - PDF report generation

## 📁 Project Structure

```
FINANCIAL_FRAUD_DETECTION/
├── backend/
│   ├── auth.py              # Authentication module
│   ├── api.py               # Backend API
│   └── report_generator.py # Report generation
├── spark/
│   ├── spark_session.py     # Spark session management
│   ├── preprocessing.py     # Data preprocessing
│   └── fraud_analysis.py   # Fraud analysis
├── ui/
│   ├── app.py               # Main Streamlit app
│   ├── dashboard.py         # Dashboard with navigation
│   ├── login.py             # Login page
│   ├── signup.py            # Signup page
│   ├── upload.py            # File upload
│   ├── statistics.py        # Statistics page
│   ├── report.py            # Report page
│   └── pages/
│       ├── dataset_overview.py
│       ├── data_quality.py
│       ├── fraud_analysis.py
│       ├── risk_percentiles.py
│       ├── rule_based.py
│       ├── isolation_forest.py
│       ├── ml_results.py
│       ├── confusion_matrix.py
│       └── precision_recall.py
├── data/
│   ├── creditcard.csv       # Sample dataset
│   ├── users.json           # User credentials
│   └── uploads/             # User uploads
├── reports/
│   └── generated/           # Generated reports
├── requirements.txt
└── README.md
```

## 🚀 Installation

1. **Clone or download the project**

2. **Install dependencies:**

```
bash
pip install -r requirements.txt
```

3. **Run the application:**

```
bash
streamlit run ui/dashboard.py
```

4. **Open in browser:**
   Navigate to `http://localhost:8501`

## 📖 Usage Guide

### Getting Started

1. **Sign Up** - Create an account with your email and password
2. **Login** - Use your credentials to access the portal
3. **Upload Data** - Upload any CSV file with transaction data (or use the sample data)
4. **Run Analysis** - Analyze your data using various detection methods

### Sample Dataset

The project includes a sample credit card fraud dataset at `data/creditcard.csv` with:

- 284,807 transactions
- 30 features (V1-V28 + Amount + Time)
- 492 fraudulent transactions (0.17%)

### Navigation

Use the sidebar to navigate between:

- **Dashboard** - Overview and quick stats
- **Upload** - Upload your dataset
- **Dataset Overview** - View data structure
- **Data Quality** - Check data quality
- **Statistics** - Detailed statistics
- **Fraud Distribution** - Fraud vs legitimate analysis
- **Risk Percentiles** - Risk score percentiles
- **Rule-Based** - Rule-based detection
- **Isolation Forest** - ML anomaly detection
- **ML Results** - Model training and evaluation
- **Confusion Matrix** - Model performance
- **Precision-Recall** - PR curves
- **Reports** - Generate and download reports

## 🔧 Configuration

### Spark Settings

You can adjust Spark configuration in `spark/spark_session.py`:

- Driver memory
- Executor memory
- Number of partitions

### Model Settings

Adjust ML model parameters in the UI sidebar:

- Contamination rate
- Number of estimators
- Max samples

## 📊 Data Format

The system works with any CSV file containing transaction data. For best results, include:

- `Amount` - Transaction amount
- `Time` - Transaction timestamp
- `Class` or `Fraud` - Label column (optional)

## 🤝 Contributing

This is a professional-grade fraud detection system. Feel free to extend it with:

- Additional ML models
- More detection rules
- Enhanced visualizations
- API endpoints

## 📝 License

This project is for educational and professional use.

## 🏆 Key Features

1. **Production-Ready** - Modular, well-commented code
2. **Professional UI** - Modern dark theme with glassmorphism
3. **No Demo Files** - Upload any CSV you want
4. **Full Analytics** - Complete analysis pipeline
5. **Downloadable Reports** - Professional PDF/CSV/TXT reports

---

Built with ❤️ using Apache Spark and Streamlit
