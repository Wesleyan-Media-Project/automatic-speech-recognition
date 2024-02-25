# Wesleyan Media Project - Automatic-Speech-Recognition

Welcome! This repo is part of the Cross-platform Election Advertising Transparency initiatIVE (CREATIVE) project. CREATIVE is a joint infrastructure project of WMP and privacy-tech-lab at Wesleyan University. CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook.

This repo is a part of the Data Processing step.
![A picture of the pipeline diagram](Creative_Pipeline.png)

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
- Data Processing
- Data Classification
- Compiled Final Data

This repo is part of the Data Processing section.

## Data

The data created by the scripts in this repo is in csv format.

- Individual records of data `asr_results_ordered.csv` and `gs_asr_results.csv` contains the following fields:

  - filename: the unique identifier of the video file
  - google_asr_text: the videos' text recognition result from Google Cloud Speech-to-Text API
  - stt_confidence: the confidence score of the text recognition result

## Setup

### Access Authorization

The Automatic Speech Recognition (ASR) codes require Google Cloud credentials to interact with Google Cloud Storage, Google BigQuery, and the Google Cloud Speech-to-Text API.

To run the script in this repo, you need to have your own Google Cloud credentials in the form of a JSON file.

Here is how you can set up the credentials:

1. Set up your Google Cloud project for Speech-to-Text

   - Go to the [Google Cloud Console](https://console.cloud.google.com).
   - Click the [project drop-down](https://console.cloud.google.com/projectselector2/home/dashboard) and select or create the project for which you want to add an API key.
   - Navigate to the "API & Services" > "Library", then search for and enable the "Cloud Speech-to-Text API" and "BigQuery API".

2. Create a Service Account:

   - In the Cloud Console, go to the "IAM & Admin" > "Service Accounts" page.
   - Click "Create Service Account".
   - Enter a name and description for the service account.
   - Click on the service account you just created.
   - Under the "Keys" tab, click "Add Key" and choose "JSON".
     This will download a JSON key file.

- For more information about setting up Google Cloud credentials for ASR, you can go to [this page](https://cloud.google.com/speech-to-text/docs/before-you-begin).

### Install Dependencies

To run the scripts in this repo, you need to install the following dependencies:

```bash
pip install pandas
pip install sox
pip install tqdm
pip install google-cloud-speech
pip install google-cloud-bigquery
pip install google-auth
```

### Run the Scripts

For the file `01_asr.py`, here are the breakdown steps of how we run it in our server:

We use the screen to avoid vpn connection issues. For more information, you can check [here](https://linuxize.com/post/how-to-use-linux-screen/).

Step 1: Run the the following bash code to copy wav files to Google storage. The placeholder `LOCAL_PATH_TO_WAV_FILES` should be replaced with your local path to the wav folder, whereas `storage_bucket_path` should be replaced with the path and/or name of your Storage Bucket.

```bash
gsutil -m cp -r LOCAL_PATH_TO_WAV_FILES gs://storage_bucket_path
```

Step 2: Look through the scripts and insert your own credentials/filepaths wherever it is specified. Comments should clearly indicate where this is necessary.

Step 3: (optional): Activate an environment before running .py file

```bash
source wmp/bin/activate
```

Step 4 (optional): After running both scripts, run the the following bash code to copy csv file from Google storage to your local. Note that the field are not in order, which is why we manually make a query in order to retrieve the results in `02_asr.py`.

```bash
gsutil cp gs://asr_demo/results/*.csv ./Results/
```
