import pathlib

import pandas as pd

CENSUS_DATA = pathlib.Path(__file__).parent.joinpath("resources/census_5_year.csv")


def get_census_data():
    df = pd.read_csv(CENSUS_DATA, skiprows=1)
    df = df[
        [c for c in df.columns if "Households!!Total" in c and "Error" not in c]
        + ["Geography"]
    ]
    df.columns = [c.split("!!")[-1] for c in df.columns]
    df = df.melt(
        id_vars="Geography", var_name="income_bracket", value_name="household_count"
    ).rename(columns={"Geography": "geography"})
    df["income_bracket"] = df["income_bracket"].map(
        {
            "Less than $10,000": 0,
            "$10,000 to $14,999": 10_000,
            "$15,000 to $24,999": 15_000,
            "$25,000 to $34,999": 25_000,
            "$35,000 to $49,999": 35_000,
            "$50,000 to $74,999": 50_000,
            "$75,000 to $99,999": 75_000,
            "$100,000 to $149,999": 100_000,
            "$150,000 to $199,999": 150_000,
            "$200,000 or more": 200_000,
        }
    )
    totals = df[df.income_bracket.isna()][["geography", "household_count"]]
    totals.columns = ["geography", "total_households"]
    df = df[df.income_bracket.notna()]
    df = df.rename(columns={"household_count": "household_percent"})
    df = df.merge(totals, on="geography")
    df["household_count"] = df["household_percent"] * df["total_households"] / 100
    return df.rename(columns={"geography": "affgeoid"})


def mortgage_payment(principal, rate, term):
    return principal * rate / (1 - (1 + rate) ** -term)
