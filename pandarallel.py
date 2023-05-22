import pandas as pd
import numpy as np
import urllib.request
import json
import multiprocessing
from pandarallel import pandarallel
base_url = "https://api.patentsview.org/patents/query?"
def fetch_data(page_number):
    string = 'q={"_gte":{"patent_date":"2010-01-01"}}&f=["patent_id","patent_title","patent_date"]&o={"page":%d,"per_page":10}' % page_number
    api_url = base_url + string
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            patents = data["patents"]
            df = pd.DataFrame(patents)
            df["word count"] = df["patent_title"].apply(lambda x: len(x.split()))
            return df
    except urllib.error.URLError as e:
        print(f"Error fetching data from page {page_number}: {e.reason}")
        return None
if __name__ == '__main__':
    pandarallel.initialize()
    pool = multiprocessing.Pool(processes=10) 
    results = pool.map(fetch_data, range(1, 11))
    pool.close()
    pool.join()
    for df in results:
        if df is not None:
            df["processed_data"] = df["patent_title"].parallel_apply(lambda x: ßx.upper())
            print(df["processed_data"])
