import pandas as pd
import numpy as np
from scipy.stats import zscore


def clean_data(df, drop_duplicates=True, outlier_column=None, outlier_method='iqr'):
    # Drop missing values
    df = df.dropna()

    # Drop duplicates
    if drop_duplicates:
        df = df.drop_duplicates()

    # Handle outliers
    if outlier_column:
        if outlier_method == 'iqr':
            Q1 = df[outlier_column].quantile(0.25)
            Q3 = df[outlier_column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[outlier_column] >= lower_bound) & (df[outlier_column] <= upper_bound)]
        elif outlier_method == 'zscore':
            df['zscore'] = zscore(df[outlier_column])
            df = df[df['zscore'].abs() <= 3]
            df = df.drop(columns=['zscore'])

    return df


def normalize_data(df, columns, method='minmax'):

    df_normalized = df.copy()
    for col in columns:
        if method == 'minmax':
            min_val = df[col].min()
            max_val = df[col].max()
            df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
        elif method == 'zscore':
            mean_val = df[col].mean()
            std_val = df[col].std()
            df_normalized[col] = (df[col] - mean_val) / std_val

    return df_normalized


def categorize_data(df, column, bins=None, labels=None, one_hot_encode=False):
    df_categorized = df.copy()

    if bins is not None:
        # Binning numerical data
        df_categorized[column + '_binned'] = pd.cut(df[column], bins=bins, labels=labels)

    if one_hot_encode:
        # One-hot encoding categorical data
        df_categorized = pd.get_dummies(df_categorized, columns=[column], prefix=column)

    return df_categorized
