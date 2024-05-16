import pandas as pd
from clearml import Dataset, Task

# create an dataset experiment
task = Task.init(
    project_name="Mlops-test", task_name="Pipeline step 1 dataset artifact"
)

# only create the task, we will actually execute it later
task.execute_remotely()

frame_path = Dataset.get(
    dataset_name="Raw data", dataset_project="Mlops-test"
).get_local_copy()
data = pd.read_csv(frame_path + "/2015-street-tree-census-tree-data.csv")

# add and upload local file containing our toy dataset
task.upload_artifact("dataset", artifact_object=data)

print("uploading artifacts in the background")

# we are done
print("Done")
