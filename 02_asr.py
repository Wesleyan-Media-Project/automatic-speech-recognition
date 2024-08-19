# for downloading data to google storage bucket as a csv
# https://cloud.google.com/bigquery/docs/samples/bigquery-extract-table

import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# TODO: Replace project, dataset, bucket, table names with your own
# Additionally, replace path vars with FULL local path to your service key json and automatic-speech-recognition directory
# Should be the same as in '01_asr.py'
bucket_name = 'asr_demo'
project = "wmp-sandbox"
dataset_id = "asr_demo"
table_id = "asr_test"
path_to_service_key = 'service-key.json'
path_to_asr = ".../automatic-speech-recognition"

# Activates google credentials
credentials = service_account.Credentials.from_service_account_file(
    path_to_service_key,
)

client = bigquery.Client(project=project, credentials=credentials)

destination_uri = f"gs://{bucket_name}/results/gs_asr_results.csv"
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
    f"Exported {project}:{dataset_id}.{table_id} to {destination_uri}"
)

# Make a query to order columns correctly and export as csv directly from bigquery table

query = f"""
    SELECT filename, google_asr_text, stt_confidence FROM `{project}.{dataset_id}.{table_id}`
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

directory = os.path.join(path_to_asr, "Results")
os.makedirs(directory, exist_ok=True)
df.to_csv('./Results/asr_results.csv', index=False, encoding="utf-8")
print("asr_results.csv saved to Results folder in local.")

# Optional: Alternatively, to copy files directly from storage bucket
# to local automatic-speech-recognition directory, in terminal use command,
# where "asr_demo" should be replaced with your own bucket name:

# gsutil cp gs://asr_demo/results/gs_asr_results.csv ./Results/

# Note that the fields of the csv that is retrieved using this command are not in order, 
# which is why in this script we choose to manually make a query in order to retrieve the results.