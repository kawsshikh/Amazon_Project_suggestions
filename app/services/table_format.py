import pandas as pd

def bayesian_score_with_sales(row, C=4.0, m=1000, alpha=0.5):
    s = row['PastMonthsales'] if row['PastMonthsales'] else 1
    v = float(row['Reviews'])
    R = float(row['Rating'])
    weight = v + alpha * s
    total = weight + m
    return (weight / total) * R + (m / total) * C

def filter_table(df: pd.DataFrame, json_query: dict) -> pd.DataFrame:
    # Drop rows with missing essential data
    df = df.dropna(subset=["SalePrice", "Rating"])

    if not json_query.get("sponsored", True):
        df = df[~df["sponsored"]]

    # Iteratively lower star rating threshold until enough products found
    stars = json_query.get("stars", 5)
    limit = json_query.get("limit", 5)

    while True:
        filtered = df[df["Rating"] >= stars]
        if len(filtered) >= limit or stars <= 0:
            json_query["stars"] = stars
            break
        stars = round(stars - 0.1, 1)

    # Apply Bayesian score
    filtered["score"] = filtered.apply(bayesian_score_with_sales, axis=1)

    # Sort results by score and other fallback criteria
    filtered.sort_values( by="score",ascending=False, inplace=True)

    # Return top N
    return filtered.head(limit)
