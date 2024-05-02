# Wesleyan Media Project - Automatic-Speech-Recognition

Welcome! This repository contains codes that replicate the workflow used by the Wesleyan Media Project to perform automatic speech recognition (ASR) on political ad videos.

This repo is a part of the [Cross-platform Election Advertising Transparency Initiative (CREATIVE)](https://www.creativewmp.com/). CREATIVE has the goal of providing the public with analysis tools for more transparency of political ads across online platforms. In particular, CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook. CREATIVE is a joint project of the [Wesleyan Media Project (WMP)](https://mediaproject.wesleyan.edu/) and the [privacy-tech-lab](https://privacytechlab.org/) at [Wesleyan University](https://www.wesleyan.edu).

To analyze the different dimensions of political ad transparency we have developed an analysis pipeline. The scripts in this repo are part of the Data Processing Step in our pipeline.

![A picture of the pipeline diagram](CREATIVE_step2_032524.png)

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
  - [Access Authorization](#access-authorization)
  - [Install Dependencies](#install-dependencies)
  - [Run the Scripts](#run-the-scripts)
- [Results Storage](#results-storage)
- [Thank You!](#thank-you)

## Overview

The scripts in this repository work to perform automatic speech recognition on political ad videos, producing a `.csv` file that contains the videos' text recognition results.

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

We recommend creating and activating a virtual python environment before running the .py scripts:

```bash
python3 -m venv venv
source venv/bin/activate
```

Deactive the environment with this command:

```bash
deactivate
```

Additionally, to run the scripts in this repo, you need to install the following dependencies:

```bash
pip3 install pandas
pip3 install sox
pip3 install tqdm
pip3 install google-cloud-speech
pip3 install google-cloud-bigquery
pip3 install google-auth
```

### Run the Scripts

For the files `01_asr.py` and `02_asr.py`, here are the breakdown steps of how we run it in our server:

Step 1: Run the the following bash code to copy wav files to Google storage. The placeholder `LOCAL_PATH_TO_WAV_FILES` should be replaced with your local path to the wav folder, whereas `storage_bucket_path` should be replaced with the path and/or name of your Storage Bucket.

```bash
gsutil -m cp -r LOCAL_PATH_TO_WAV_FILES gs://storage_bucket_path
```

Step 2: Look through the scripts and insert your own credentials/filepaths wherever it is specified. Comments should clearly indicate where this is necessary.

Step 3: Run the scripts in order:

```bash
python3 01_asr.py
python3 02_asr.py
```

Step 4 (optional): After running both scripts, run the the following bash code to copy csv file from Google storage to your local. Note that the fields are not in order, which is why we manually make a query in order to retrieve the results in `02_asr.py`.

```bash
gsutil cp gs://asr_demo/results/*.csv ./Results/
```

## Results Storage

When you run `01_asr.py` and `02_asr.py`, the resulting data is saved in a `Results` folder. The data will be in `csv` format, entitled `asr_results.csv`.

- Individual records of data `asr_results.csv` contains the following fields:

  - `filename`: the unique identifier of the video file
  - `google_asr_text`: the videos' text recognition result from Google Cloud Speech-to-Text API
  - `stt_confidence`: the confidence score of the text recognition result

## Thank You

<p align="center"><strong>We would like to thank our financial supporters!</strong></p><br>

<p align="center">This material is based upon work supported by the National Science Foundation under Grant Numbers 2235006, 2235007, and 2235008.</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2235006">
    <img class="img-fluid" src="nsf.png" height="150px" alt="National Science Foundation Logo">
  </a>
</p>

<p align="center">The Cross-Platform Election Advertising Transparency Initiative (CREATIVE) is a joint infrastructure project of the Wesleyan Media Project and privacy-tech-lab at Wesleyan University in Connecticut.

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://www.creativewmp.com/">
    <img class="img-fluid" src="CREATIVE_logo.png"  width="220px" alt="CREATIVE Logo">
  </a>
</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://mediaproject.wesleyan.edu/">
    <img src="wmp-logo.png" width="218px" height="100px" alt="Wesleyan Media Project logo">
  </a>
</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://privacytechlab.org/" style="margin-right: 20px;">
