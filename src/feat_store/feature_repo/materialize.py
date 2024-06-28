from datetime import datetime

from feast import FeatureStore

if __name__ == "__main__":
    store = FeatureStore(repo_path=".")

    # Materialize features into the online store
    store.materialize_incremental(end_date=datetime.now())
