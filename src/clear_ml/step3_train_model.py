import joblib
from catboost import CatBoostClassifier
from clearml import Task
from sklearn.metrics import classification_report

from mlops_ods.config import compose_config

task = Task.init(project_name="Mlops-test", task_name="Pipeline step 3 train model")

# Arguments
args = {
    "dataset_task_id": "1127dc51d21e440a8e962266372d692e",
}
task.connect(args)

# only create the task, we will actually execute it later
task.execute_remotely()

print("Retrieving dataset")
dataset_task = Task.get_task(task_id=args["dataset_task_id"])
X_train = dataset_task.artifacts["X_train"].get()
X_test = dataset_task.artifacts["X_test"].get()
y_train = dataset_task.artifacts["y_train"].get()
y_test = dataset_task.artifacts["y_test"].get()
print("Dataset loaded")

cfg = compose_config()
cat_cols = cfg.features.categorical
model_params = {
    "iterations": cfg.model.iterations,
    "verbose": cfg.model.verbose,
    "random_seed": cfg.model.random_seed,
    "cat_features": cat_cols,
}
model = CatBoostClassifier(**model_params)
model.fit(X_train, y_train)

joblib.dump(model, "models/model.pkl", compress=True)

loaded_model = joblib.load("models/model.pkl")
predicts = loaded_model.predict(X_test)
result = classification_report(y_test.to_numpy(), predicts, output_dict=True)

print("Done")
