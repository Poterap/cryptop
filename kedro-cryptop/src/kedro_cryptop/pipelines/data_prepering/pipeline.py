from kedro.pipeline import Pipeline, node, pipeline

from .nodes import fill_ticker_nans


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                fill_ticker_nans,
                inputs="tickers",
                outputs="preprocessed_tickers",
                name="fill_ticker_nans"
            ),
            # kolejne kroki potoku
        ]
    )

