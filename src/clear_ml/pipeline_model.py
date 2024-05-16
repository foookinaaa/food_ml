from clearml import PipelineController

if __name__ == "__main__":
    pipe = PipelineController(
        project="Mlops-test",
        name="Pipeline catboost long",
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
        parameter_override={
            "General/dataset_url": "${stage_data.artifacts.dataset.url}",
        },
    )
    pipe.add_step(
        name="stage_train",
        parents=["stage_process"],
        base_task_project="Mlops-test",
        base_task_name="Pipeline step 3 train model",
        parameter_override={"General/dataset_task_id": "${stage_process.id}"},
    )

    # Use run_pipeline_steps_locally=True
    pipe.start_locally(run_pipeline_steps_locally=True)
    # pipe.start()

    print("pipeline completed")
