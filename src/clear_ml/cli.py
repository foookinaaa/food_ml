import click
import joblib
import pandas as pd
from clearml import Dataset, Task

from .dataset_split import dataframe_split
from .model import test, train
from .preprocessing import dataframe_preprocessing


@click.command()
@click.argument("random_state", type=int, default=42)
@click.argument("max_iter", type=int, default=300)
@click.argument("lr_const", type=float, default=10.0)
def cli_clearml(
    random_state: int,
    max_iter: int,
    lr_const: float,
):
    task = Task.init(project_name="Mlops-test", task_name="baseline", output_uri=True)
    frame_path = Dataset.get(
        dataset_name="Raw data", dataset_project="Mlops-test"
    ).get_local_copy()
    task.set_progress(0)
    data = pd.read_csv(frame_path + "/2015-street-tree-census-tree-data.csv")
    task.set_progress(10)
    processed_data = dataframe_preprocessing(data)
    task.set_progress(20)
    task.upload_artifact(name="processed_data", artifact_object=processed_data)

    train_data, test_data = dataframe_split(processed_data)
    train_result = train_data.drop("health", axis=1)
    test_result = test_data.drop("health", axis=1)
    task.set_progress(50)
    task.upload_artifact(
        name="train_features",
        artifact_object=(train_result, train_data["health"].to_numpy()),
    )
    task.upload_artifact(
        name="test_features",
        artifact_object=(test_result, test_data["health"].to_numpy()),
    )
    model = train(
        train_result,
        train_data["health"].to_numpy(),
        {
            "random_state": random_state,
            "max_iter": max_iter,
            "C": lr_const,
        },
    )
    joblib.dump(model, "src/clear_ml/models/model.pkl", compress=True)
    task.set_progress(80)
    result, confusion = test(model, test_result, test_data["health"].to_numpy())
    task.set_progress(90)
    logger = task.get_logger()
    logger.report_single_value("accuracy", result.pop("accuracy"))
    for class_name, metrics in result.items():
        for metric, value in metrics.items():
            logger.report_single_value(f"{class_name}_{metric}", value)
    logger.report_confusion_matrix("conflusion matrix", "ignored", matrix=confusion)
