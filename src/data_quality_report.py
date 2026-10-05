from pathlib import Path
import pandas as pd


INPUT_FILE = Path(
    "data/processed/master_daily_station_2022_2024.csv"
)


def generate_quality_report():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 60)
    print("MASTER DATA QUALITY REPORT")
    print("=" * 60)

    print("\nDataset shape:")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nDate range:")
    print(df["date"].min(), "to", df["date"].max())

    print("\nUnique cities:", df["city"].nunique())
    print("Unique stations:", df["station_code"].nunique())

    print("\nMissing values:")
    missing = df.isna().sum()
    print(missing)

    print("\nMissing percentage:")
    missing_pct = (df.isna().mean() * 100).round(2)
    print(missing_pct)

    print("\nMissing pollutant percentage:")
    pollutants = [
        "pm25",
        "pm10",
        "no2",
        "nh3",
        "so2",
        "co",
        "ozone",
    ]

    for pollutant in pollutants:
        pct = df[pollutant].isna().mean() * 100
        print(f"{pollutant}: {pct:.2f}%")

    print("\nMissing values by station:")
    station_missing = (
        df.groupby(
            ["city", "station_name", "station_code"]
        )[pollutants]
        .apply(lambda x: x.isna().sum())
    )
    print(station_missing)

    print("\nMissing percentage by station:")
    station_missing_pct = (
        df.groupby(
            ["city", "station_name", "station_code"]
        )[pollutants]
        .apply(lambda x: x.isna().mean() * 100)
        .round(2)
    )
    print(station_missing_pct)

    print("\nDuplicate station-date records:")
    duplicates = df.duplicated(
        subset=["station_code", "date"]
    ).sum()
    print(duplicates)

    print("\nRows by city:")
    print(df.groupby("city").size())

    print("\nRows by station:")
    print(
        df.groupby(
            ["city", "station_name", "station_code"]
        ).size()
    )

    print("\n" + "=" * 60)
    print("QUALITY REPORT COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    generate_quality_report()