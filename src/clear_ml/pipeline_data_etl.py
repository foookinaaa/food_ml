from clearml import PipelineController


def step_one():
    import pandas as pd  # noqa
    from clearml import Dataset

    frame_path = Dataset.get(
        dataset_name="Raw data", dataset_project="Mlops-test"
    ).get_local_copy()
    data = pd.read_csv(frame_path + "/2015-street-tree-census-tree-data.csv")
    return data


def step_two(df, test_size=0.3, random_state=42):
    import pandas as pd  # noqa
    from sklearn.model_selection import train_test_split

    from mlops_ods.config import compose_config
    from mlops_ods.utils.utils_model import drop_columns, preprocess_data

    cfg = compose_config()
    num_cols = cfg.features.numerical
    cat_cols = cfg.features.categorical
    df = df[~df["health"].isna()]
    drop_columns(df)
    preprocess_data(df)
    y = df["health"]
    X = df[num_cols + cat_cols]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    pipe = PipelineController(
        project="Mlops-test",
        name="Pipeline data etl task",
        version="1.1",
        add_pipeline_tags=False,
    )
    pipe.set_default_execution_queue("default")

    pipe.add_step(
        name="stage_data",
        base_task_project="Mlops-test",
        base_task_name="Pipeline step 1 dataset artifact",
    )
    pipe.add_step(
        name="stage_process",
        parents=["stage_data"],
        base_task_project="Mlops-test",
        base_task_name="Pipeline step 2 process dataset",
    )

    # Use run_pipeline_steps_locally=True
    # pipe.start_locally(run_pipeline_steps_locally=True)
    pipe.start()

    print("pipeline completed")
