# Step 1: Run the the following bash code to copy wav files to google storage 
# gsutil -m cp -r LOCAL_PATH_TO_WAV_FILES gs://storage_bucket_path/

# Step 2 (optional): Activate an environment before running .py file
# source wmp/bin/activate

# Make sure you have all the following imports installed

import io
import os
import json
import pandas as pd
from sox import file_info
from tqdm import tqdm
from google.cloud import speech, bigquery
from google.oauth2 import service_account

# Activates google credentials, replace with your own service account key file
credentials = service_account.Credentials.from_service_account_file(
    '/Users/bella.tassone/ServiceKeys/wmp-sandbox-f8a61d63a8e5.json',
)

# To copy files from storage bucket to local (current directory) I used command:
# gsutil cp gs://asr_demo/*.wav .

path_wav = "/Users/bella.tassone/wav_files/"

## Transcribe
# Use Google's speech-to-text API

# Instantiates a client
client = speech.SpeechClient(credentials=credentials)

video_name = []
transcript = []
stt_confidence = []

# first_lang = "en-US"
# second_lang = "es"

# For each file in the given directory
for wav in tqdm(os.listdir(path_wav)[:]):
    # If the file ends with '.wav' (AKA is a .wav file)
    if wav.endswith(".wav"):
        #print entire path to file
        print(path_wav+wav)
        channel = file_info.channels(path_wav+wav)
        print(channel)
        curr_vid = wav.split('.')[0]
        video_name.append(curr_vid)
        file_name = path_wav + wav
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(uri='gs://asr_demo/'+wav)
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
        # Set timeout based on the videos' length to avoid the following error
        # TimeoutError: Operation did not complete within the designated timeout.
        response = operation.result(timeout=1000000)
        #print(response)
        texts = []
        confs = []
        for result in response.results:
            texts.append(result.alternatives[0].transcript)
            confs.append(result.alternatives[0].confidence)
        curr_transcript = ' '.join(texts)
        transcript.append(curr_transcript)
        if len(confs) == 0:
            temp = "NA"
            curr_conf = temp
            stt_confidence.append(curr_conf)
        else:
            curr_conf = max(confs)
            stt_confidence.append(curr_conf)

        transcript_dict = {
            'filename': curr_vid,
            'google_asr_text': curr_transcript,
            'stt_confidence': curr_conf
        }
        with open(("./temp_jsons/" + curr_vid + ".json"), "w") as outfile:
            json.dump(transcript_dict, outfile)

df = pd.DataFrame()
df['filename'] = video_name
df['google_asr_text'] = transcript
df['stt_confidence'] = stt_confidence

df.to_csv('./Results/result_asr_g2022_raw.csv', index=False, encoding="utf-8")

os.system('say "your program has finished"')