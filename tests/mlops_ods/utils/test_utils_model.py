import hypothesis.strategies as st
import numpy as np
import pandas as pd
from hypothesis.extra.pandas import column, data_frames, range_indexes

from hypothesis import given
from mlops_ods.utils.utils_model import drop_columns, preprocess_data, yes_no_to_numeric


def test_yes_no_to_numeric():
    column = pd.Series(["Yes", "No", "Yes", "No", "Yes"])
    result = yes_no_to_numeric(column)

    assert result.equals(pd.Series([1, 0, 1, 0, 1]))


def test_yes_no_to_numeric_all_yes():
    column = pd.Series(["Yes", "Yes", "Yes", "Yes", "Yes"])
    result = yes_no_to_numeric(column)

    assert result.equals(pd.Series([1, 1, 1, 1, 1]))


def test_yes_no_to_numeric_all_no():
    column = pd.Series(["No", "No", "No", "No", "No"])
    result = yes_no_to_numeric(column)

    assert result.equals(pd.Series([0, 0, 0, 0, 0]))


def test_yes_no_to_numeric_empty_series():
    column = pd.Series([])
    result = yes_no_to_numeric(column)

    assert result.empty


def test_drop_columns():
    df = pd.DataFrame(
        {
            "block_id": [1, 2, 3],
            "created_at": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "status": ["active", "inactive", "active"],
            "address": ["123 Main St", "456 Elm St", "789 Oak St"],
            "latitude": [40.123, 40.456, 40.789],
            "longitude": [-73.123, -73.456, -73.789],
            "x_sp": [123, 456, 789],
            "y_sp": [321, 654, 987],
            "bin": [111, 222, 333],
            "bbl": [444, 555, 666],
            "census tract": [777, 888, 999],
            "state": ["NY", "NY", "NY"],
            "council district": [123, 456, 789],
            "boro_ct": [101, 202, 303],
            "nta": ["NTA1", "NTA2", "NTA3"],
            "st_senate": [1111, 2222, 3333],
            "st_assem": [4444, 5555, 6666],
            "cncldist": [7777, 8888, 9999],
            "postcode": [10001, 10002, 10003],
            "community board": [11111, 22222, 33333],
            "borocode": [1, 2, 3],
            "stump_diam": [10, 20, 30],
            "spc_latin": ["Latin1", "Latin2", "Latin3"],
            "nta_name": ["NTA Name 1", "NTA Name 2", "NTA Name 3"],
            "target": [1, 0, 1],
        }
    )
    drop_columns(df)

    assert df.columns.tolist() == ["target"]


def test_preprocess_data():
    df = pd.DataFrame(
        {
            "root_stone": ["Yes", "No", "Yes"],
            "root_grate": ["No", "Yes", "No"],
            "root_other": ["No", "Yes", "No"],
            "curb_loc": ["OnCurb", "NotOnCurb", "OnCurb"],
            "sidewalk": ["Damage", "NoDamage", "Damage"],
            "steward": ["1or2", "3or4", "4orMore"],
            "guards": ["Harmful", "Unsure", "Helpful"],
            "spc_common": ["Oak", np.nan, "Maple"],
            "problems": ["Disease,BranchLights", "Stones,BranchOther", ""],
            "user_type": ["A", "B", "A"],
            "health": ["Poor", "Fair", "Good"],
            "trunk_wire": [1, 0, 0],
            "trnk_light": [0, 0, 0],
            "trnk_other": [0, 1, 1],
            "brch_light": [0, 0, 0],
            "brch_shoe": [0, 1, 1],
            "brch_other": [0, 0, 0],
        }
    )
    preprocess_data(df)

    assert df["root_stone"].tolist() == [1, 0, 1]
    assert df["root_grate"].tolist() == [0, 1, 0]
    assert df["root_other"].tolist() == [0, 1, 0]
    assert df["curb_loc"].tolist() == [1, 0, 1]
    assert df["sidewalk"].tolist() == [1, 0, 1]
    assert df["steward"].tolist() == [1, 2, 3]
    assert df["guards"].tolist() == [1, 2, 3]
    assert df["spc_common"].tolist() == ["Oak", "n/d", "Maple"]
    assert df["problems"].tolist() == [2, 2, 1]
    assert df["health"].tolist() == [0, 1, 2]


@given(st.lists(st.text()))
def test_yes_no_to_numeric_hyp(column):
    result = yes_no_to_numeric(column)
    if column == "Yes":
        assert result == 1
    else:
        assert result == 0


df_columns = {
    "root_stone": {
        "elements": st.one_of(st.sampled_from(["Yes", "No"]), st.none()),
        "unique": False,
    },
    "root_grate": {
        "elements": st.one_of(st.sampled_from(["Yes", "No"]), st.none()),
        "unique": False,
    },
    "root_other": {
        "elements": st.one_of(st.sampled_from(["Yes", "No"]), st.none()),
        "unique": False,
    },
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
        "root_stone",
        "root_grate",
        "root_other",
        "trunk_wire",
        "trnk_light",
        "trnk_other",
        "brch_light",
        "brch_shoe",
        "brch_other",
    ]:
        assert data[col].isin([0, 1]).all()
        assert data["curb_loc"].isin([0, 1]).all()
        assert data["sidewalk"].isin([0, 1]).all()
        assert data["steward"].isin([0, 1, 2, 3]).all()
        assert data["guards"].isin([0, 1, 2, 3]).all()
        assert data["spc_common"].notna().all()
        assert data["problems"].apply(lambda x: isinstance(x, int)).all()
        assert data["health"].isin([0, 1, 2, -1]).all()
