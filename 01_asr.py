# Step 1: Run the the following bash code to copy wav file folder to google storage 
# Replace '...' with path leading up to asr folder and 'storage_bucket_path' with your own sb path
# gsutil -m cp -r .../automatic-speech-recognition/sample_wavs gs://storage_bucket_path/

# Step 2: Replace code with your own credentials/filepaths wherever specified
# by comments.

# Step 3 (optional): Activate an environment before running .py file
# source wmp/bin/activate

# Make sure you have all the following imports installed

import io
import os
import json
from sox import file_info
from tqdm import tqdm
from google.cloud import speech, bigquery
from google.oauth2 import service_account

# Activates google credentials
# TODO: Replace with your own service account key file path
credentials = service_account.Credentials.from_service_account_file(
    'service-key.json',
)

# To copy files from storage bucket to local (current directory) I used command:
# gsutil cp gs://asr_demo/sample_wavs/*.wav .

# TODO: Replace with FULL path to files in sample_wavs folder
path_wav = "/sample_wavs/"

# Instantiates a bq client
# TODO: Replace project, dataset, and table names with your own
bq_client = bigquery.Client(project='wmp-sandbox', credentials=credentials)
dataset_ref = bq_client.dataset('asr_demo')
table_ref = dataset_ref.table('asr_test')
# query clears the table prior to populating it, replace 'wmp-sandbox.asr_demo.asr_test' with your own info
query = """
    TRUNCATE TABLE `wmp-sandbox.asr_demo.asr_test`
"""
query_job = bq_client.query(query)

# bq job configuration
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
job_config.autodetect = True  # This allows BigQuery to automatically detect the schema

## Transcribe
# Use Google's speech-to-text API

# Instantiates a speech client
client = speech.SpeechClient(credentials=credentials)

# first_lang = "en-US"
# second_lang = "es"

# For each file in the given directory
for wav in tqdm(os.listdir(path_wav)[:]):
    if wav.endswith(".wav"):
        print(path_wav+wav)
        channel = file_info.channels(path_wav+wav)
        #print(channel)
        curr_vid = wav.split('.')[0]
        file_name = path_wav + wav
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(uri='gs://asr_demo/sample_wavs/'+wav) # TODO: Replace uri with own gs path
        config = speech.RecognitionConfig(
            #encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            #sample_rate_hertz=16000,
            #enable_separate_recognition_per_channel=True,
            audio_channel_count = channel,
            language_code='en-US',
            # language_code=first_lang,
            # alternative_language_codes=[second_lang],
            enable_automatic_punctuation=True,
            # Use video model rather than default model for videos
            use_enhanced=True,
            model = 'video'
            #enable_word_confidence=True
            )
        operation = client.long_running_recognize(config=config, audio=audio)
        # Detects speech in the audio file
        print('Waiting for operation to complete...')
        response = operation.result()
        texts = []
        confs = []
        for result in response.results:
            texts.append(result.alternatives[0].transcript)
            confs.append(result.alternatives[0].confidence)
        curr_transcript = ' '.join(texts)
        if len(confs) == 0:
            curr_conf = "NA"
        else:
            curr_conf = max(confs)

        transcript_dict = {
            'filename': curr_vid,
            'google_asr_text': curr_transcript,
            'stt_confidence': curr_conf
        }

        # Convert results into json, stores locally in new temp_jsons folder
        # TODO: Replace "current_path" with the full path to the automatic-speech-recognition folder in your local
        directory = os.path.join("current_path", "temp_jsons")
        os.makedirs(directory, exist_ok=True)
        curr_json_path = "./temp_jsons/" + curr_vid + ".json"
        with open(curr_json_path, "w") as outfile:
            json.dump(transcript_dict, outfile)
        print(curr_vid + ".json saved to temp_jsons folder in local.")

        # Load the JSON file into BigQuery
        with open(curr_json_path, "rb") as source_file:
            job = bq_client.load_table_from_file(source_file, table_ref, job_config=job_config)

        job.result()  # Wait for the job to complete

        print(f"Loaded {job.output_rows} rows into table")

os.system('say "your program has finished"')