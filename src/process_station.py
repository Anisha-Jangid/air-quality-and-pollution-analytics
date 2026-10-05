from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT SETTINGS
# ============================================================

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# We require at least 18 valid hourly observations
# out of 24 hours for a daily pollutant average.
MIN_VALID_HOURS = 18

# Core pollutants used in the project.
POLLUTANT_COLUMNS = {
    "PM2.5 (µg/m³)": "pm25",
    "PM10 (µg/m³)": "pm10",
    "NO2 (µg/m³)": "no2",
    "NH3 (µg/m³)": "nh3",
    "SO2 (µg/m³)": "so2",
    "CO (mg/m³)": "co",
    "Ozone (µg/m³)": "ozone",
}

# Weather variables retained for later analysis.
WEATHER_COLUMNS = {
    "AT (°C)": "temperature",
    "RH (%)": "humidity",
    "WS (m/s)": "wind_speed",
    "WD (deg)": "wind_direction",
    "SR (W/mt2)": "solar_radiation",
    "BP (mmHg)": "pressure",
}


# ============================================================
# PROCESS ONE STATION
# ============================================================

def process_station(
    station_keyword,
    station_name,
    city,
    station_code,
):
    """
    Process all hourly CSV files belonging to one station
    and create hourly + daily analysis-ready datasets.
    """

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # 1. Find raw files for this station
    # --------------------------------------------------------

    files = sorted(RAW_DIR.glob(f"*{station_keyword}*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found for station keyword: {station_keyword}"
        )

    print(f"Found {len(files)} raw CSV file(s) for {station_name}.")

    # --------------------------------------------------------
    # 2. Read and combine the raw files
    # --------------------------------------------------------

    dataframes = []

    for file in files:
        print(f"Reading: {file.name}")

        df = pd.read_csv(file)

        # Convert timestamp to datetime.
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)

    # --------------------------------------------------------
    # 3. Sort by timestamp
    # --------------------------------------------------------

    df = df.sort_values("Timestamp").reset_index(drop=True)

    # --------------------------------------------------------
    # 4. Check duplicate timestamps
    # --------------------------------------------------------

    duplicate_count = df["Timestamp"].duplicated().sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate timestamps "
            f"for {station_name}."
        )

    print("No duplicate timestamps found.")

    # --------------------------------------------------------
    # 5. Select project columns
    # --------------------------------------------------------

    selected_columns = (
        ["Timestamp"]
        + list(POLLUTANT_COLUMNS.keys())
        + list(WEATHER_COLUMNS.keys())
    )

    df = df[selected_columns].copy()

    # Rename pollutant columns.
    df = df.rename(columns=POLLUTANT_COLUMNS)

    # Rename weather columns.
    df = df.rename(columns=WEATHER_COLUMNS)

    # --------------------------------------------------------
    # 6. Add station metadata
    # --------------------------------------------------------

    df["station_name"] = station_name
    df["city"] = city
    df["station_code"] = station_code

    # --------------------------------------------------------
    # 7. Arrange hourly columns
    # --------------------------------------------------------

    hourly_columns = [
        "Timestamp",
        "pm25",
        "pm10",
        "no2",
        "nh3",
        "so2",
        "co",
        "ozone",
        "temperature",
        "humidity",
        "wind_speed",
        "wind_direction",
        "solar_radiation",
        "pressure",
        "station_name",
        "city",
        "station_code",
    ]

    df = df[hourly_columns]

    # --------------------------------------------------------
    # 8. Save processed hourly dataset
    # --------------------------------------------------------

    station_slug = station_keyword.lower().replace(" ", "_")

    hourly_output = (
        PROCESSED_DIR
        / f"{station_slug}_hourly_2022_2024.csv"
    )

    df.to_csv(hourly_output, index=False)

    print("----------------------------------------")
    print("Hourly processing completed successfully.")
    print("----------------------------------------")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Date range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
    print(f"Output file: {hourly_output}")

    # ========================================================
    # DAILY AGGREGATION
    # ========================================================

    print()
    print("Creating daily station-level dataset...")

    # Create date column.
    df["date"] = df["Timestamp"].dt.date

    # --------------------------------------------------------
    # 9. Calculate valid hourly observations per pollutant
    # --------------------------------------------------------

    daily_valid_hours = (
        df.groupby("date")[list(POLLUTANT_COLUMNS.values())]
        .count()
    )

    # --------------------------------------------------------
    # 10. Calculate daily pollutant averages
    # --------------------------------------------------------

    daily_pollutants = (
        df.groupby("date")[list(POLLUTANT_COLUMNS.values())]
        .mean()
    )

    # --------------------------------------------------------
    # 11. Apply the 18-hour coverage rule
    # --------------------------------------------------------

    for pollutant in POLLUTANT_COLUMNS.values():

        insufficient_days = (
            daily_valid_hours[pollutant] < MIN_VALID_HOURS
        )

        daily_pollutants.loc[
            insufficient_days,
            pollutant
        ] = pd.NA

    # --------------------------------------------------------
    # 12. Add station metadata
    # --------------------------------------------------------

    daily = daily_pollutants.reset_index()

    daily["station_name"] = station_name
    daily["city"] = city
    daily["station_code"] = station_code

    # Arrange columns.
    daily_columns = [
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

    daily = daily[daily_columns]

    # --------------------------------------------------------
    # 13. Save daily dataset
    # --------------------------------------------------------

    daily_output = (
        PROCESSED_DIR
        / f"{station_slug}_daily_2022_2024.csv"
    )

    daily.to_csv(daily_output, index=False)

    print("----------------------------------------")
    print("Daily aggregation completed successfully.")
    print("----------------------------------------")
    print(f"Daily rows: {len(daily):,}")
    print(f"Daily columns: {len(daily.columns)}")
    print(f"Output file: {daily_output}")


# ============================================================
# RUN PROCESSING
# ============================================================

if __name__ == "__main__":
    process_station(
        station_keyword="rajbansi_nagar",
        station_name="Rajbansi Nagar",
        city="Patna",
        station_code=5262,
    )