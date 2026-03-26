import pandas as pd
import numpy as np

df = pd.read_csv("no_dup_rows.csv")

def clean(x):
    if pd.isna(x):
        return ""
    return str(x).lower().strip()

def get_words(text):
    return set(clean(text).split())

def compute_score(row):

    score = 0
    input_words = get_words(row["input_company_name"])
    cand_words = get_words(row["company_name"])
    score += min(len(input_words & cand_words) * 10, 50)

    if clean(row["input_main_country"]) == clean(row["main_country"]):
        score += 25

    if clean(row["input_main_region"]) == clean(row["main_region"]):
        score += 15

    if clean(row["input_main_city"]) == clean(row["main_city"]):
        score += 10

    return score


df["score"] = df.apply(compute_score, axis=1)

threshold = 50

group_cols = [
    "input_company_name",
    "input_main_country",
    "input_main_region",
    "input_main_city"
]

best_matches = df.loc[
    df.groupby(group_cols)["score"].idxmax()
]

matched = best_matches[best_matches["score"] >= threshold]
unmatched = best_matches[best_matches["score"] < threshold]

matched.to_csv("best_matches.csv", index=False)
unmatched.to_csv("unmatched_rows.csv", index=False)
unmatched.drop(columns=["score"]).to_csv("unmatched_rows.csv", index=False)

print("Matched:", len(best_matches))
print("Unmatched:", len(unmatched))
