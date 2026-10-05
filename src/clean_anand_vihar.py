from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# 1. Define project folders
# ---------------------------------------------------------

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


# ---------------------------------------------------------
# 2. Define Anand Vihar station information
# ---------------------------------------------------------

STATION_NAME = "Anand Vihar"
CITY = "Delhi"
STATION_CODE = 301


# ---------------------------------------------------------
# 3. Define the columns needed for our project
# ---------------------------------------------------------

COLUMN_MAP = {
    "PM2.5 (µg/m³)": "pm25",
    "PM10 (µg/m³)": "pm10",
    "NO2 (µg/m³)": "no2",
    "NH3 (µg/m³)": "nh3",
    "SO2 (µg/m³)": "so2",
    "CO (mg/m³)": "co",
    "Ozone (µg/m³)": "ozone",
    "AT (°C)": "temperature",
    "RH (%)": "humidity",
    "WS (m/s)": "wind_speed",
    "WD (deg)": "wind_direction",
    "SR (W/mt2)": "solar_radiation",
    "BP (mmHg)": "pressure",
}


# ---------------------------------------------------------
# 4. Find Anand Vihar raw CSV files
# ---------------------------------------------------------

raw_files = sorted(RAW_DIR.glob("*.csv"))

if not raw_files:
    raise FileNotFoundError(
        "No CSV files were found in data/raw."
    )


print(f"Found {len(raw_files)} raw CSV file(s).")


# ---------------------------------------------------------
# 5. Read and standardize each CSV
# ---------------------------------------------------------

processed_data = []

for file in raw_files:

    print(f"\nReading: {file.name}")

    df = pd.read_csv(file)

    # Convert timestamp from text to datetime
    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    # Check for invalid timestamps
    invalid_timestamps = df["Timestamp"].isna().sum()

    if invalid_timestamps > 0:
        raise ValueError(
            f"{file.name} contains "
            f"{invalid_timestamps} invalid timestamps."
        )

    # Keep only the project columns that actually exist
    available_columns = [
        column
        for column in COLUMN_MAP
        if column in df.columns
    ]

    df = df[["Timestamp"] + available_columns].copy()

    # Rename columns to analysis-friendly names
    df = df.rename(columns=COLUMN_MAP)

    # Add station metadata
    df["station_name"] = STATION_NAME
    df["city"] = CITY
    df["station_code"] = STATION_CODE

    processed_data.append(df)


# ---------------------------------------------------------
# 6. Combine all years
# ---------------------------------------------------------

hourly_data = pd.concat(
    processed_data,
    ignore_index=True
)


# ---------------------------------------------------------
# 7. Sort chronologically
# ---------------------------------------------------------

hourly_data = hourly_data.sort_values(
    "Timestamp"
).reset_index(drop=True)


# ---------------------------------------------------------
# 8. Check for duplicate timestamps
# ---------------------------------------------------------

duplicate_count = hourly_data["Timestamp"].duplicated().sum()

if duplicate_count > 0:
    print(
        f"\nWARNING: {duplicate_count} duplicate timestamps found."
    )
else:
    print("\nNo duplicate timestamps found.")


# ---------------------------------------------------------
# 9. Create output directory if necessary
# ---------------------------------------------------------

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# 10. Save standardized hourly dataset
# ---------------------------------------------------------

output_file = PROCESSED_DIR / "anand_vihar_hourly_2022_2024.csv"

hourly_data.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# 11. Print final summary
# ---------------------------------------------------------

print("\n----------------------------------------")
print("Processing completed successfully.")
print("----------------------------------------")

print(f"Rows: {len(hourly_data):,}")
print(f"Columns: {len(hourly_data.columns)}")

print(
    f"Date range: "
    f"{hourly_data['Timestamp'].min()} "
    f"to "
    f"{hourly_data['Timestamp'].max()}"
)

print(f"Output file: {output_file}")

# ---------------------------------------------------------
# 12. Create daily station-level dataset
# ---------------------------------------------------------

print("\nCreating daily station-level dataset...")


# Create a date column from the hourly timestamp
hourly_data["date"] = hourly_data["Timestamp"].dt.date


# Core pollutants for daily analysis
pollutants = [
    "pm25",
    "pm10",
    "no2",
    "nh3",
    "so2",
    "co",
    "ozone",
]


# Count valid hourly observations for each pollutant
daily_counts = (
    hourly_data
    .groupby("date")[pollutants]
    .count()
)


# Calculate daily averages
daily_means = (
    hourly_data
    .groupby("date")[pollutants]
    .mean()
)


# Apply the 18-hour coverage rule
daily_data = daily_means.where(
    daily_counts >= 18
)


# Add station metadata
daily_data["station_name"] = STATION_NAME
daily_data["city"] = CITY
daily_data["station_code"] = STATION_CODE


# Reset the date index
daily_data = daily_data.reset_index()


# Convert date to datetime
daily_data["date"] = pd.to_datetime(
    daily_data["date"]
)


# Reorder columns
daily_data = daily_data[
    [
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
]


# Save daily station-level dataset
daily_output_file = (
    PROCESSED_DIR
    / "anand_vihar_daily_2022_2024.csv"
)


daily_data.to_csv(
    daily_output_file,
    index=False
)


# Print daily dataset summary
print("\n----------------------------------------")
print("Daily aggregation completed successfully.")
print("----------------------------------------")

print(f"Daily rows: {len(daily_data):,}")
print(f"Daily columns: {len(daily_data.columns)}")
print(f"Output file: {daily_output_file}")