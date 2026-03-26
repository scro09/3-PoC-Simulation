import pandas as pd

df = pd.read_csv("presales_data_sample.csv")

print("Original dataset shape:", df.shape)

columns_for_exact_match = [

   "input_company_name",
    "input_main_country_code",
    "input_main_country",
    "input_main_region",
    "input_main_city",
    "input_main_postcode",
    "input_main_street",
    "input_main_street_number",
    "veridion_id",
    "company_name",
    "company_legal_names",
    "company_commercial_names",
    "main_country_code",
    "main_country",
    "main_region",
    "main_city",
    "main_postcode",
    "main_street",
    "main_street_number",
    "main_latitude",
    "main_longitude",
    "locations",
    "num_locations",
    "company_type",
    "year_founded",
    "revenue",
    "revenue_type", 
]

columns_for_exact_match = [col for col in columns_for_exact_match if col in df.columns]


df_dedup = df.drop_duplicates(subset=columns_for_exact_match, keep="first")

original_rows = len(df)
final_rows = len(df_dedup)
removed_rows = original_rows - final_rows
removed_percentage = (removed_rows / original_rows) * 100

print(f"Final rows: {final_rows}")
print(f"Rows removed: {removed_rows}")
print(f"Percentage removed: {removed_percentage:.2f}%")


df_dedup.to_csv("no_dup_rows.csv", index=False)

print("File saved as 'noduprows.csv'")