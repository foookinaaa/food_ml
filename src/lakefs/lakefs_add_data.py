import pandas as pd

import lakefs
from lakefs.client import Client

df = pd.read_csv("../mlops_ods/dataset/2015-street-tree-census-tree-data.csv")
clt = Client(
    host="http://localhost:8000",
    username="AKIAJODO3YZ444RWVYRQ",
    password="LdOEm437fvEu6UlA0pxL3B7uVaePDv1pPQwtdcsc",
)
# repo = lakefs.Repository("mlops-example", client=clt) /
# .create(storage_namespace="s3://mlops-data-bucket/")
# branch1 = lakefs.repository("mlops-example") /
# .branch("experiment1").create(source_reference="main")
branch1 = lakefs.repository("mlops-example", client=clt).branch("experiment1")

obj = branch1.object(path="csv/raw_data.csv")

with obj.writer(mode="w", pre_sign=False, content_type="text/csv") as fd:
    df.to_csv(fd, index=False)
