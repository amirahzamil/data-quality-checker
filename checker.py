"""Data Quality Checker
Reads a CSV file and reports missing values, duplicate rows,
and numeric outliers, then gives an overall quality score.

Usage: python checker.py sample_data.csv
"""
import sys
import pandas as pd


def find_outliers(df):
    """Return {column: count} of outliers using the IQR method."""
    outliers = {}
    for col in df.select_dtypes(include="number").columns:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((df[col] < low) | (df[col] > high)).sum())
        if count > 0:
            outliers[col] = count
    return outliers


def check_quality(df):
    """Run all checks and return the results as a dictionary."""
    missing = df.isna().sum()
    missing = {c: int(n) for c, n in missing.items() if n > 0}
    duplicates = int(df.duplicated().sum())
    outliers = find_outliers(df)

    # Score: share of "problem cells" out of all cells
    total_cells = df.shape[0] * df.shape[1]
    problems = (
        sum(missing.values())
        + duplicates * df.shape[1]
        + sum(outliers.values())
    )
    score = max(0, round(100 * (1 - problems / total_cells), 1))

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing": missing,
        "duplicates": duplicates,
        "outliers": outliers,
        "score": score,
    }


def print_report(result):
    print("=" * 40)
    print("DATA QUALITY REPORT")
    print("=" * 40)
    print(f"Rows: {result['rows']} | Columns: {result['columns']}")
    print(f"\nDuplicate rows: {result['duplicates']}")

    print("\nMissing values:")
    if result["missing"]:
        for col, n in result["missing"].items():
            print(f"  - {col}: {n}")
    else:
        print("  None")

    print("\nOutliers:")
    if result["outliers"]:
        for col, n in result["outliers"].items():
            print(f"  - {col}: {n}")
    else:
        print("  None")

    print(f"\nQuality score: {result['score']}/100")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python checker.py <file.csv>")
        sys.exit(1)
    data = pd.read_csv(sys.argv[1])
    print_report(check_quality(data))
