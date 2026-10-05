from pathlib import Path
import pandas as pd


INPUT_FILE = Path("data/processed/master_daily_station_2022_2024.csv")
OUTPUT_FILE = Path("data/processed/qc_flags_2022_2024.csv")


def create_qc_flags():
    df = pd.read_csv(INPUT_FILE)

    flags = []

    # Flag the known Sanathnagar PM2.5 anomaly.
    sanathnagar_anomaly = (
    (df["station_code"] == 294)
    & (df["date"].isin([
        "2024-04-27",
        "2024-04-28",
        "2024-04-29"
    ]))
    & (df["pm25"].notna())
)

    for _, row in df[sanathnagar_anomaly].iterrows():
        flags.append({
            "date": row["date"],
            "station_name": row["station_name"],
            "city": row["city"],
            "station_code": row["station_code"],
            "pollutant": "PM2.5",
            "value": row["pm25"],
            "flag": "Potential data-quality anomaly",
            "reason": (
                "Repeated exact PM2.5 value of 887 µg/m³ observed "
                "across a prolonged hourly period in the raw source data."
            )
        })

    qc_df = pd.DataFrame(flags)

    if qc_df.empty:
        print("No QC flags found.")
    else:
        qc_df.to_csv(OUTPUT_FILE, index=False)
        print("QC flag file created successfully.")
        print("Number of flagged observations:", len(qc_df))
        print("\nFlagged observations:")
        print(qc_df.to_string(index=False))
        print("\nOutput file:", OUTPUT_FILE)


if __name__ == "__main__":
    create_qc_flags()