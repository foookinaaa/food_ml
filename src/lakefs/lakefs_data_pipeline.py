import pandas as pd
import yaml
from sklearn.preprocessing import LabelEncoder

import lakefs
from lakefs.client import Client
from mlops_ods.utils.utils_model import drop_columns, preprocess_data


def main():
    # setup
    with open(".lakectl.yaml", "r") as yaml_file:
        creds = yaml.safe_load(yaml_file)
    access_key_id = creds["credentials"]["access_key_id"]
    secret_access_key = creds["credentials"]["secret_access_key"]

    clt = Client(
        host="http://localhost:8000",
        username=access_key_id,
        password=secret_access_key,
    )
    try:
        repo = lakefs.Repository("mlops-example", client=clt).create(
            storage_namespace="s3://example/"
        )
        branch1 = (
            lakefs.repository("mlops-example")
            .branch("experiment1")
            .create(source_reference="main")
        )
    except:  # noqa: E722
        repo = lakefs.Repository("mlops-example", client=clt)
        branch1 = lakefs.repository("mlops-example", client=clt).branch("experiment1")
    main_br = repo.branch("main")

    # read
    df = pd.read_csv("../mlops_ods/dataset/2015-street-tree-census-tree-data.csv")
    obj = branch1.object(path="csv/raw_data.csv")
    with obj.writer(mode="w", pre_sign=False, content_type="text/csv") as fd:
        df.to_csv(fd, index=False)

    # preprocess
    obj = branch1.object(path="csv/raw_data.csv")
    with obj.reader(mode="r", pre_sign=False) as rd:
        df = pd.read_csv(rd)
    df = df[~df["health"].isna()]
    drop_columns(df)
    preprocess_data(df)
    # change preprocess here
    le = LabelEncoder()
    df["borough"] = le.fit_transform(df["borough"])
    #
    obj = branch1.object(path="csv/preprocess_data.csv")
    with obj.writer(mode="w", pre_sign=False, content_type="text/csv") as fd:
        df.to_csv(fd, index=False)

    branch1.commit(message="Add raw data", metadata={"using": "python_sdk"})
    branch1.merge_into(main_br)


if __name__ == "__main__":
    main()
