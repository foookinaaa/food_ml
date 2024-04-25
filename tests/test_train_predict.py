from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mlops_ods.config import compose_config
from mlops_ods.train_predict import main


@pytest.fixture
def mock_download_kaggle_dataset_if_not_exist():
    with patch(
        "mlops_ods.utils.utils_etl.download_kaggle_dataset_if_not_exist"
    ) as mock_download:
        yield mock_download


@pytest.fixture
def mock_pd_read_csv():
    with patch("pandas.read_csv") as mock_read_csv:
        yield mock_read_csv


@pytest.fixture
def mock_drop_columns():
    with patch("mlops_ods.utils.utils_model.drop_columns") as mock_drop:
        yield mock_drop


@pytest.fixture
def mock_preprocess_data():
    with patch("mlops_ods.utils.utils_model.preprocess_data") as mock_preprocess:
        yield mock_preprocess


@pytest.fixture
def mock_CatBoostClassifier():
    with patch("catboost.CatBoostClassifier") as mock_catboost:
        yield mock_catboost


@pytest.fixture
def mock_save_model():
    with patch("mlops_ods.utils.utils_etl.save_model") as mock_save:
        yield mock_save


@pytest.fixture
def mock_load_model():
    with patch("mlops_ods.utils.utils_etl.load_model") as mock_load:
        yield mock_load


@pytest.fixture
def mock_roc_auc_score():
    with patch("sklearn.metrics.roc_auc_score") as mock_roc_auc:
        yield mock_roc_auc


def test_main_train(
    mock_download_kaggle_dataset_if_not_exist,
    mock_pd_read_csv,
    mock_drop_columns,
    mock_preprocess_data,
    mock_CatBoostClassifier,
    mock_save_model,
    mock_roc_auc_score,
):
    cfg = compose_config(overrides=["settings=train"])
    df_mock = pd.DataFrame(
        {
            "tree_dbh": [10],
            "curb_loc": ["OnCurb"],
            "steward": ["None"],
            "guards": ["Harmful"],
            "sidewalk": ["Damage"],
            "problems": [1],
            "root_stone": ["No"],
            "root_grate": ["No"],
            "root_other": ["No"],
            "trunk_wire": ["No"],
            "trnk_light": ["No"],
            "trnk_other": ["No"],
            "brch_light": ["No"],
            "brch_shoe": ["No"],
            "brch_other": ["No"],
            "spc_common": ["Maple"],
            "zip_city": ["New York"],
            "borough": ["Manhattan"],
            "user_type": ["TreesCount Staff"],
            "health": ["Fair"],
        }
    )
    mock_pd_read_csv.return_value = df_mock
    clf_mock = MagicMock()
    mock_CatBoostClassifier.return_value = clf_mock
    main(cfg)

    mock_save_model.assert_called_once()


def test_main_predict(
    mock_pd_read_csv,
    mock_drop_columns,
    mock_preprocess_data,
    mock_load_model,
):
    cfg = compose_config(overrides=["settings=predict"])
    df_mock = pd.DataFrame(
        {
            "tree_dbh": [10],
            "curb_loc": ["OnCurb"],
            "steward": ["None"],
            "guards": ["Harmful"],
            "sidewalk": ["Damage"],
            "problems": [1],
            "root_stone": ["No"],
            "root_grate": ["No"],
            "root_other": ["No"],
            "trunk_wire": ["No"],
            "trnk_light": ["No"],
            "trnk_other": ["No"],
            "brch_light": ["No"],
            "brch_shoe": ["No"],
            "brch_other": ["No"],
            "spc_common": ["Maple"],
            "zip_city": ["New York"],
            "borough": ["Manhattan"],
            "user_type": ["TreesCount Staff"],
            "health": ["Fair"],
        }
    )
    mock_pd_read_csv.return_value = df_mock
    clf_mock = MagicMock()
    mock_load_model.return_value = clf_mock
    main(cfg)

    clf_mock.predict_proba.assert_called_once()
