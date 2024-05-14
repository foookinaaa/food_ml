# Clear ML research
```commandline
docker compose --project-directory src/clearml/. up
```
http://localhost:8080
settings -> workspace -> create credentials
```commandline
clearml-init
clearml-data create --project "Mlops-test" --name "Raw data"
clearml-data add --files src/mlops_ods/dataset/2015-street-tree-census-tree-data.csv
clearml-data upload
clearml-data close

export PYTHONPATH='src'
python src/clear_ml

poetry add clearml-agent
nano ~/clearml.conf
clearml-agent daemon --detached --queue default
```
