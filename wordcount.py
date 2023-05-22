import pandas as pd
import urllib.request
import json

base_url = "https://api.patentsview.org/patents/query?"
master_df = pd.DataFrame()

for page_number in range(1, 11):
    string = 'q={"_gte":{"patent_date":"2010-01-01"}}&f=["patent_id","patent_title","patent_date"]&o={"page":%d,"per_page":10}' % page_number
    api_url = base_url + string
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            patents = data["patents"]
            df = pd.DataFrame(patents)
            df["word count"] = df["patent_title"].apply(lambda x: len(x.split()))
            master_df = pd.concat([master_df, df], ignore_index=True)
    except urllib.error.URLError as e:
        print(f"Error fetching data from page {page_number}: {e.reason}")
        break
print(master_df)
