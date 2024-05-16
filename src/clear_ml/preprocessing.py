import pandas as pd

from mlops_ods.utils.utils_model import drop_columns, preprocess_data


def dataframe_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    df = df[~df["health"].isna()]
    drop_columns(df)
    preprocess_data(df)
    return df
