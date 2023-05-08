from kedro.pipeline import node, Pipeline
from kedro.io import DataCatalog, MemoryDataSet, CSVLocalDataSet
from .nodes.data_processing import preprocess_data


def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=preprocess_data,
            inputs=['raw_data'],
            outputs='preprocessed_data',
            name='preprocess_data_node'
        )
    ])
