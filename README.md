# Wesleyan Media Project - Automatic-Speech-Recognition

Welcome! This repo is part of the Cross-platform Election Advertising Transparency initiatIVE (CREATIVE) project. CREATIVE is a joint infrastructure project of WMP and privacy-tech-lab at Wesleyan University. CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook.

This repo is a part of the data storage and processing step.

## Table of Contents

- [Introduction](#introduction)

- [Objective](#objective)

- [Data](#data)

- [Setup](#setup)
  - [Access Authorization](#access-authorization)
  - [Install Dependencies](#install-dependencies)
  - [Run the Scripts](#run-the-scripts)

## Introduction

This repo contains codes that replicate the workflow used by the Wesleyan Media Project to perform automatic speech recognition (ASR) on political ad videos.

## Objective

Each of our repos belongs to one or more of the following categories:

- Data Collection
- Data Storage & Processing
- Preliminary Data Classification
- Final Data Classification

This repo is part of the data storage and processing section.

## Data

The data created by the scripts in this repo is in csv format.

- An individual record of data `result_asr_g2022_raw.csv` contains the following fields:

  - filename: the unique identifier of the video file
  - google_asr_text: the videos' text recognition result from Google Cloud Speech-to-Text API
  - stt_confidence: the confidence score of the text recognition result

- An individual record of cleaned data `result_asr_g2022.cvs` contains the following fields:
  - filename: the unique identifier of the video file
  - checksum_sha256: the unique SHA-256 hash of the video file
  - google_asr_text: the videos' text recognition result from Google Cloud Speech-to-Text API
  - google_asr_confidence: the confidence score of the text recognition result
  - google_asr_status: the status of the text recognition result. `success` means the ASR process is completed.
  - google_asr_model: the model we used to perform ASR.

## Setup

### Access Authorization

The Automatic Speech Recognition (ASR) codes require Google Cloud credentials to interact with Google Cloud Storage and the Google Cloud Speech-to-Text API.

To run the script in this repo, you need to have your own Google Cloud credentials in the form of a JSON file.

Here is how you can set up the credentials:

1. Set up your Google Cloud project for Speech-to-Text

   - Go to the [Google Cloud Console](console.cloud.google.com).
   - Click the [project drop-down](https://console.cloud.google.com/projectselector2/home/dashboard) and select or create the project for which you want to add an API key.
   - Navigate to the "API & Services" > "Library", then search for and enable the "Cloud Speech-to-Text API".

2. Create a Service Account:

   - In the Cloud Console, go to the "IAM & Admin" > "Service Accounts" page.
   - Click "Create Service Account".
   - Enter a name and description for the service account.
   - Click on the service account you just created.
   - Under the "Keys" tab, click "Add Key" and choose "JSON".
     This will download a JSON key file.

- In code `01_asr_g2022.py`, change the path in line 7 to your own credentials file path:

```
 # export GOOGLE_APPLICATION_CREDENTIALS="path/to/your_google_api_credential.json"
```

- For more information about setting up Google Cloud credentials for ASR, you can go to [this page](https://cloud.google.com/speech-to-text/docs/before-you-begin).

### Install Dependencies

To run the scripts in this repo, you need to install the following dependencies:

```bash
pip install pandas
pip install sox
pip install tqdm
pip install google-cloud-speech
```

### Run the Scripts

For the file `01_asr_g2022.py`, here are the breakdown steps of how we run it in our server:

We use the screen to avoid vpn connection issues. For more information, you can check [here](https://linuxize.com/post/how-to-use-linux-screen/).

Step 1: Run the following bash code to activate Google credentials, replacing `LOCAL_PATH_TO_SERVICE_KEY` with your own local path to your service key JSON:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="LOCAL_PATH_TO_SERVICE_KEY"
```

Step 2: Run the the following bash code to copy wav files to Google storage. The placeholder `LOCAL_PATH_TO_WAV_FILES` should be replaced with your local path to the wav folder, whereas `storage_bucket_path` should be replaced with the path and/or name of your Storage Bucket.

```bash
gsutil -m cp -r LOCAL_PATH_TO_WAV_FILES gs://storage_bucket_path
```

Step 3: (optional): Activate an environment before running .py file

```bash
source wmp/bin/activate
```
