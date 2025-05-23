# House Price Predictor

A machine learning application that predicts house prices based on various features like lot size, building type, year built, and more.

## Project Overview

This application uses machine learning algorithms to predict house prices based on a dataset of housing features. The model was trained in Google Colab and exported to local files for use in a Streamlit web application.

## Directory Structure

```
HOUSE_PRICE_PREDICTOR/
├── data/
│   └── HousePricePrediction.xlsx    # Dataset containing house features and prices
├── model/
│   ├── house_price_model.pkl        # Trained machine learning model
│   └── trained_columns.pkl          # Columns used during model training
├── notebooks/
│   └── model_training.ipynb         # Jupyter notebook used for model development
├── utils/
│   └── preprocessing.py             # Utility functions for data preprocessing
├── app.py                           # Main Streamlit application
├── README.md                        # Project documentation
└── requirements.txt                 # Required Python packages
```

## Dataset Information

The dataset (`HousePricePrediction.xlsx`) contains various features of houses along with their sale prices. Key features include:

- **Id**: Record identifier
- **MSSubClass**: Type of dwelling involved in the sale
- **MSZoning**: General zoning classification
- **LotArea**: Lot size in square feet
- **LotConfig**: Configuration of the lot
- **BldgType**: Type of dwelling
- **OverallCond**: Overall condition rating
- **YearBuilt**: Original construction year
- **YearRemodAdd**: Remodel date
- **Exterior1st**: Exterior covering on house
- **BsmtFinSF2**: Type 2 finished basement square feet
- **TotalBsmtSF**: Total square feet of basement area
- **SalePrice**: Sale price (target variable)

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository or download the project files
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

Launch the Streamlit app by running:
```
streamlit run app.py
```

The application will open in your default web browser.

## How to Use

1. The application presents a user-friendly interface for entering house features
2. Enter the required details for the house you want to price
3. Submit the form to get a price prediction
4. View the predicted house price along with additional information

## Model Information

The prediction model was developed in Google Colab using machine learning algorithms. The trained model and its required preprocessing components are stored in the `model/` directory:

- `house_price_model.pkl`: Serialized trained model
- `trained_columns.pkl`: Feature columns used during training

## Contributing

If you'd like to contribute to this project, please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Dataset source: [mention source if applicable]
- Contributors and maintainers