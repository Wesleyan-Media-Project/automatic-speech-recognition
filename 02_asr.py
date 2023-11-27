# for downloading data to google storage bucket as a csv
# https://cloud.google.com/bigquery/docs/samples/bigquery-extract-table

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Activates google credentials, replace with your own service account key file
credentials = service_account.Credentials.from_service_account_file(
    '/Users/bella.tassone/ServiceKeys/wmp-sandbox-f8a61d63a8e5.json',
)

client = bigquery.Client(project='wmp-sandbox', credentials=credentials)
bucket_name = 'asr_demo/results'
project = "wmp-sandbox"
dataset_id = "asr_demo"
table_id = "asr_test"

destination_uri = "gs://{}/{}".format(bucket_name, "gs_asr_results.csv")
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table(table_id)

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    # Location must match that of the source table.
    location="US",
)  # API request
extract_job.result()  # Waits for job to complete.

print(
    "Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
)

# To copy files from storage bucket to local (current directory) use command:
# gsutil cp gs://asr_demo/results/*.csv ./Results/

# You may alternatively make a query to order columns correctly and export as csv directly from bigquery table

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