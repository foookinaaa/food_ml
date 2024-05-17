# Hypothesis report
Initial function for preprocess dataframe:
```python
import numpy as np
import pandas as pd
from mlops_ods.utils.utils_model import yes_no_to_numeric

def preprocess_data(df: pd.DataFrame) -> None:
    """
    Preprocess some columns - change df inplace

    :param df: original dataframe from kaggle
    :return:
    """
    columns_yes_no = [
        "root_stone",
        "root_grate",
        "root_other",
        "trunk_wire",
        "trnk_light",
        "trnk_other",
        "brch_light",
        "brch_shoe",
        "brch_other",
    ]
    for col in columns_yes_no:
        df[col] = yes_no_to_numeric(df[col])

    df["curb_loc"] = (df["curb_loc"] == "OnCurb") * 1
    df["sidewalk"] = np.where(df["sidewalk"] == "Damage", 1, 0)
    df["steward"] = (
        df["steward"].map({"1or2": 1, "3or4": 2, "4orMore": 3}).fillna(0).astype(int)
    )
    df["guards"] = (
        df["guards"]
        .map({"Harmful": 1, "Unsure": 2, "Helpful": 3})
        .fillna(0)
        .astype(int)
    )
    df["spc_common"] = df["spc_common"].fillna("n/d")
    df["problems"] = df["problems"].fillna("").apply(lambda x: len(x.split(",")))
    df["health"] = df["health"].map({"Poor": 0, "Fair": 1, "Good": 2}).astype(int)
```
Function working values and results:
```
input: pandas DataFrame with columns:
  "root_stone": "Yes", "No", Nan
  "root_grate": "Yes", "No", Nan
  "root_other": "Yes", "No", Nan
  "curb_loc": Any text, Nan
  "sidewalk": Any text, Nan
  "steward": Any text, Nan
  "guards": Any text, Nan
  "spc_common": Any text, Nan
  "problems": Any text, Nan
  "user_type": Any text, Nan
  "health": Any text, Nan
  "trunk_wire": Boolean (0,1)
  "trnk_light": Boolean (0,1)
  "trnk_other": Boolean (0,1)
  "brch_light": Boolean (0,1)
  "brch_shoe": Boolean (0,1)
  "brch_other": Boolean (0,1)

output: preprocessed pandas DataFrame
  "root_stone": "Yes", "No", Nan
  "root_grate": "Yes", "No", Nan
  "root_other": "Yes", "No", Nan
  "curb_loc": Any text, Nan
  "sidewalk": Any text, Nan
  "steward": Any text, Nan
  "guards": Any text, Nan
  "spc_common": Any text, Nan
  "problems": Any text, Nan
  "user_type": Any text, Nan
  "health": Any text, Nan
  "trunk_wire": Boolean (0,1)
  "trnk_light": Boolean (0,1)
  "trnk_other": Boolean (0,1)
  "brch_light": Boolean (0,1)
  "brch_shoe": Boolean (0,1)
  "brch_other": Boolean (0,1)
```





Hypothesis test on this function:
```python
from hypothesis import given
from hypothesis.extra.pandas import data_frames , column, range_indexes
import hypothesis.strategies as st
from mlops_ods.utils.utils_model import preprocess_data

df_columns = {
    "root_stone": {"elements": st.one_of(st.sampled_from(["Yes", "No"]), st.none()), "unique": False},
    "root_grate": {"elements": st.one_of(st.sampled_from(["Yes", "No"]), st.none()), "unique": False},
    "root_other": {"elements": st.one_of(st.sampled_from(["Yes", "No"]), st.none()), "unique": False},
    "curb_loc": {"elements": st.text(), "unique": False},
    "sidewalk": {"elements": st.text(), "unique": False},
    "steward": {"elements": st.text(), "unique": False},
    "guards": {"elements": st.text(), "unique": False},
    "spc_common": {"elements": st.text(), "unique": False},
    "problems": {"elements": st.text(), "unique": False},
    "user_type": {"elements": st.text(), "unique": False},
    "health": {"elements": st.text(), "unique": False},
    "trunk_wire": {"elements": st.booleans(), "unique": False},
    "trnk_light": {"elements": st.booleans(), "unique": False},
    "trnk_other": {"elements": st.booleans(), "unique": False},
    "brch_light": {"elements": st.booleans(), "unique": False},
    "brch_shoe": {"elements": st.booleans(), "unique": False},
    "brch_other": {"elements": st.booleans(), "unique": False},
}
test_dfs = data_frames(
    index=range_indexes(min_size=5),
    columns=[column(key, **value) for key, value in df_columns.items()],
)


@given(data=test_dfs)
def test_preprocess_data_hyp(data):
    preprocess_data(data)

    for col in [
        "root_stone", "root_grate", "root_other",
        "trunk_wire", "trnk_light", "trnk_other",
        "brch_light", "brch_shoe", "brch_other"
    ]:
        assert data[col].isin([0, 1]).all()
        assert data["curb_loc"].isin([0, 1]).all()
        assert data["sidewalk"].isin([0, 1]).all()
        assert data["steward"].isin([0, 1, 2, 3]).all()
        assert data["guards"].isin([0, 1, 2, 3]).all()
        assert data["spc_common"].notna().all()
        assert data["problems"].apply(lambda x: isinstance(x, int)).all()
        assert data["health"].isin([0, 1, 2]).all()
```
Error:
```
df["health"] = df["health"].map({"Poor": 0, "Fair": 1, "Good": 2}).astype(int)
values = array([nan, nan, nan, nan, nan]), dtype = dtype('int64'), copy = True
def _astype_float_to_int_nansafe(
    values: np.ndarray, dtype: np.dtype, copy: bool
) -> np.ndarray:
    """
    astype with a check preventing converting NaN to an meaningless integer value.
    """
    if not np.isfinite(values).all():
        raise IntCastingNaNError(
            "Cannot convert non-finite values (NA or inf) to integer"
        )
pandas.errors.IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer
```
If put all nan values that it cannot do astype(int) and it needs to be fixed:
* add "fillna(-1)" in function
* add "-1" to test function
```python
df["health"] = df["health"].map({"Poor": 0, "Fair": 1, "Good": 2}).fillna(-1).astype(int)

assert data["health"].isin([0, 1, 2, -1]).all()
```
