import urllib.request
import json
import pandas as pd
def get_all_patent_ids():
    base_url = "https://api.patentsview.org/patents/query?"
    api_url = base_url + 'q={"_gte":{"patent_date":"2010-01-01"}}&f=["patent_id"]&o={"per_page":10}'
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            patents = data["patents"]
            patent_ids = [patent["patent_id"] for patent in patents]
            return patent_ids
    except urllib.error.URLError as e:
        print(f"Error in retrieving patent IDs: {e.reason}")
        return []
def get_patent_data(patent_ids):
    base_url = "https://api.patentsview.org/patents/query?"
    results = []
    for patent_id in patent_ids:
        string = 'q={"patent_id":"' + patent_id + '"}&f=["patent_id","patent_title","patent_date"]'
        api_url = base_url + string
        try:
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read().decode())
                if data["patents"] is not None:
                    results.append(data["patents"])
        except urllib.error.URLError as e:
            print(f"Error for patent ID {patent_id}: {e.reason}")
    table_data = []
    for patents in results:
        for patent in patents:
            patent_id = patent["patent_id"]
            patent_title = patent["patent_title"]
            patent_date = patent["patent_date"]
            table_data.append([patent_id, patent_title, patent_date])
    df = pd.DataFrame(table_data, columns=["Patent ID", "Patent Title", "Patent Date"])
    return df
patent_ids = get_all_patent_ids()[:10]
table = get_patent_data(patent_ids)
print(table)
