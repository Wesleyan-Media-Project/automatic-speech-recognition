# Use screen to avoid vpn connecton issue
# See https://linuxize.com/post/how-to-use-linux-screen/

# Step1: run the the following bash code on wesmedia1 
# to activate google credentials:

# export GOOGLE_APPLICATION_CREDENTIALS="/home/jyao01/wmp/ad-media-laura.json"

# Step2: run the the following bash code on wesmedia1
# to copy wav files to google storage 
# Notice the files need to be copyed to the 'ad_media_laura' project

# gsutil -m cp -r /home/jyao01/github/google_2022/data/wav_c gs://ad_data_files/google_2022/batch_03162022

# Step3 (opitional): activate an environment before running .py file
# source wmp/bin/activate

import io
import os
import pandas as pd
from sox import file_info
from tqdm import tqdm
from google.cloud import speech

path_mp4 = "/home/jyao01/github/google_2022/data/mp4_c"
path_wav = "/home/jyao01/github/google_2022/data/wav_c/"


## Transcribe
# Use Google's speech-to-text API

# Instantiates a client
client = speech.SpeechClient()

video_name = []
transcript = []
stt_confidence = []

# first_lang = "en-US"
# second_lang = "es"

for wav in tqdm(os.listdir(path_wav)[:]):
    if wav.endswith(".wav"):
        print(path_wav+wav)
        channel = file_info.channels(path_wav+wav)
        print(channel)
        video_name.append(wav.split('.')[0])
        file_name = path_wav + wav
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(uri='gs://ad_data_files/google_2022/batch_03162022/'+wav)
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
        transcript.append(' '.join(texts))
        if len(confs) == 0:
            temp = "NA"
            stt_confidence.append(temp)
        else:
            stt_confidence.append(max(confs))

df = pd.DataFrame()
df['filename'] = video_name
df['google_asr_text'] = transcript
df['stt_confidence'] = stt_confidence

df.to_csv('result_asr_g2022_raw.csv', index=False, encoding="utf-8")

#os.system('say "your program has finished"')