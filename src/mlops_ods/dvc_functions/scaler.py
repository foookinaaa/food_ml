import pickle
from pathlib import Path

import click
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from mlops_ods.config import compose_config

from .cli import cli


def train_scaler(df: pd.DataFrame) -> tuple[StandardScaler, pd.DataFrame, pd.DataFrame]:
    train, test = train_test_split(df, test_size=0.3, random_state=42)

    sc = StandardScaler()
    sc.fit(train)
    return sc, train, test


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("scaler_path", type=Path)
@click.argument("train_features_path", type=Path)
@click.argument("test_features_path", type=Path)
def cli_train_scaler(
    input_frame_path: Path,
    scaler_path: Path,
    train_features_path: Path,
    test_features_path: Path,
):
    cfg = compose_config()
    num_cols = cfg.features.numerical

    df = pd.read_csv(input_frame_path)
    scaler, train, test = train_scaler(df[num_cols])
    pickle.dump(scaler, scaler_path.open("wb"))
    train.to_csv(train_features_path, index=False)
    test.to_csv(test_features_path, index=False)
