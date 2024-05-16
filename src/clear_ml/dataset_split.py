import pandas as pd
from sklearn.model_selection import train_test_split

from mlops_ods.config import compose_config


def dataframe_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train, test = train_test_split(df, test_size=0.3, random_state=42)
    cfg = compose_config()
    num_cols = cfg.features.numerical
    return train[num_cols + ["health"]], test[num_cols + ["health"]]
