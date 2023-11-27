# Manually make a query to order columns correctly and export as csv directly from bigquery table
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Activates google credentials, replace with your own service account key file
credentials = service_account.Credentials.from_service_account_file(
    '/Users/bella.tassone/ServiceKeys/wmp-sandbox-f8a61d63a8e5.json',
)
# Construct a BigQuery client object.
client = bigquery.Client(project='wmp-sandbox', credentials=credentials)
query = """
    SELECT filename, google_asr_text, stt_confidence FROM `wmp-sandbox.asr_demo.asr_test`
"""
query_job = client.query(query)  # Make an API request.

vids = []
transcripts = []
confs = []

for row in query_job:
    vids.append(row["filename"])
    transcripts.append(row["google_asr_text"])
    confs.append(row["stt_confidence"])

df = pd.DataFrame()
df['filename'] = vids
df['google_asr_text'] = transcripts
df['stt_confidence'] = confs

df.to_csv('./Results/asr_results_ordered.csv', index=False, encoding="utf-8")