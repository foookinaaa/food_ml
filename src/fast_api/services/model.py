import os

import pandas as pd

import mlops_ods.utils.utils_etl as ut_etl
from fast_api.schemas.requests import FeatureRequest


class TreeHealthClassifier:
    """
    Classifier the health of tree on 3 classes.

    Methods:
        predict: Predict health of tree by some sample of features
    """

    path_to_model = os.path.join(
        os.path.abspath(os.getcwd()),
        "src/resources",
        "model.bin",
    )
    model = ut_etl.load_model(path_to_model)

    @classmethod
    def predict(cls, features: FeatureRequest):
        """
        Predict probability of health tree

        Args:
            features (dict): Dict with features and values

        Returns:
            dict: Prediction of tree health
        """
        df = pd.DataFrame([features.dict()])
        prediction = cls.model.predict_proba(df)[0]
        health_classes = {0: "Poor", 1: "Fair", 2: "Good"}
        result = {
            name_health: round(score, 4)
            for name_health, score in zip(health_classes.values(), prediction)
        }
        return result
