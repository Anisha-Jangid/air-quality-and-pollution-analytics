from pathlib import Path
import pandas as pd

INPUT_FILE = Path(
    "data/processed/ai_human_validation_2022_2024.csv"
)


def validate_ai_output():

    df = pd.read_csv(INPUT_FILE)

    print("=" * 60)
    print("FINAL AI + HUMAN VALIDATION QC")
    print("=" * 60)

    # 1. Number of rows
    print("\n1. Total rows:", len(df))

    # 2. Unique cities
    print("2. Unique cities:", df["city"].nunique())

    # 3. Duplicate city/date combinations
    duplicates = df.duplicated(
        subset=["city", "extreme_date"]
    ).sum()

    print("3. Duplicate city/date records:", duplicates)

    # 4. Human validation status
    accepted = (
        df["human_validation_status"]
        == "Accepted with cautious wording"
    ).sum()

    print("4. Accepted validations:", accepted)

    # 5. Human corrections
    corrections = (
        df["human_correction_required"]
        == "Yes"
    ).sum()

    print("5. Human corrections required:", corrections)

    # 6. Missing final explanations
    missing_explanations = (
        df["final_analyst_explanation"]
        .isna()
        .sum()
    )

    print(
        "6. Missing final explanations:",
        missing_explanations
    )

    # 7. Required columns
    required_columns = [
        "city",
        "extreme_date",
        "ai_draft_status",
        "human_validation_status",
        "human_correction_required",
        "validation_notes",
        "final_analyst_explanation"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    print(
        "7. Missing required columns:",
        missing_columns
    )

    # Final checks
    print("\n" + "=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)

    if (
        len(df) == 8
        and df["city"].nunique() == 8
        and duplicates == 0
        and accepted == 8
        and corrections == 0
        and missing_explanations == 0
        and len(missing_columns) == 0
    ):
        print("\nALL AI + HUMAN VALIDATION CHECKS PASSED.")
        print("The final AI validation dataset is ready.")
    else:
        print("\nVALIDATION FAILED.")
        print("Please review the results above.")

    print("\nFile checked:")
    print(INPUT_FILE)


if __name__ == "__main__":
    validate_ai_output()