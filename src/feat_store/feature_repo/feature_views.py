from datetime import timedelta

import numpy as np
import pandas as pd
from feast import Entity, FeatureService, FeatureView, Field, FileSource, PushSource
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Int64, String

# Define an entity as a primary key used to fetch features
treedata = Entity(name="tree_data", join_keys=["tree_id"])

# Read data from parquet files.
tree_data_stats_source = FileSource(
    path="data/tree_data.parquet",
    event_timestamp_column="timestamp",  # this column should exist in Parquet file
)

# Define Feature View
tree_stats_fv = FeatureView(
    name="tree_data_stats",
    entities=[treedata],
    ttl=timedelta(days=0),
    schema=[
        Field(name="tree_dbh", dtype=Int64),
        Field(name="curb_loc", dtype=String),
        Field(name="health", dtype=String),
        Field(name="spc_common", dtype=String),
        Field(name="steward", dtype=String),
        Field(name="guards", dtype=String),
        Field(name="sidewalk", dtype=String),
        Field(name="user_type", dtype=String),
        Field(name="problems", dtype=String),
        Field(name="root_stone", dtype=String),
        Field(name="root_grate", dtype=String),
        Field(name="root_other", dtype=String),
        Field(name="trunk_wire", dtype=String),
        Field(name="trnk_light", dtype=String),
        Field(name="trnk_other", dtype=String),
        Field(name="brch_light", dtype=String),
        Field(name="brch_shoe", dtype=String),
        Field(name="brch_other", dtype=String),
        Field(name="zip_city", dtype=String),
        Field(name="borough", dtype=String),
    ],
    online=True,
    source=tree_data_stats_source,
    tags={"team": "tree_features"},
)


# Define an on demand feature view which can generate new features based on
# existing feature views and transformation function
@on_demand_feature_view(
    sources=[tree_stats_fv],
    schema=[
        Field(name="curb_loc_num", dtype=Int64),
        Field(name="sidewalk_num", dtype=Int64),
        Field(name="steward_num", dtype=Int64),
        Field(name="guards_num", dtype=Int64),
        Field(name="problems_num", dtype=Int64),
        Field(name="health_num", dtype=Int64),
        Field(name="root_stone_num", dtype=Int64),
        Field(name="root_grate_num", dtype=Int64),
        Field(name="root_other_num", dtype=Int64),
        Field(name="trunk_wire_num", dtype=Int64),
        Field(name="trnk_light_num", dtype=Int64),
        Field(name="trnk_other_num", dtype=Int64),
        Field(name="brch_light_num", dtype=Int64),
        Field(name="brch_shoe_num", dtype=Int64),
        Field(name="brch_other_num", dtype=Int64),
    ],
)
# Transformation function
def transformed_tree_data(inputs: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
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
        df[f"{col}_num"] = (inputs[col] == "Yes") * 1
    df["curb_loc_num"] = (inputs["curb_loc"] == "OnCurb") * 1
    df["sidewalk_num"] = np.where(inputs["sidewalk"] == "Damage", 1, 0)
    df["steward_num"] = (
        inputs["steward"]
        .map({"1or2": 1, "3or4": 2, "4orMore": 3})
        .fillna(0)
        .astype(int)
    )
    df["guards_num"] = (
        inputs["guards"]
        .map({"Harmful": 1, "Unsure": 2, "Helpful": 3})
        .fillna(0)
        .astype(int)
    )
    df["problems_num"] = (
        inputs["problems"].fillna("").apply(lambda x: len(x.split(","))).astype(int)
    )
    df["health_num"] = (
        inputs["health"].map({"Poor": 0, "Fair": 1, "Good": 2}).fillna(-1).astype(int)
    )
    return df


# This groups features into a model version
tree_numeric_v1 = FeatureService(
    name="tree_numeric_v1",
    features=[
        tree_stats_fv[["tree_dbh"]],  # Sub-selects a feature from a feature view
        transformed_tree_data,  # Selects all features from the transformed feature view
    ],
)

tree_total_v2 = FeatureService(
    name="tree_total_v2",
    features=[tree_stats_fv, transformed_tree_data],
)

# -------------
# Defines a way to push data (to be available offline, online or both) into Feast.
tree_data_stats_push_source = PushSource(
    name="tree_data_stats_push_source",
    batch_source=tree_data_stats_source,
)

# Defines a slightly modified version of the feature view from above, where the source
# has been changed to the push source. This allows fresh features to be directly pushed
# to the online store for this feature view.
tree_data_stats_fresh_fv = FeatureView(
    name="tree_data_stats_fresh",
    entities=[treedata],
    ttl=timedelta(days=1),
    schema=[
        Field(name="tree_dbh", dtype=Int64),
        Field(name="curb_loc", dtype=String),
        Field(name="health", dtype=String),
        Field(name="spc_common", dtype=String),
        Field(name="steward", dtype=String),
        Field(name="guards", dtype=String),
        Field(name="sidewalk", dtype=String),
        Field(name="user_type", dtype=String),
        Field(name="problems", dtype=String),
        Field(name="root_stone", dtype=String),
        Field(name="root_grate", dtype=String),
        Field(name="root_other", dtype=String),
        Field(name="trunk_wire", dtype=String),
        Field(name="trnk_light", dtype=String),
        Field(name="trnk_other", dtype=String),
        Field(name="brch_light", dtype=String),
        Field(name="brch_shoe", dtype=String),
        Field(name="brch_other", dtype=String),
        Field(name="zip_city", dtype=String),
        Field(name="borough", dtype=String),
    ],
    online=True,
    source=tree_data_stats_push_source,  # Changed from above
    tags={"team": "tree_features"},
)
