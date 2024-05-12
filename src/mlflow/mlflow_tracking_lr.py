import pandas as pd
from sklearn.linear_model import LogisticRegression
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

    mlflow.set_tracking_uri("http://127.0.0.1:8080")
    # current name of experiment
    mlflow.set_experiment("mlops_test")
    # current name of run
    logreg_run_name = "logreg"

    with mlflow.start_run(run_name=logreg_run_name) as run:  # noqa: F841
        model_params = {
            "random_state": 42,
            "max_iter": 300,
            "C": 10,
        }
        model_lr = LogisticRegression(**model_params)
        model_lr.fit(X_train[num_cols], y_train)
        predicts = model_lr.predict(X_test[num_cols])
        report = classification_report(y_test, predicts, output_dict=True)

        # log metrics
        mlflow.log_metric("accuracy", report.pop("accuracy"))
        for class_or_avg, metrics_dict in report.items():
            if class_or_avg == "macro avg":
                break
            for metric, value in metrics_dict.items():
                mlflow.log_metric(class_or_avg + "_" + metric, value)

        # log model params
        mlflow.log_params(model_params)

        # log full model
        mlflow.sklearn.log_model(
            sk_model=model_lr,
            input_example=X_test[num_cols][:10],
            artifact_path=f"mlflow/{logreg_run_name}/model",
        )

        fig = conf_matrix(y_test, predicts)
        # log fig
        mlflow.log_figure(fig, f"{logreg_run_name}_confusion_matrix.png")


if __name__ == "__main__":
    main()
