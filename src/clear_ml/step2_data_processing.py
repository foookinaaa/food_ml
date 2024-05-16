import pandas as pd
from clearml import StorageManager, Task
from sklearn.model_selection import train_test_split

from mlops_ods.config import compose_config
from mlops_ods.utils.utils_model import drop_columns, preprocess_data

task = Task.init(project_name="Mlops-test", task_name="Pipeline step 2 process dataset")

# program arguments
# Use either dataset_task_id to point to a tasks artifact or
# use a direct url with dataset_url
args = {
    "dataset_task_id": "",
    "dataset_url": "",
    "random_state": 42,
    "test_size": 0.2,
}

# store arguments, later we will be able to change them from outside the code
task.connect(args)
print("Arguments: {}".format(args))

# only create the task, we will actually execute it later
task.execute_remotely()

# get dataset from task's artifact
if args["dataset_task_id"]:
    dataset_upload_task = Task.get_task(task_id=args["dataset_task_id"])
    print(
        "Input task id={} artifacts {}".format(
            args["dataset_task_id"], list(dataset_upload_task.artifacts.keys())
        )
    )
    # download the artifact
    data = dataset_upload_task.artifacts["dataset"].get_local_copy()
# get the dataset from a direct url
elif args["dataset_url"]:
    data = StorageManager.get_local_copy(remote_url=args["dataset_url"])
else:
    raise ValueError("Missing dataset link")

# open the local copy
df = pd.read_csv(data)

# "process" data
cfg = compose_config()
num_cols = cfg.features.numerical
cat_cols = cfg.features.categorical
df = df[~df["health"].isna()]
drop_columns(df)
preprocess_data(df)
y = df["health"]
X = df[num_cols + cat_cols]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=args["test_size"], random_state=args["random_state"]
)
# upload processed data
print("Uploading process dataset")
task.upload_artifact("X_train", X_train)
task.upload_artifact("X_test", X_test)
task.upload_artifact("y_train", y_train)
task.upload_artifact("y_test", y_test)

print("Notice, artifacts are uploaded in the background")
print("Done")
