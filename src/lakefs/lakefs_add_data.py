import pandas as pd

import lakefs
from lakefs.client import Client

df = pd.read_csv("../mlops_ods/dataset/2015-street-tree-census-tree-data.csv")
clt = Client(
    host="http://localhost:8000",
    username="AKIAJODO3YZ444RWVYRQ",
    password="LdOEm437fvEu6UlA0pxL3B7uVaePDv1pPQwtdcsc",
)
branch1 = lakefs.repository("mlops-example", client=clt).branch("experiment1")

with branch1.object(path="csv/raw_data.csv").upload(
    content_type="text/csv", data="raw data"
) as f:
    df.to_csv(f, index=False)
