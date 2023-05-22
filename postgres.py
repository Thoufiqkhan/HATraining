import urllib.request
import json
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="sampleDB",
    user="postgres",
    password="Thou16@s"
)
cursor = conn.cursor()
base_url = "https://api.patentsview.org/patents/query?"
table_name = "sampletab"

for page_number in range(1, 11):
    string = 'q={"_gte":{"patent_date":"2010-01-01"}}&f=["patent_id","patent_title","patent_date"]&o={"page":%d,"per_page":10}' % page_number
    api_url = base_url + string
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            for patent in data["patents"]:
                patent_id = patent["patent_id"]
                patent_title = patent["patent_title"]
                patent_date = patent["patent_date"]
                word_count = len(patent_title.split())

                query = f"INSERT INTO \"{table_name}\" (patent_id, patent_title, patent_date, word_count) VALUES (%s, %s, %s, %s)"
                values = (patent_id, patent_title, patent_date, word_count)

                cursor.execute(query, values)
    except urllib.error.URLError as e:
        print(f"Error in {page_number}: {e.reason}")
        break

conn.commit()
cursor.close()
conn.close()
