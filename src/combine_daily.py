from pathlib import Path
import pandas as pd


PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "master_daily_station_2022_2024.csv"


def combine_daily_files():
    files = sorted(
        PROCESSED_DIR.glob("*_daily_2022_2024.csv")
    )

    if not files:
        raise FileNotFoundError("No daily station files found.")

    print(f"Found {len(files)} daily station files.")

    frames = []

    for file in files:
        print(f"Reading: {file.name}")

        df = pd.read_csv(file)

        required_columns = [
            "date",
            "station_name",
            "city",
            "station_code",
            "pm25",
            "pm10",
            "no2",
            "nh3",
            "so2",
            "co",
            "ozone",
        ]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{file.name} is missing columns: {missing_columns}"
            )

        frames.append(df[required_columns])


    master = pd.concat(frames, ignore_index=True)

    master["date"] = pd.to_datetime(master["date"])

    master = master.sort_values(
        ["city", "station_name", "date"]
    ).reset_index(drop=True)


    print("\n----------------------------------------")
    print("Master dataset created successfully.")
    print("----------------------------------------")
    print("Rows:", len(master))
    print("Columns:", len(master.columns))
    print(
        "Date range:",
        master["date"].min().date(),
        "to",
        master["date"].max().date(),
    )
    print("Unique stations:", master["station_code"].nunique())
    print("Unique cities:", master["city"].nunique())

    print("\nRows per station:")
    print(
        master.groupby(
            ["city", "station_name", "station_code"]
        ).size()
    )


    duplicate_keys = master.duplicated(
        subset=["station_code", "date"]
    ).sum()

    print("\nDuplicate station-date records:", duplicate_keys)


    master.to_csv(
        OUTPUT_FILE,
        index=False,
        date_format="%Y-%m-%d",
    )

    print("\nOutput file:", OUTPUT_FILE)


if __name__ == "__main__":
    combine_daily_files()