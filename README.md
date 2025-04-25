# 🏨 Hotel Reservation Cancellation Prediction

## 📌 Project Overview

This end-to-end machine learning project focuses on predicting hotel reservation cancellations. By analyzing booking details and customer behavior, the goal is to identify potential cancellations in advance using classification algorithms. The project also implements **MLOps best practices** to ensure scalability, reproducibility, and ease of deployment.

---

## 📊 Dataset Details

The dataset contains information about hotel reservations, customer behavior, and booking attributes. It includes both categorical and numerical features. The **target variable** is:

> `is_canceled`: A binary classification label (1 if canceled, 0 otherwise)

### 🔢 Feature Categories

**Categorical Features:**
- `type_of_meal_plan`
- `required_car_parking_space`
- `room_type_reserved`
- `market_segment_type`
- `repeated_guest`

**Numerical Features:**
- `no_of_adults`
- `no_of_children`
- `no_of_weekend_nights`
- `no_of_week_nights`
- `lead_time`
- `arrival_year`
- `arrival_month`
- `arrival_date`
- `no_of_previous_cancellations`
- `no_of_previous_bookings_not_canceled`
- `avg_price_per_room`
- `no_of_special_requests`

---

## 🔍 Exploratory Data Analysis (EDA)

This section includes an in-depth analysis of booking trends, cancellation patterns, and feature correlations. Insights are derived from:
- Histograms of feature distributions
- Correlation matrix heatmaps
- Time-series cancellation patterns
- Average prices by segment

📎 _Visualizations will be added here soon._  
🖼️ ![EDA Placeholder](./eda_placeholder.png)

---

## 🤖 Model Comparison

The following models were trained and evaluated using Accuracy, Precision, Recall, and F1-score metrics:

| Model                    | Accuracy  | Precision | Recall    | F1 Score  |
|--------------------------|-----------|-----------|-----------|-----------|
| Random Forest            | 0.891679  | 0.892508  | 0.892508  | **0.892508** |
| Logistic Regression      | 0.774331  | 0.802787  | 0.731922  | 0.765718  |
| Gradient Boosting        | 0.837190  | 0.821473  | 0.864821  | 0.842590  |
| Support Vector Classifier| 0.720335  | 0.723657  | 0.706840  | 0.718068  |
| Decision Tree            | 0.840801  | 0.850000  | 0.830619  | 0.840198  |
| K-Nearest Neighbors (KNN)| 0.779419  | 0.856612  | 0.675244  | 0.755191  |
| Naive Bayes              | 0.773346  | 0.803232  | 0.728664  | 0.764133  |
| XGBoost                  | 0.870343  | 0.866324  | 0.878176  | 0.872210  |
| AdaBoost                 | 0.821927  | 0.814780  | 0.836608  | 0.825547  |
| LGBM                     | 0.866732  | 0.851494  | 0.890879  | 0.870742  |

📌 _**Random Forest** achieved the best performance with an F1-score of **0.892508**._

---

## ⚙️ MLOps Implementation

This project follows core MLOps practices:

- ✅ **Version Control**: Git is used for tracking code and data pipeline versions.
- ✅ **CI/CD Pipelines**: Automated pipelines handle data preprocessing, model training, and testing.
- ✅ **Monitoring & Logging**: Logs and metrics are tracked to monitor model performance in production.
- ✅ **Containerization**: The entire pipeline is containerized using **Docker** for reliable deployment.
- ✅ **API Deployment**: A lightweight **Flask API** is used to serve predictions, deployed via **AWS** or **Heroku**.

---

## 🗂️ Project Structure

\`\`\`bash
hotel-reservation-cancellation/
│
├── artifacts/               # Output directories for processed data and artifacts
│   ├── processed/
│   └── raw/
│
├── config/                  # Configuration files (YAML, JSON, etc.)
│
├── logs/                    # General logging directory
│
├── notebook/                # Jupyter Notebooks for EDA and experimentation
│
├── src/                     # Source code for the ML pipeline
│   ├── __pycache__/
│   ├── artifacts/           # Folder to handle output artifacts in scripts
│   ├── logs/                # Script-specific logging
│   ├── __init__.py
│   ├── custom_exception.py  # Custom error handling
│   ├── data_ingestion.py    # Raw data ingestion pipeline
│   ├── data_preprocessing.py# Data cleaning and feature engineering
│   ├── logger.py            # Logging utility
│   └── model_training.py    # Model training and evaluation script
│
├── static/                  # Static assets (if deploying with web UI)
│
├── templates/               # HTML templates for web UI
│
├── utils/                   # Utility functions and shared helpers
│
├── venv/                    # Virtual environment directory
│
├── .gitignore
├── requirements.txt         # Python dependencies
├── setup.py                 # Setup script for packaging
\`\`\`

---

## 🛠️ Installation & Usage

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/your-username/hotel-cancellation-prediction.git
   cd hotel-cancellation-prediction
   \`\`\`

2. **Create a virtual environment & install dependencies**
   \`\`\`bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   pip install -e .
   \`\`\`



## 🚀 Future Improvements

- 🧪 **Hyperparameter tuning** with GridSearchCV or Optuna
- 🛠️ **Advanced feature engineering** for time-based trends
- 📈 **Model explainability** with SHAP/LIME
- 🌐 **Deploy as a web dashboard** using Streamlit or Dash
- ⏱️ **Real-time monitoring** with Prometheus + Grafana

---

## 📚 References & Tools

- [scikit-learn](https://scikit-learn.org/)
- [XGBoost](https://xgboost.ai/)
- [LightGBM](https://lightgbm.readthedocs.io/)
- [Flask](https://flask.palletsprojects.com/)
- [Docker](https://www.docker.com/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib & Seaborn](https://seaborn.pydata.org/)

---

_**Author**: Daniel Alfonso Garcia Perez  
**Role**: Data Analyst / Data Scientist  
**Contact**: dgarciap@outlook.com - https://www.linkedin.com/in/danielext10/
