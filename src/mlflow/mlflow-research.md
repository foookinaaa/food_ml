# MLFlow research
```commandline
mlflow server --host 127.0.0.1 --port 8080
```
### log_reg vs catboost for classification task
(probability of trees to be alive, normal or dead)
![mlops_exp](./experiments_info.png)
Comparison of metrics:
![mlops_metrics1](./metrics1.png)
![mlops_metrics2](./metrics2.png)
![mlops_metrics3](./metrics3.png)
Catboost predicts better classes 0 and 1, so it's better to choose this model for usage
