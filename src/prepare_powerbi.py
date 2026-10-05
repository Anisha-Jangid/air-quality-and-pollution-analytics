from pathlib import Path
import pandas as pd


INPUT_FILE = Path(
    "data/processed/master_daily_station_2022_2024.csv"
)

OUTPUT_FILE = Path(
    "data/processed/powerbi_daily_station_2022_2024.csv"
)


def prepare_powerbi_data():

    df = pd.read_csv(INPUT_FILE)

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Date fields
    df["year"] = df["date"].dt.year
    df["month_number"] = df["date"].dt.month
    df["month"] = df["date"].dt.strftime("%B")

    # Quarter
    df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)

    # Project-defined seasons
    def assign_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Summer"
        elif month in [6, 7, 8, 9]:
            return "Monsoon"
        else:
            return "Post-Monsoon"

    df["season"] = df["month_number"].apply(assign_season)

    # Sort rows
    df = df.sort_values(
        ["date", "city", "station_name"]
    ).reset_index(drop=True)

    # Save
    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 60)
    print("POWER BI DATA PREPARATION")
    print("=" * 60)

    print("\nShape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nDate range:")
    print(df["date"].min().date(), "to", df["date"].max().date())

    print("\nCities:")
    print(sorted(df["city"].unique()))

    print("\nSeasons:")
    print(df["season"].value_counts())

    print("\nDuplicate station-date rows:")
    print(
        df.duplicated(
            ["station_name", "date"]
        ).sum()
    )

    print("\nOutput file:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    prepare_powerbi_data()