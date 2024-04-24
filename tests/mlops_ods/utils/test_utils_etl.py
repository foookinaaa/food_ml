import logging
from unittest.mock import patch

import dill
import pytest
from catboost import CatBoostClassifier

from mlops_ods.utils.utils_etl import (
    download_kaggle_dataset_if_not_exist,
    get_logger,
    load_model,
    save_model,
)

test_logger_name = "test_logger"
test_logger_level_num = logging.DEBUG
test_logger_format_name = (
    "%(asctime)s %(process)d %(processName)s "
    "%(name)-12s:%(lineno)d %(levelname)-8s %(message)s"
)


@pytest.fixture
def setup_logger():
    logger = get_logger(test_logger_name)
    yield logger
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)


def test_logger_created(setup_logger):
    assert setup_logger.name == test_logger_name


def test_logger_level(setup_logger):
    assert setup_logger.level == test_logger_level_num


def test_logger_format(setup_logger):
    handler = setup_logger.handlers[0]
    assert handler.formatter._fmt == test_logger_format_name


def test_load_model(tmp_path):
    # Create a temporary file to simulate the model file
    model_file = tmp_path / "model.pkl"
    with open(model_file, "wb") as f1:
        dill.dump("model_data", f1)

    model = load_model(str(model_file))

    assert model == "model_data"


def test_save_model(tmp_path):
    model = CatBoostClassifier()
    model_file = tmp_path / "model.pkl"

    save_model(str(model_file), model)

    with open(str(model_file), "rb") as f:
        saved_model = f.read()

    assert saved_model == dill.dumps(model)


@pytest.fixture
def mock_os_path_exists():
    with patch("os.path.exists") as mock_exists:
        yield mock_exists


@pytest.fixture
def mock_subprocess_run():
    with patch("subprocess.run") as mock_run:
        yield mock_run


def test_download_kaggle_dataset_if_not_exist_file_does_not_exist(
    mock_os_path_exists, mock_subprocess_run, capsys
):
    mock_os_path_exists.return_value = False
    download_kaggle_dataset_if_not_exist("/path/to/data", "dataset.zip")

    mock_subprocess_run.assert_called_once_with(
        [
            "kaggle",
            "datasets",
            "download",
            "-d",
            "new-york-city/ny-2015-street-tree-census-tree-data",
            "-p",
            "/path/to/data",
            "--unzip",
        ]
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == "Downloaded dataset.zip from Kaggle"


def test_download_kaggle_dataset_if_not_exist_file_exists(
    mock_os_path_exists, mock_subprocess_run, capsys
):
    mock_os_path_exists.return_value = True
    download_kaggle_dataset_if_not_exist("/path/to/data", "dataset.zip")

    mock_subprocess_run.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out.strip() == "dataset.zip already exists"


def test_download_kaggle_dataset_if_not_exist_error_downloading(
    mock_os_path_exists, mock_subprocess_run, capsys
):
    mock_os_path_exists.return_value = False
    mock_subprocess_run.side_effect = Exception("Some error occurred")
    download_kaggle_dataset_if_not_exist("/path/to/data", "dataset.zip")

    mock_subprocess_run.assert_called_once_with(
        [
            "kaggle",
            "datasets",
            "download",
            "-d",
            "new-york-city/ny-2015-street-tree-census-tree-data",
            "-p",
            "/path/to/data",
            "--unzip",
        ]
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == "Error downloading dataset.zip: Some error occurred"
