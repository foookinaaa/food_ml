import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

import mlflow
from mlops_ods.config import compose_config
from mlops_ods.dvc_functions.models import conf_matrix
from mlops_ods.utils.utils_model import drop_columns, preprocess_data


def main():
    path_to_data = "../mlops_ods/dataset/2015-street-tree-census-tree-data.csv"
    df = pd.read_csv(path_to_data)
    df = df[~df["health"].isna()]
    drop_columns(df)
    preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop("health", axis=1),
        df["health"],
        test_size=0.3,
        random_state=42,
        stratify=df["health"],
    )
    cfg = compose_config()
    num_cols = cfg.features.numerical
    cat_cols = cfg.features.categorical
    total_cols = num_cols + cat_cols

    mlflow.set_tracking_uri("http://127.0.0.1:8080")
    mlflow.set_experiment("mlops_test")
    cb_run_name = "catboost"

    with mlflow.start_run(run_name=cb_run_name) as run:  # noqa: F841
        model_params = {
            "random_state": 42,
            "iterations": 100,
            "verbose": False,
            "cat_features": cat_cols,
        }
        model_cb = CatBoostClassifier(**model_params)
        model_cb.fit(X_train[total_cols], y_train)
        predicts = model_cb.predict(X_test[total_cols])
        report = classification_report(y_test, predicts, output_dict=True)

        mlflow.log_metric("accuracy", report.pop("accuracy"))
        for class_or_avg, metrics_dict in report.items():
            if class_or_avg == "macro avg":
                break
            for metric, value in metrics_dict.items():
                mlflow.log_metric(class_or_avg + "_" + metric, value)

        mlflow.log_params(model_params)

        mlflow.catboost.log_model(
            cb_model=model_cb,
            input_example=X_test[total_cols][:10],
            artifact_path=f"mlflow/{cb_run_name}/model",
        )

        fig = conf_matrix(y_test, predicts)
        mlflow.log_figure(fig, f"{cb_run_name}_confusion_matrix.png")


if __name__ == "__main__":
    main()
