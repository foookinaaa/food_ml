import os

import catboost
import hydra
import pandas as pd
from omegaconf import DictConfig
from sklearn import metrics

import mlops_ods.utils.utils_etl as ut_etl
import mlops_ods.utils.utils_model as ut_models
from mlops_ods.utils import utils_etl

logger = utils_etl.get_logger(__name__)
logger.propagate = False


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    path_to_data = os.path.join(os.path.dirname(os.getcwd()), cfg.settings.path_to_data)
    path_to_model = os.path.join(
        os.path.dirname(os.getcwd()),
        cfg.settings.path_to_model,
        cfg.settings.model_name,
    )
    logger.info("Start job")
    file_name = cfg.settings.file_name
    ut_etl.download_kaggle_dataset_if_not_exist(path_to_data, file_name)

    df = pd.read_csv(f"{path_to_data}/{file_name}")
    df = df[~df["health"].isna()]

    logger.info("Preprocess data")
    ut_models.drop_columns(df)
    ut_models.preprocess_data(df)

    num_cols = cfg.features.numerical
    cat_cols = cfg.features.categorical
    total_cols = num_cols + cat_cols

    logger.info("Fit model")
    clf = catboost.CatBoostClassifier(
        iterations=100, verbose=False, random_seed=42, cat_features=cat_cols
    )
    clf.fit(df[total_cols], df["health"])
    predictions = clf.predict_proba(df[total_cols])
    roc_auc = metrics.roc_auc_score(df["health"], predictions, multi_class="ovr")
    logger.info("Roc auc score: %s", roc_auc)

    logger.info("Save model")
    ut_etl.save_model(model_path=path_to_model, model=clf)


if __name__ == "__main__":
    main()
