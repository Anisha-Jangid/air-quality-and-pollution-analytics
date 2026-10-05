from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/ai_human_validation_2022_2024.csv")
OUTPUT_FILE = Path("data/processed/ai_human_validation_2022_2024.csv")


def update_human_validation():

    # Read the existing file containing the Delhi validation
    existing_df = pd.read_csv(INPUT_FILE)

    # Validated AI explanations for the remaining 7 events
    new_rows = [

        {
            "city": "Bengaluru",
            "extreme_date": "2022-12-18",
            "ai_draft_status": "Generated",
            "human_validation_status": "Accepted with cautious wording",
            "human_correction_required": "No",
            "validation_notes": (
                "Checked PM2.5, baseline, percentage increase, "
                "cross-station values, winter context, and event classification. "
                "No unsupported causal claim or missing weather value was introduced."
            ),
            "final_analyst_explanation": (
                "Bengaluru experienced a broad and sustained PM2.5 elevation "
                "around 18 December 2022. The two-station city average was "
                "105.99 µg/m³ compared with a surrounding baseline of "
                "73.37 µg/m³, representing a 44.44% increase. BTM Layout "
                "recorded 106.72 µg/m³ while Peenya recorded 105.25 µg/m³, "
                "showing that the elevated pollution was broadly observed "
                "across the selected monitoring locations. The event occurred "
                "during winter, but the available evidence does not establish "
                "a single cause. Seasonal conditions and other local or regional "
                "emission sources may have contributed, but these explanations "
                "should be treated as hypotheses rather than confirmed causes."
            )
        },

        {
            "city": "Chennai",
            "extreme_date": "2023-11-12",
            "ai_draft_status": "Generated",
            "human_validation_status": "Accepted with cautious wording",
            "human_correction_required": "No",
            "validation_notes": (
                "Checked PM2.5, baseline, percentage increase, cross-station "
                "values, Diwali context, and Broad/Sustained classification. "
                "Diwali was treated as a possible contributor rather than a "
                "confirmed cause."
            ),
            "final_analyst_explanation": (
                "Chennai experienced a substantial and broadly observed PM2.5 "
                "elevation on 12 November 2023. The two-station city average "
                "was 173.40 µg/m³ compared with a surrounding baseline of "
                "47.12 µg/m³, representing a 267.99% increase. Manali recorded "
                "205.88 µg/m³ while Alandur Bus Depot recorded 140.92 µg/m³. "
                "The event coincided with Diwali, making festival-related "
                "emissions a possible contributing factor, but the available "
                "evidence does not establish Diwali as the sole or confirmed "
                "cause. Seasonal, meteorological, local, and regional factors "
                "may also have contributed."
            )
        },

        {
            "city": "Hyderabad",
            "extreme_date": "2024-04-28",
            "ai_draft_status": "Generated",
            "human_validation_status": "Accepted with cautious wording",
            "human_correction_required": "No",
            "validation_notes": (
                "Checked PM2.5, baseline, percentage increase, cross-station "
                "difference, repeated 887 µg/m³ readings, and D classification. "
                "Event was treated as a potential data-quality anomaly and not "
                "as confirmed pollution-event evidence."
            ),
            "final_analyst_explanation": (
                "Hyderabad recorded an extreme PM2.5 value on 28 April 2024, "
                "but the available evidence does not support interpreting it "
                "as a confirmed city-wide pollution spike. The two-station "
                "city average was 457.27 µg/m³ compared with a surrounding "
                "baseline of 109.39 µg/m³. Sanathnagar recorded 887.00 µg/m³ "
                "while Central University recorded 27.54 µg/m³. Repeated exact "
                "887 µg/m³ values were observed in the underlying hourly data. "
                "The original observations are therefore retained for "
                "transparency but flagged as a potential data-quality anomaly "
                "and not used as confirmed evidence of a pollution event or "
                "assigned a specific pollution cause."
            )
        },

        {
            "city": "Kolkata",
            "extreme_date": "2022-01-21",
            "ai_draft_status": "Generated",
            "human_validation_status": "Accepted with cautious wording",
            "human_correction_required": "No",
            "validation_notes": (
                "Checked PM2.5, baseline, percentage increase, cross-station "
                "values, winter context, and Broad/Sustained classification. "
                "No unsupported causal claim or missing weather value was introduced."
            ),
            "final_analyst_explanation": (
                "Kolkata experienced a broad and sustained PM2.5 elevation "
                "around 21 January 2022. The two-station city average was "
                "181.04 µg/m³ compared with a surrounding baseline of "
                "124.34 µg/m³, representing a 45.60% increase. Rabindra Bharati "
                "University recorded 224.93 µg/m³ while Victoria recorded "
                "137.14 µg/m³. The event occurred during winter, but the "
                "available evidence does not establish a single cause. "
                "Seasonal conditions and local or regional emission sources "
                "may have contributed, but these explanations should be treated "
                "as hypotheses rather than confirmed causes."
            )
        },

        {
            "city": "Lucknow",
            "extreme_date": "2024-11-01",
            "ai_draft_status": "Generated",
            "human_validation_status": "Accepted with cautious wording",
            "human_correction_required": "No",
            "validation_notes": (
                "Checked PM2.5, baseline, percentage increase, cross-station "
                "values, post-Diwali context, and Broad/Sustained classification. "
                "Diwali-related emissions were described only as a possible "
                "contributor."
            ),
            "final_analyst_explanation": (
                "Lucknow experienced a broad and sustained PM2.5 elevation "
                "around 1 November 2024. The two-station city average was "
                "212.50 µg/m³ compared with a surrounding baseline of "
                "121.79 µg/m³, representing a 74.48% increase. Kendriya "
                "Vidyalaya recorded 256.75 µg/m³ while Lalbagh recorded "
                "168.26 µg/m³. The event occurred one day after Diwali, "
                "making festival-related emissions a possible contributing "
                "factor, but the available evidence does not establish Diwali "
                "as the sole or confirmed cause. Seasonal conditions and other "
                "local or regional emission sources may also have contributed."
            )
        },

        {
            "city": "Mumbai",
            "extreme_date": "2022-01-23",
            "ai_draft_status": "Generated",
            "human_validation_status": "Accepted with cautious wording",
            "human_correction_required": "No",
            "validation_notes": (
                "Checked PM2.5, baseline, percentage increase, cross-station "
                "values, winter context, and Broad but spatially uneven "
                "classification. No unsupported causal claim was introduced."
            ),
            "final_analyst_explanation": (
                "Mumbai experienced a substantial PM2.5 elevation around "
                "23 January 2022. The two-station city average was 187.48 "
                "µg/m³ compared with a surrounding baseline of 68.77 µg/m³, "
                "representing a 172.62% increase. Colaba recorded 271.64 µg/m³ "
                "while Borivali East recorded 103.33 µg/m³, indicating "
                "substantial spatial variation in pollution intensity. "
                "The event occurred during winter and was followed by elevated "
                "concentrations over several days. However, the available "
                "evidence does not establish a single cause, and seasonal, "
                "local, and regional factors may all have contributed."
            )
        },

        {
            "city": "Patna",
            "extreme_date": "2024-11-27",
            "ai_draft_status": "Generated",
            "human_validation_status": "Accepted with cautious wording",
            "human_correction_required": "No",
            "validation_notes": (
                "Checked PM2.5, baseline, percentage increase, cross-station "
                "values, post-monsoon context, and Broad but spatially uneven "
                "classification. No unsupported causal claim was introduced."
            ),
            "final_analyst_explanation": (
                "Patna experienced a substantial PM2.5 elevation around "
                "27 November 2024. The two-station city average was 259.10 "
                "µg/m³ compared with a surrounding baseline of 108.56 µg/m³, "
                "representing a 138.67% increase. IGSC Planetarium Complex "
                "recorded 437.11 µg/m³ while Rajbansi Nagar recorded "
                "81.09 µg/m³, showing considerable spatial variation. "
                "The event occurred during the post-monsoon season and "
                "represented a broad but spatially uneven pollution episode. "
                "Seasonal, local, meteorological, and regional factors may "
                "have contributed, but the available evidence does not "
                "establish a single cause."
            )
        }
    ]

    new_df = pd.DataFrame(new_rows)

    # Combine existing Delhi row with the seven new validated rows
    final_df = pd.concat(
        [existing_df, new_df],
        ignore_index=True
    )

    # Prevent accidental duplicate city/date records
    final_df = final_df.drop_duplicates(
        subset=["city", "extreme_date"],
        keep="first"
    )

    # Sort by date for easier reading
    final_df["extreme_date"] = pd.to_datetime(
        final_df["extreme_date"]
    )

    final_df = final_df.sort_values(
        ["extreme_date", "city"]
    )

    final_df["extreme_date"] = final_df[
        "extreme_date"
    ].dt.strftime("%Y-%m-%d")

    final_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("AI + human validation file updated successfully.")
    print("Total validated events:", len(final_df))
    print("\nValidated events:")
    print(
        final_df[
            [
                "city",
                "extreme_date",
                "human_validation_status",
                "human_correction_required"
            ]
        ].to_string(index=False)
    )

    print("\nOutput file:", OUTPUT_FILE)


if __name__ == "__main__":
    update_human_validation()