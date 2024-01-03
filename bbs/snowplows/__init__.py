import pathlib

import pandas as pd

PLOW_DATA = pathlib.Path(__file__).parent.joinpath("data/plow_positions.csv")


def get_plow_data():
    return pd.read_csv(PLOW_DATA)


def select_plow_data_for_timestamp(
    df: pd.DataFrame, dt: pd.Timestamp, interval=60 * 30
):
    mark = dt.timestamp() * 1000
    return df[(df["timestamp"] <= mark) & (df["timestamp"] > (mark - interval * 1000))]
