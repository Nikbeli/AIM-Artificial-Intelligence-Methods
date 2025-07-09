import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TitanicFeatures(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        def get_title(name) -> str:
            return name.split(",")[1].split(".")[0].strip()

        def get_cabin_type(cabin) -> str:
            if pd.isna(cabin):
                return "unknown"
            return cabin[0]

        X["Is_married"] = [1 if get_title(name) == "Mrs" else 0 for name in X["Name"]]
        X["Cabin_type"] = [get_cabin_type(cabin) for cabin in X["Cabin"]]
        return X

    def get_feature_names_out(self, features_in):
        return np.append(features_in, ["Is_married", "Cabin_type"], axis=0)
