from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Air Quality Analytics | India",
    page_icon="🌫️",
    layout="wide",
)


# --------------------------------------------------
# 2. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data" / "processed"


# --------------------------------------------------
# 3. DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_csv(filename):
    """Load an existing processed CSV file."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


# --------------------------------------------------
# 4. LOAD THE MAIN DATASET
# --------------------------------------------------

try:
    daily_data = load_csv(
        "powerbi_daily_station_2022_2024.csv"
    )

except (FileNotFoundError, pd.errors.ParserError) as error:
    st.error(f"Unable to load the main dataset: {error}")
    st.stop()


# --------------------------------------------------
# 5. PREPARE DATA TYPES
# --------------------------------------------------

daily_data["date"] = pd.to_datetime(
    daily_data["date"],
    errors="coerce",
)

daily_data["year"] = pd.to_numeric(
    daily_data["year"],
    errors="coerce",
)

for column in ["pm25", "pm10"]:
    daily_data[column] = pd.to_numeric(
        daily_data[column],
        errors="coerce",
    )


# --------------------------------------------------
# 6. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🌫️ Air Quality Analytics")

st.sidebar.caption(
    "Indian Cities | 2022–2024"
)

page = st.sidebar.radio(
    "Explore the project",
    [
        "Home / Overview",
        "City Analysis",
        "Seasonal Analysis",
        "Pollution Events",
        "Diwali Analysis",
        "GRAP Stage IV",
        "AI-Assisted Explanations",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    "Data source: Central Pollution Control Board (CPCB)"
)

st.sidebar.caption(
    "Analytical results are observational and "
    "should not automatically be interpreted as proof of causation."
)


# --------------------------------------------------
# 7. HOME / OVERVIEW
# --------------------------------------------------

if page == "Home / Overview":

    st.title("Air Quality & Pollution Analytics")
    st.subheader("Exploring air pollution patterns across Indian cities")

    st.write(
        """
        This project analyzes CPCB air-quality monitoring data
        from Indian cities between 2022 and 2024.

        It combines Python-based data preparation, SQL analysis,
        interactive visualizations, policy-period comparisons,
        and AI-assisted explanations reviewed by a human analyst.
        """
    )

    valid_dates = daily_data["date"].dropna()

    if valid_dates.empty:
        st.error("The dataset does not contain valid dates.")
        st.stop()

    first_date = valid_dates.min().date()
    last_date = valid_dates.max().date()

    city_count = daily_data["city"].nunique()
    station_count = daily_data["station_name"].nunique()
    observation_count = len(daily_data)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Cities",
        f"{city_count:,}",
    )

    col2.metric(
        "Monitoring stations",
        f"{station_count:,}",
    )

    col3.metric(
        "Daily station records",
        f"{observation_count:,}",
    )

    col4.metric(
        "Analysis period",
        f"{first_date.year}–{last_date.year}",
    )

    st.divider()

    st.markdown("### Project sections")

    st.markdown(
        """
        - **City Analysis:** Compare pollution levels across cities.
        - **Seasonal Analysis:** Explore changes across seasons and years.
        - **Pollution Events:** Investigate selected extreme pollution events.
        - **Diwali Analysis:** Compare pollution levels around Diwali.
        - **GRAP Stage IV:** Explore pollution patterns before, during,
          and after selected enforcement periods.
        - **AI-Assisted Explanations:** Review evidence-backed draft
          explanations and human validation results.
        """
    )

    st.info(
        "Use the navigation menu on the left to explore the demo. "
        "The charts and analyses will be added and tested section by section."
    )


# --------------------------------------------------
# 8. PLACEHOLDERS FOR REMAINING SECTIONS
# --------------------------------------------------

# --------------------------------------------------
# 8. CITY ANALYSIS
# --------------------------------------------------

elif page == "City Analysis":

    st.title("City Analysis")
    st.write(
        "Compare PM2.5 and PM10 pollution levels across "
        "Indian cities using daily station observations from 2022–2024."
    )

    # City selection
    available_cities = sorted(
        daily_data["city"].dropna().unique().tolist()
    )

    selected_cities = st.multiselect(
        "Select cities to compare",
        options=available_cities,
        default=available_cities,
    )

    if not selected_cities:
        st.warning("Select at least one city to display the analysis.")
        st.stop()

    city_data = daily_data[
        daily_data["city"].isin(selected_cities)
    ].copy()

    # Average pollution by city
    st.subheader("Average pollution by city")

    city_summary = (
        city_data.groupby("city", as_index=False)
        .agg(
            avg_pm25=("pm25", "mean"),
            avg_pm10=("pm10", "mean"),
            station_count=("station_name", "nunique"),
            daily_records=("date", "count"),
        )
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Average PM2.5**")

        pm25_chart = city_summary.sort_values(
            "avg_pm25",
            ascending=False,
        )

        st.bar_chart(
            pm25_chart,
            x="city",
            y="avg_pm25",
            x_label="City",
            y_label="Average PM2.5",
        )

    with col2:
        st.markdown("**Average PM10**")

        pm10_chart = city_summary.sort_values(
            "avg_pm10",
            ascending=False,
        )

        st.bar_chart(
            pm10_chart,
            x="city",
            y="avg_pm10",
            x_label="City",
            y_label="Average PM10",
        )

    st.caption(
        "Values are averages of the available daily station observations. "
        "Missing readings are excluded from each pollutant's average."
    )

    # Summary table
    st.subheader("City summary table")

    display_summary = city_summary.rename(
        columns={
            "city": "City",
            "avg_pm25": "Average PM2.5",
            "avg_pm10": "Average PM10",
            "station_count": "Monitoring stations",
            "daily_records": "Records with valid dates",
        }
    )

    st.dataframe(
        display_summary.round(2),
        use_container_width=True,
        hide_index=True,
    )

    # Year-wise pollution trends
    st.subheader("Year-wise pollution trends")

    yearly_summary = (
        city_data.groupby(["year", "city"], as_index=False)
        .agg(
            avg_pm25=("pm25", "mean"),
            avg_pm10=("pm10", "mean"),
        )
    )

    pollutant_choice = st.selectbox(
        "Choose pollutant",
        options=["PM2.5", "PM10"],
    )

    trend_column = (
        "avg_pm25" if pollutant_choice == "PM2.5"
        else "avg_pm10"
    )

    trend_chart = yearly_summary.pivot(
        index="year",
        columns="city",
        values=trend_column,
    )

    st.line_chart(
        trend_chart,
        x_label="Year",
        y_label=f"Average {pollutant_choice}",
    )

    st.caption(
        "Yearly values summarize available daily station observations "
        "within each selected city. These descriptive comparisons do "
        "not establish the causes of pollution differences."
    )


# --------------------------------------------------
# 9. SEASONAL ANALYSIS
# --------------------------------------------------

elif page == "Seasonal Analysis":

    st.title("Seasonal Analysis")

    st.write(
        "Explore how PM2.5 and PM10 concentrations vary across "
        "seasons and years in the selected cities."
    )

    # Confirm that the dataset contains the required columns.
    required_columns = {"city", "season", "year", "pm25", "pm10"}
    missing_columns = required_columns - set(daily_data.columns)

    if missing_columns:
        st.error(
            "The seasonal dataset is missing these columns: "
            + ", ".join(sorted(missing_columns))
        )
        st.stop()

    # City selector
    available_cities = sorted(
        daily_data["city"].dropna().unique().tolist()
    )

    selected_cities = st.multiselect(
        "Select cities for seasonal analysis",
        options=available_cities,
        default=available_cities,
        key="seasonal_city_selector",
    )

    if not selected_cities:
        st.warning("Select at least one city to continue.")
        st.stop()

    seasonal_data = daily_data[
        daily_data["city"].isin(selected_cities)
    ].copy()

    # Establish the order using the season labels already in the data.
    season_order = sorted(
        seasonal_data["season"].dropna().unique().tolist()
    )

    seasonal_data["season"] = pd.Categorical(
        seasonal_data["season"],
        categories=season_order,
        ordered=True,
    )

    # Average pollutant concentration by season
    st.subheader("Average pollution by season")

    seasonal_summary = (
        seasonal_data.groupby(
            "season",
            observed=True,
            as_index=False,
        )
        .agg(
            avg_pm25=("pm25", "mean"),
            avg_pm10=("pm10", "mean"),
            daily_records=("date", "count"),
        )
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Average PM2.5 by season**")

        st.bar_chart(
            seasonal_summary,
            x="season",
            y="avg_pm25",
            x_label="Season",
            y_label="Average PM2.5",
        )

    with col2:
        st.markdown("**Average PM10 by season**")

        st.bar_chart(
            seasonal_summary,
            x="season",
            y="avg_pm10",
            x_label="Season",
            y_label="Average PM10",
        )

    st.caption(
        "Seasonal averages summarize available daily station "
        "observations for the selected cities. Missing pollutant "
        "readings are excluded from the corresponding averages."
    )

    # Year-wise seasonal trends
    st.subheader("Seasonal trends by year")

    pollutant_choice = st.selectbox(
        "Choose pollutant for seasonal trends",
        options=["PM2.5", "PM10"],
        key="seasonal_pollutant_selector",
    )

    trend_column = (
        "pm25" if pollutant_choice == "PM2.5" else "pm10"
    )

    yearly_seasonal_summary = (
        seasonal_data.groupby(
            ["year", "season"],
            observed=True,
            as_index=False,
        )
        .agg(
            average_concentration=(trend_column, "mean")
        )
    )

    trend_table = yearly_seasonal_summary.pivot(
        index="year",
        columns="season",
        values="average_concentration",
    )

    st.line_chart(
        trend_table,
        x_label="Year",
        y_label=f"Average {pollutant_choice}",
    )

    # Detailed summary table
    st.subheader("Seasonal summary table")

    display_seasonal_summary = seasonal_summary.rename(
        columns={
            "season": "Season",
            "avg_pm25": "Average PM2.5",
            "avg_pm10": "Average PM10",
            "daily_records": "Records with valid dates",
        }
    )

    st.dataframe(
        display_seasonal_summary.round(2),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "These are descriptive comparisons. Seasonal patterns alone "
        "do not establish why pollution levels changed."
    )


# --------------------------------------------------
# 10. POLLUTION EVENTS
# --------------------------------------------------

elif page == "Pollution Events":

    st.title("Extreme Pollution Events")

    st.write(
        "Explore eight selected extreme pollution events identified "
        "in the existing 2022–2024 analysis. Compare event-day PM2.5 "
        "concentrations with their surrounding six-day averages."
    )

    try:
        events = load_csv(
            "final_extreme_event_analysis_2022_2024.csv"
        ).copy()

    except (FileNotFoundError, pd.errors.ParserError) as error:
        st.error(f"Unable to load the event dataset: {error}")
        st.stop()

    required_columns = [
        "city",
        "extreme_date",
        "season",
        "city_extreme_pm25",
        "surrounding_6day_avg_pm25",
        "increase_pct",
        "classification",
        "context",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in events.columns
    ]

    if missing_columns:
        st.error(
            "The event dataset is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    # Prepare data types for filtering and plotting.
    events["extreme_date"] = pd.to_datetime(
        events["extreme_date"],
        errors="coerce",
    )

    numeric_columns = [
        "city_extreme_pm25",
        "surrounding_6day_avg_pm25",
        "increase_pct",
    ]

    for column in numeric_columns:
        events[column] = pd.to_numeric(
            events[column],
            errors="coerce",
        )

    events["year"] = events["extreme_date"].dt.year

    # Filters
    st.subheader("Explore selected events")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        available_cities = sorted(
            events["city"].dropna().unique().tolist()
        )

        selected_cities = st.multiselect(
            "Filter by city",
            options=available_cities,
            default=available_cities,
            key="event_city_filter",
        )

    with filter_col2:
        available_years = sorted(
            events["year"].dropna().astype(int).unique().tolist()
        )

        selected_years = st.multiselect(
            "Filter by year",
            options=available_years,
            default=available_years,
            key="event_year_filter",
        )

    filtered_events = events[
        events["city"].isin(selected_cities)
        & events["year"].isin(selected_years)
    ].copy()

    if filtered_events.empty:
        st.warning(
            "No events match these filters. Select another city or year."
        )
        st.stop()

    # Summary metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric(
        "Selected events",
        f"{len(filtered_events):,}",
    )

    metric_col2.metric(
        "Cities represented",
        f"{filtered_events['city'].nunique():,}",
    )

    anomaly_count = filtered_events[
        filtered_events["classification"].str.contains(
            "Data-Quality Anomaly",
            case=False,
            na=False,
        )
    ].shape[0]

    metric_col3.metric(
        "Potential data anomalies",
        f"{anomaly_count:,}",
    )

    # Event comparison chart
    st.subheader("Event-day PM2.5 vs surrounding average")

    chart_data = filtered_events[
        [
            "city",
            "extreme_date",
            "city_extreme_pm25",
            "surrounding_6day_avg_pm25",
        ]
    ].copy()

    chart_data["event_label"] = (
        chart_data["city"]
        + " — "
        + chart_data["extreme_date"].dt.strftime("%d %b %Y")
    )

    chart_data = chart_data.set_index("event_label")

    chart_data = chart_data.rename(
        columns={
            "city_extreme_pm25": "Event-day PM2.5",
            "surrounding_6day_avg_pm25": "Surrounding 6-day average",
        }
    )

    st.bar_chart(
        chart_data[
            [
                "Event-day PM2.5",
                "Surrounding 6-day average",
            ]
        ],
        x_label="Selected event",
        y_label="PM2.5 concentration",
    )

    st.caption(
        "PM2.5 concentrations are reported in the units of the source "
        "dataset. The surrounding average is the existing six-day "
        "comparison measure used in this project."
    )

    # Detailed event table
    st.subheader("Event details")

    display_events = filtered_events[
        [
            "city",
            "extreme_date",
            "season",
            "city_extreme_pm25",
            "surrounding_6day_avg_pm25",
            "increase_pct",
            "classification",
        ]
    ].copy()

    display_events["extreme_date"] = (
        display_events["extreme_date"].dt.strftime("%Y-%m-%d")
    )

    display_events = display_events.rename(
        columns={
            "city": "City",
            "extreme_date": "Event date",
            "season": "Season",
            "city_extreme_pm25": "Event-day PM2.5",
            "surrounding_6day_avg_pm25": "Surrounding 6-day average",
            "increase_pct": "Increase (%)",
            "classification": "Event classification",
        }
    )

    st.dataframe(
        display_events.round(2),
        use_container_width=True,
        hide_index=True,
    )

    # Event context
    st.subheader("Analyst context")

    for _, event in filtered_events.iterrows():

        event_date = event["extreme_date"]

        if pd.isna(event_date):
            date_label = "Date unavailable"
        else:
            date_label = event_date.strftime("%d %B %Y")

        with st.expander(
            f"{event['city']} — {date_label}"
        ):
            st.markdown(
                f"**Classification:** {event['classification']}"
            )

            st.markdown(
                f"**Season:** {event['season']}"
            )

            st.markdown(
                f"**Event-day PM2.5:** "
                f"{event['city_extreme_pm25']:.2f}"
                if pd.notna(event["city_extreme_pm25"])
                else "**Event-day PM2.5:** Not available"
            )

            st.markdown(
                f"**Surrounding six-day average:** "
                f"{event['surrounding_6day_avg_pm25']:.2f}"
                if pd.notna(event["surrounding_6day_avg_pm25"])
                else "**Surrounding six-day average:** Not available"
            )

            st.write(
                event["context"]
                if pd.notna(event["context"])
                else "No additional context is available."
            )

            if "Data-Quality Anomaly" in str(
                event["classification"]
            ):
                st.warning(
                    "This event was flagged as a potential data-quality "
                    "anomaly. Interpret its unusually high concentration "
                    "cautiously; it should not be treated as a confirmed "
                    "pollution episode without further validation."
                )

    st.info(
        "These are selected events from the project's analysis, not a "
        "complete inventory of all pollution events. Comparisons show "
        "associations, not proof of causation."
    )


# --------------------------------------------------
# 11. DIWALI ANALYSIS
# --------------------------------------------------

elif page == "Diwali Analysis":

    st.title("Diwali Pollution Analysis")

    st.write(
        "Compare average PM2.5 concentrations before, during, "
        "and after Diwali across 2022, 2023, and 2024."
    )

    try:
        diwali_data = load_csv(
            "diwali_comparison_2022_2024.csv"
        ).copy()

    except (FileNotFoundError, pd.errors.ParserError) as error:
        st.error(f"Unable to load the Diwali dataset: {error}")
        st.stop()

    required_columns = ["year", "period", "avg_pm25"]

    missing_columns = [
        column
        for column in required_columns
        if column not in diwali_data.columns
    ]

    if missing_columns:
        st.error(
            "The Diwali dataset is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    # Prepare the data.
    diwali_data["year"] = pd.to_numeric(
        diwali_data["year"],
        errors="coerce",
    )

    diwali_data["avg_pm25"] = pd.to_numeric(
        diwali_data["avg_pm25"],
        errors="coerce",
    )

    period_order = ["Before", "Diwali", "After"]

    diwali_data["period"] = pd.Categorical(
        diwali_data["period"].astype(str).str.strip(),
        categories=period_order,
        ordered=True,
    )

    diwali_data = diwali_data.dropna(
        subset=["year", "period", "avg_pm25"]
    )

    # Year filter.
    st.subheader("Explore by year")

    available_years = sorted(
        diwali_data["year"].astype(int).unique().tolist()
    )

    selected_years = st.multiselect(
        "Select years",
        options=available_years,
        default=available_years,
        key="diwali_year_filter",
    )

    filtered_diwali = diwali_data[
        diwali_data["year"].isin(selected_years)
    ].copy()

    if filtered_diwali.empty:
        st.warning("Select at least one year to view the analysis.")
        st.stop()

    # Summary metrics.
    period_averages = (
        filtered_diwali
        .groupby("period", observed=False)["avg_pm25"]
        .mean()
    )

    before_value = period_averages.get("Before", float("nan"))
    diwali_value = period_averages.get("Diwali", float("nan"))
    after_value = period_averages.get("After", float("nan"))

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric(
        "Average before Diwali",
        f"{before_value:.2f}" if pd.notna(before_value) else "N/A",
    )

    metric_col2.metric(
        "Average during Diwali",
        f"{diwali_value:.2f}" if pd.notna(diwali_value) else "N/A",
    )

    metric_col3.metric(
        "Average after Diwali",
        f"{after_value:.2f}" if pd.notna(after_value) else "N/A",
    )

    st.caption(
        "These metrics are averages of the available yearly comparison "
        "values for the selected years."
    )

    # Chart: compare the three periods within each year.
    st.subheader("PM2.5 before, during, and after Diwali")

    chart_data = filtered_diwali.pivot(
        index="year",
        columns="period",
        values="avg_pm25",
    )

    chart_data = chart_data.reindex(columns=period_order)

    chart_data.index = chart_data.index.astype(int).astype(str)
    chart_data.index.name = "Year"

    chart_data.columns.name = "Period"

    st.bar_chart(
        chart_data,
        x_label="Year",
        y_label="Average PM2.5 concentration",
    )

    # Table of the original comparison values.
    st.subheader("Year-wise comparison")

    display_data = filtered_diwali.copy()

    display_data["year"] = display_data["year"].astype(int)

    display_data = display_data.rename(
        columns={
            "year": "Year",
            "period": "Period",
            "avg_pm25": "Average PM2.5",
        }
    )

    st.dataframe(
        display_data.sort_values(
            ["Year", "Period"]
        ).round(2),
        use_container_width=True,
        hide_index=True,
    )

    # Compare the change after Diwali with the before-Diwali value.
    st.subheader("Change from before Diwali to after Diwali")

    wide_data = filtered_diwali.pivot(
        index="year",
        columns="period",
        values="avg_pm25",
    )

    if {"Before", "After"}.issubset(wide_data.columns):

        change_data = wide_data.dropna(
            subset=["Before", "After"]
        ).copy()

        change_data["Absolute change"] = (
            change_data["After"] - change_data["Before"]
        )

        change_data["Percentage change (%)"] = (
            (change_data["After"] - change_data["Before"])
            / change_data["Before"].where(
                change_data["Before"] != 0
            )
        ) * 100

        change_data.index = (
            change_data.index.astype(int).astype(str)
        )

        change_data.index.name = "Year"

        st.dataframe(
            change_data[
                ["Before", "After", "Absolute change",
                 "Percentage change (%)"]
            ].round(2),
            use_container_width=True,
        )

    else:
        st.info(
            "Both Before and After measurements are needed "
            "to calculate the change."
        )

    st.info(
        "This analysis describes the observed differences in the "
        "existing Diwali comparison dataset. It does not establish "
        "that Diwali or fireworks alone caused those differences."
    )


# --------------------------------------------------
# 12. GRAP STAGE IV ANALYSIS
# --------------------------------------------------

elif page == "GRAP Stage IV":

    st.title("GRAP Stage IV Policy Analysis")

    st.write(
        "Compare average PM2.5 concentrations before, during, "
        "and after the GRAP Stage IV comparison periods in 2023 and 2024."
    )

    try:
        grap_data = load_csv(
            "grap_stage_iv_comparison_2023_2024.csv"
        ).copy()

    except (FileNotFoundError, pd.errors.ParserError) as error:
        st.error(f"Unable to load the GRAP dataset: {error}")
        st.stop()

    required_columns = ["year", "period", "avg_pm25"]

    missing_columns = [
        column
        for column in required_columns
        if column not in grap_data.columns
    ]

    if missing_columns:
        st.error(
            "The GRAP dataset is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    # Prepare the data.
    grap_data["year"] = pd.to_numeric(
        grap_data["year"],
        errors="coerce",
    )

    grap_data["avg_pm25"] = pd.to_numeric(
        grap_data["avg_pm25"],
        errors="coerce",
    )

    period_order = ["Before", "During", "After"]

    grap_data["period"] = pd.Categorical(
        grap_data["period"].astype(str).str.strip(),
        categories=period_order,
        ordered=True,
    )

    grap_data = grap_data.dropna(
        subset=["year", "period", "avg_pm25"]
    )

    # Year filter.
    st.subheader("Explore comparison periods")

    available_years = sorted(
        grap_data["year"].astype(int).unique().tolist()
    )

    selected_years = st.multiselect(
        "Select years",
        options=available_years,
        default=available_years,
        key="grap_year_filter",
    )

    filtered_grap = grap_data[
        grap_data["year"].isin(selected_years)
    ].copy()

    if filtered_grap.empty:
        st.warning("Select at least one year to view the analysis.")
        st.stop()

    # Display the selected periods.
    st.subheader("PM2.5 by comparison period")

    chart_data = filtered_grap.pivot(
        index="year",
        columns="period",
        values="avg_pm25",
    )

    chart_data = chart_data.reindex(columns=period_order)

    chart_data.index = chart_data.index.astype(int).astype(str)
    chart_data.index.name = "Year"
    chart_data.columns.name = "Period"

    st.bar_chart(
        chart_data,
        x_label="Year",
        y_label="Average PM2.5 concentration",
    )

    # Summary metrics for the selected years.
    st.subheader("Selected-period summary")

    period_averages = (
        filtered_grap
        .groupby("period", observed=False)["avg_pm25"]
        .mean()
    )

    before_value = period_averages.get("Before", float("nan"))
    during_value = period_averages.get("During", float("nan"))
    after_value = period_averages.get("After", float("nan"))

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric(
        "Before GRAP",
        f"{before_value:.2f}" if pd.notna(before_value) else "N/A",
    )

    metric_col2.metric(
        "During GRAP",
        f"{during_value:.2f}" if pd.notna(during_value) else "N/A",
    )

    metric_col3.metric(
        "After GRAP",
        f"{after_value:.2f}" if pd.notna(after_value) else "N/A",
    )

    # Year-wise percentage changes.
    st.subheader("Change relative to the Before period")

    wide_data = filtered_grap.pivot(
        index="year",
        columns="period",
        values="avg_pm25",
    )

    if {"Before", "During", "After"}.issubset(wide_data.columns):

        change_data = wide_data.dropna(
            subset=["Before", "During", "After"]
        ).copy()

        change_data["Before to During (%)"] = (
            (change_data["During"] - change_data["Before"])
            / change_data["Before"].where(
                change_data["Before"] != 0
            )
        ) * 100

        change_data["Before to After (%)"] = (
            (change_data["After"] - change_data["Before"])
            / change_data["Before"].where(
                change_data["Before"] != 0
            )
        ) * 100

        change_data.index = (
            change_data.index.astype(int).astype(str)
        )

        change_data.index.name = "Year"

        st.dataframe(
            change_data[
                [
                    "Before",
                    "During",
                    "After",
                    "Before to During (%)",
                    "Before to After (%)",
                ]
            ].round(2),
            use_container_width=True,
        )

    else:
        st.info(
            "All three periods are required to calculate the "
            "year-wise changes."
        )

    # Original comparison values.
    st.subheader("Underlying comparison data")

    display_data = filtered_grap.copy()

    display_data["year"] = display_data["year"].astype(int)

    display_data = display_data.rename(
        columns={
            "year": "Year",
            "period": "Period",
            "avg_pm25": "Average PM2.5",
        }
    )

    st.dataframe(
        display_data.sort_values(
            ["Year", "Period"]
        ).round(2),
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "These values describe the observed comparison periods in the "
        "existing project dataset. Weather, seasonal conditions, other "
        "pollution sources, and the exact comparison windows may also "
        "influence PM2.5. The results do not independently establish "
        "the causal effect of GRAP Stage IV."
    )


# --------------------------------------------------
# 13. AI-ASSISTED SPIKE EXPLANATIONS
# --------------------------------------------------

elif page == "AI-Assisted Explanations":

    st.title("AI-Assisted Pollution Spike Explanations")

    st.write(
        "Explore existing AI-assisted analyst explanations for eight "
        "selected extreme pollution events. Each explanation was "
        "checked against the project's evidence and reviewed by a human."
    )

    # Load the existing project datasets.
    try:
        validation_data = load_csv(
            "ai_human_validation_2022_2024.csv"
        ).copy()

        evidence_data = load_csv(
            "ai_spike_evidence_2022_2024.csv"
        ).copy()

    except (FileNotFoundError, pd.errors.ParserError) as error:
        st.error(f"Unable to load the AI analysis datasets: {error}")
        st.stop()

    # Check required columns.
    validation_columns = [
        "city",
        "extreme_date",
        "ai_draft_status",
        "human_validation_status",
        "human_correction_required",
        "validation_notes",
        "final_analyst_explanation",
    ]

    missing_validation_columns = [
        column
        for column in validation_columns
        if column not in validation_data.columns
    ]

    evidence_columns = [
        "city",
        "extreme_date",
        "city_extreme_pm25",
        "surrounding_6day_avg_pm25",
        "increase_pct",
        "classification",
        "context",
        "temperature",
        "humidity",
        "wind_speed",
    ]

    missing_evidence_columns = [
        column
        for column in evidence_columns
        if column not in evidence_data.columns
    ]

    if missing_validation_columns:
        st.error(
            "The validation dataset is missing columns: "
            + ", ".join(missing_validation_columns)
        )
        st.stop()

    if missing_evidence_columns:
        st.error(
            "The evidence dataset is missing columns: "
            + ", ".join(missing_evidence_columns)
        )
        st.stop()

    # Prepare dates and numeric values.
    validation_data["extreme_date"] = pd.to_datetime(
        validation_data["extreme_date"],
        errors="coerce",
    )

    evidence_data["extreme_date"] = pd.to_datetime(
        evidence_data["extreme_date"],
        errors="coerce",
    )

    evidence_numeric_columns = [
        "city_extreme_pm25",
        "surrounding_6day_avg_pm25",
        "increase_pct",
        "temperature",
        "humidity",
        "wind_speed",
    ]

    for column in evidence_numeric_columns:
        evidence_data[column] = pd.to_numeric(
            evidence_data[column],
            errors="coerce",
        )

    # Match the human-reviewed explanations to their evidence.
    event_key = ["city", "extreme_date"]

    merged_data = validation_data.merge(
        evidence_data,
        on=event_key,
        how="left",
        validate="one_to_one",
        suffixes=("_validation", "_evidence"),
    )

    # Summary metrics.
    total_events = len(merged_data)

    accepted_events = merged_data[
        merged_data["human_validation_status"]
        .astype(str)
        .str.contains("Accepted", case=False, na=False)
    ].shape[0]

    corrections_required = merged_data[
        merged_data["human_correction_required"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["yes", "true", "1"])
    ].shape[0]

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric(
        "Reviewed events",
        f"{total_events:,}",
    )

    metric_col2.metric(
        "Accepted explanations",
        f"{accepted_events:,}",
    )

    metric_col3.metric(
        "Corrections required",
        f"{corrections_required:,}",
    )

    st.caption(
        "These metrics describe the existing human-validation dataset; "
        "they do not measure the general accuracy of an AI model."
    )

    # Select a city and event.
    st.subheader("Explore an explanation")

    available_cities = sorted(
        merged_data["city"].dropna().unique().tolist()
    )

    selected_city = st.selectbox(
        "Select a city",
        options=available_cities,
        key="ai_explanation_city",
    )

    city_events = merged_data[
        merged_data["city"] == selected_city
    ].copy()

    city_events = city_events.sort_values("extreme_date")

    city_events["event_label"] = city_events[
        "extreme_date"
    ].dt.strftime("%d %b %Y")

    selected_event_label = st.selectbox(
        "Select an event date",
        options=city_events["event_label"].tolist(),
        key="ai_explanation_date",
    )

    selected_event = city_events[
        city_events["event_label"] == selected_event_label
    ].iloc[0]

    event_date = selected_event["extreme_date"]

    st.divider()

    # Show the measured evidence.
    st.subheader("1. Observed evidence")

    if pd.notna(event_date):
        st.write(
            f"**City:** {selected_event['city']}  \n"
            f"**Event date:** {event_date.strftime('%d %B %Y')}"
        )

    evidence_col1, evidence_col2, evidence_col3 = st.columns(3)

    event_pm25 = selected_event["city_extreme_pm25"]
    baseline_pm25 = selected_event["surrounding_6day_avg_pm25"]
    increase_pct = selected_event["increase_pct"]

    evidence_col1.metric(
        "Event-day PM2.5",
        f"{event_pm25:.2f} µg/m³"
        if pd.notna(event_pm25)
        else "Not available",
    )

    evidence_col2.metric(
        "Surrounding 6-day average",
        f"{baseline_pm25:.2f} µg/m³"
        if pd.notna(baseline_pm25)
        else "Not available",
    )

    evidence_col3.metric(
        "Increase vs baseline",
        f"{increase_pct:.2f}%"
        if pd.notna(increase_pct)
        else "Not available",
    )

    st.markdown(
        f"**Event classification:** "
        f"{selected_event['classification']}"
    )

    # Weather values, when available.
    st.subheader("Weather context")

    weather_col1, weather_col2, weather_col3 = st.columns(3)

    weather_col1.metric(
        "Temperature",
        f"{selected_event['temperature']:.2f}"
        if pd.notna(selected_event["temperature"])
        else "Not available",
    )

    weather_col2.metric(
        "Humidity",
        f"{selected_event['humidity']:.2f}%"
        if pd.notna(selected_event["humidity"])
        else "Not available",
    )

    weather_col3.metric(
        "Wind speed",
        f"{selected_event['wind_speed']:.2f}"
        if pd.notna(selected_event["wind_speed"])
        else "Not available",
    )

    st.caption(
        "Weather values are shown in the units and aggregation used "
        "by the existing evidence dataset. Missing values are not "
        "filled with invented estimates."
    )

    st.divider()

    # Human-review status.
    st.subheader("2. Human-validation record")

    status_col1, status_col2 = st.columns(2)

    with status_col1:
        st.markdown(
            f"**AI draft status:** "
            f"{selected_event['ai_draft_status']}"
        )

        st.markdown(
            f"**Human-validation status:** "
            f"{selected_event['human_validation_status']}"
        )

    with status_col2:
        st.markdown(
            f"**Human correction required:** "
            f"{selected_event['human_correction_required']}"
        )

    with st.expander("View validation notes", expanded=True):
        st.write(
            selected_event["validation_notes"]
            if pd.notna(selected_event["validation_notes"])
            else "No validation notes are available."
        )

    st.divider()

    # Final human-reviewed explanation.
    st.subheader("3. Final analyst explanation")

    st.markdown(
        selected_event["final_analyst_explanation"]
        if pd.notna(selected_event["final_analyst_explanation"])
        else "No final analyst explanation is available."
    )

    # Explicit warning for the Hyderabad anomaly.
    if "Data-Quality Anomaly" in str(
        selected_event["classification"]
    ):
        st.warning(
            "Potential data-quality anomaly: this event contains "
            "unusually high and repeated PM2.5 readings. The original "
            "observations were retained for transparency, but this "
            "event should not be treated as a confirmed pollution spike "
            "or assigned a specific cause."
        )

    st.info(
        "Methodology: the existing AI-assisted draft and human-reviewed "
        "explanation are displayed alongside their evidence and review "
        "notes. Explanations describe plausible context where appropriate; "
        "they do not establish a single cause for a pollution event."
    )


# --------------------------------------------------
# 14. PLACEHOLDERS FOR REMAINING SECTIONS
# --------------------------------------------------

else:
    st.title(page)

    st.info(
        "This section will be implemented in the next development steps."
    )

    st.write(
        "The existing datasets will be reused without changing "
        "the original analytical workflow."
    )