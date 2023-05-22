import urllib.request
import json
base_url = "https://api.patentsview.org/patents/query?"
results = []
for page_number in range(1, 11):
    string = 'q={"_gte":{"patent_date":"2010-01-01"}}&f=["patent_id","patent_title","patent_date"]&o={"page":%d,"per_page":10}' % page_number
    api_url = base_url + string
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            results.append(data["patents"])
    except urllib.error.URLError as e:
        print(f"Error in {page_number}: {e.reason}")
        break
print((results))

