from kedro.pipeline import node
from pandas import DataFrame


def preprocess_data(df: DataFrame) -> DataFrame:
    """Replace missing values in `df` with zeros."""
    return df.fillna(0)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=preprocess_data,
                inputs="my_csv_data",
                outputs="preprocessed_data",
                name="preprocess_data_node",
            ),
        ]
    )
