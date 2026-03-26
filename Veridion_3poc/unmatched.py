import pandas as pd
import time
from ddgs import DDGS


df = pd.read_csv("unmatched_rows.csv")
print(f"\n{len(df)} unmatched rows.")

def get_top_search_result(row):

    name = str(row.get("input_company_name", ""))
    city = str(row.get("input_main_city", ""))
    region = str(row.get("input_main_region", ""))
    country = str(row.get("input_main_country", ""))
    
    if name.lower() == "nan" or not name.strip():
        return pd.Series([None, None])

    query_pieces = [name, city, region, country, "official website"]
    clean_pieces = [piece for piece in query_pieces if piece.strip() and piece.lower() != "nan"]
    query = " ".join(clean_pieces)

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            
            if results:
               # time.sleep(1)
                return pd.Series([results[0].get("title"), results[0].get("href")])
                
    except Exception as e:
        print(f"  -> Error searching for {name}: {e}")
        
    return pd.Series([None, None])


print("\nWeb Search going \n")

df[["ddg_title", "ddg_url"]] = df.apply(get_top_search_result, axis=1)
matched_count = df["ddg_url"].notna().sum()
unmatched_count = df["ddg_url"].isna().sum()

df.to_csv("solvedunmatched.csv", index=False)

print(f"Matched : {matched_count}")
print(f"Unmatched: {unmatched_count}")