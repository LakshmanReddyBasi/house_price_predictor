import pandas as pd

def preprocess_input(df):
    # Replace missing values or dummy encoding
    # Ensure only columns used in training are present
    required_columns = ['LotArea', 'OverallCond', 'YearBuilt', 'YearRemodAdd', 'TotalBsmtSF']
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[required_columns]
    return df
