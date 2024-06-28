from datetime import datetime

import pandas as pd
from feast import FeatureStore


def fetch_historical_features_entity_df(store: FeatureStore, for_batch_scoring: bool):
    # for all entities in the offline store instead
    entity_df = pd.DataFrame.from_dict(
        {
            # entity's join key -> entity values
            "tree_id": [536325, 247341],
            # "event_timestamp" (reserved key) -> timestamps
            "event_timestamp": [
                datetime(2024, 6, 28),
                datetime(2024, 6, 28),
            ],
        }
    )
    # For batch scoring, we want the latest timestamps
    if for_batch_scoring:
        entity_df["event_timestamp"] = pd.to_datetime("now", utc=True)

    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "tree_data_stats:root_stone",
            "tree_data_stats:root_grate",
            "tree_data_stats:root_other",
            "tree_data_stats:curb_loc",
            "tree_data_stats:trunk_wire",
            "tree_data_stats:trnk_light",
            "tree_data_stats:trnk_other",
            "tree_data_stats:brch_light",
            "tree_data_stats:brch_shoe",
            "tree_data_stats:brch_other",
            "tree_data_stats:sidewalk",
            "tree_data_stats:steward",
            "tree_data_stats:guards",
            "tree_data_stats:problems",
            "tree_data_stats:health",
            "transformed_tree_data:brch_light_num",
            "transformed_tree_data:brch_shoe_num",
            "transformed_tree_data:brch_other_num",
            "transformed_tree_data:curb_loc_num",
        ],
    ).to_df()
    print(training_df.head())


def fetch_online_features(store, source: str = ""):
    entity_rows = [
        # {join_key: entity_value}
        {
            "tree_id": 536325,
        },
        {
            "tree_id": 247341,
        },
    ]
    if source == "feature_service":
        features_to_fetch = store.get_feature_service("tree_numeric_v1")
    elif source == "push":
        features_to_fetch = store.get_feature_service("tree_total_v2")
    else:
        features_to_fetch = [
            "tree_data_stats:root_stone",
            "tree_data_stats:root_grate",
            "tree_data_stats:root_other",
            "tree_data_stats:curb_loc",
            "tree_data_stats:trunk_wire",
            "tree_data_stats:trnk_light",
            "tree_data_stats:trnk_other",
            "tree_data_stats:brch_light",
            "tree_data_stats:brch_shoe",
            "tree_data_stats:brch_other",
            "tree_data_stats:sidewalk",
            "tree_data_stats:steward",
            "tree_data_stats:guards",
            "tree_data_stats:problems",
            "tree_data_stats:health",
            "transformed_tree_data:brch_light_num",
            "transformed_tree_data:brch_shoe_num",
            "transformed_tree_data:brch_other_num",
            "transformed_tree_data:curb_loc_num",
        ]
    returned_features = store.get_online_features(
        features=features_to_fetch,
        entity_rows=entity_rows,
    ).to_dict()
    for key, value in sorted(returned_features.items()):
        print(key, " : ", value)
