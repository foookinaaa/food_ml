import datetime as dt

import pandas as pd
from sklearn.model_selection import train_test_split


def main():
    df = pd.read_csv("../mlops_ods/dataset/2015-street-tree-census-tree-data.csv")
    df = df[~df["health"].isna()]
    drop_cols = [
        "block_id",
        "created_at",
        "status",
        "address",
        "latitude",
        "longitude",
        "x_sp",
        "y_sp",
        "bin",
        "bbl",
        "census tract",
        "state",
        "council district",
        "boro_ct",
        "nta",
        "st_senate",
        "st_assem",
        "cncldist",
        "postcode",
        "community board",
        "borocode",
        "stump_diam",
        "spc_latin",
        "nta_name",
    ]
    df.drop(drop_cols, axis=1, inplace=True)
    df["timestamp"] = dt.datetime(2024, 6, 28, tzinfo=dt.timezone.utc)
    _, test = train_test_split(
        df, random_state=42, stratify=df["health"], test_size=0.1
    )
    test.to_parquet("./feature_repo/data/tree_data.parquet", index=False)


if __name__ == "__main__":
    main()
