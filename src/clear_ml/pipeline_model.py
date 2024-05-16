from clearml import PipelineController

from clear_ml.pipeline_data_etl import step_one, step_two


def step_three(data):
    import pandas as pd  # noqa
    from catboost import CatBoostClassifier

    from mlops_ods.config import compose_config

    X_train, X_test, y_train, y_test = data
    cfg = compose_config()
    cat_cols = cfg.features.categorical
    model_params = {
        "iterations": 800,
        "verbose": cfg.model.verbose,
        "random_seed": cfg.model.random_seed,
        "cat_features": cat_cols,
    }
    model = CatBoostClassifier(**model_params)
    model.fit(X_train, y_train)
    return model


def step_four(data, model):
    import pandas as pd  # noqa
    from sklearn.metrics import classification_report

    X_train, X_test, y_train, y_test = data
    predicts = model.predict(X_test)
    return classification_report(y_test.to_numpy(), predicts, output_dict=True)


if __name__ == "__main__":
    pipe = PipelineController(
        project="Mlops-test",
        name="Pipeline catboost long",
        version="1.1",
        add_pipeline_tags=False,
    )
    pipe.set_default_execution_queue("default")
    pipe.add_function_step(
        name="step_one",
        function=step_one,
        function_return=["data_frame"],
        cache_executed_step=True,
    )
    pipe.add_function_step(
        name="step_two",
        # parents=['step_one'],
        function=step_two,
        function_kwargs=dict(df="${step_one.data_frame}"),
        function_return=["processed_data"],
        cache_executed_step=True,
    )

    pipe.add_function_step(
        name="step_three",
        # parents=['step_two'],
        function=step_three,
        function_kwargs=dict(data="${step_two.processed_data}"),
        function_return=["model"],
        cache_executed_step=True,
    )
    pipe.add_function_step(
        name="step_four",
        # parents=['step_three'],
        function=step_four,
        function_kwargs=dict(
            data="${step_two.processed_data}", model="${step_three.model}"
        ),
        function_return=["classification_report"],
        cache_executed_step=True,
    )

    # Use run_pipeline_steps_locally=True
    pipe.start_locally(run_pipeline_steps_locally=True)
    # pipe.start()

    print("pipeline completed")
