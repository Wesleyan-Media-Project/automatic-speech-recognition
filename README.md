# Wesleyan Media Project - Automatic Speech Recognition

Welcome! This repo contains scripts for performing automatic speech recognition (ASR) on political ad videos.

This repo is a part of the [Cross-platform Election Advertising Transparency Initiative (CREATIVE)](https://www.creativewmp.com/). CREATIVE has the goal of providing the public with analysis tools for more transparency of political ads across online platforms. In particular, CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook. CREATIVE is a joint project of the [Wesleyan Media Project (WMP)](https://mediaproject.wesleyan.edu/) and the [privacy-tech-lab](https://privacytechlab.org/) at [Wesleyan University](https://www.wesleyan.edu).

To analyze the different dimensions of political ad transparency we have developed an analysis pipeline. The scripts in this repo are part of the Data Processing Step in our pipeline.

![A picture of the pipeline diagram](CREATIVE_step2_032524.png)

## Table of Contents

- [1. Overview](#1-overview)
- [2. Setup](#2-setup)
  - [2.1 Access Authorization](#21-access-authorization)
  - [2.2 Install Dependencies](#22-install-dependencies)
  - [2.3 Run the Scripts](#23-run-the-scripts)
- [3. Results Storage](#3-results-storage)
- [4. Thank You!](#4-thank-you)

## 1. Overview

The scripts in this repository work to perform automatic speech recognition on political ad videos, producing a `.csv` file that contains the videos' text recognition results.

## 2. Setup

### 2.1 Access Authorization

The Automatic Speech Recognition (ASR) codes require Google Cloud credentials to interact with Google Cloud Storage, Google BigQuery, and the Google Cloud Speech-to-Text API.

To run the script in this repo, you need to have your own Google Cloud credentials in the form of a JSON file.

Here is how you can set up the credentials:

0. If you have not done it yet, register with [Google Cloud Platform (GCP)](https://cloud.google.com/) and create a project.

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

- For more information about setting up Google Cloud credentials for ASR, you can go to [Google's ASR documentation](https://cloud.google.com/speech-to-text/docs/before-you-begin).

### 2.2 Install Dependencies

In order to copy files between your local drive and Google Storage, you need to install the `gsutil` tool, which can be achieved by installing the Google Cloud CLI. Instructions on how to do so (including the package that must be downloaded) is found [here](https://cloud.google.com/storage/docs/gsutil_install). 

Then, in order to authorize the gcloud CLI using a service account key, run the following command, where `KEY_FILE` is replaced with the full path to your service account key file ([source](https://cloud.google.com/sdk/docs/authorizing)):

```bash
gcloud auth login --cred-file=KEY_FILE
```

You can double-check the list of accounts whose credentials are stored on the local system using the command:

```bash
gcloud auth list
```

and switch the active account by running the command below, where `ACCOUNT` is the full email address of the account:

```bash
gcloud config set account ACCOUNT
```

We recommend creating and activating a Python virtual environment before running the .py scripts:

```bash
python3 -m venv venv
source venv/bin/activate
```

If you want to stop the virtual environment at some point, you can deactivate it:

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

### 2.3 Run the Scripts

Here is how we run the files `01_asr.py` and `02_asr.py`:

1. Run the following bash code to copy wav files to Google Storage. If you have not yet created a Cloud Storage Bucket within your Google Cloud project, you can do so easily by following [these instructions](https://cloud.google.com/storage/docs/creating-buckets). The placeholder `LOCAL_PATH_TO_WAV_FILES` should be replaced with your local path to the wav folder, whereas `storage_bucket_path` should be replaced with the path and/or name of your Storage Bucket.

   ```bash
   gsutil -m cp -r LOCAL_PATH_TO_WAV_FILES gs://storage_bucket_path
   ```

2. Look through the scripts and insert your own credentials/filepaths wherever it is specified. Comments in the code indicate where this is necessary.

3. Run the scripts in order:

   ```bash
   python3 01_asr.py
   python3 02_asr.py
   ```

4. (Optional) After running both scripts, run the the following bash code to copy the csv file from Google storage to your local storage. Note that the fields are not in order, which is why we manually make a query in order to retrieve the results in `02_asr.py`.

   ```bash
   gsutil cp gs://asr_demo/results/*.csv ./Results/
   ```

## 3. Results Storage

When you run `01_asr.py` and `02_asr.py`, the resulting data is saved in a `Results` folder. The data will be in `csv` format, entitled `asr_results.csv`.

- Individual records of data `asr_results.csv` contain the following fields:

  - `filename`: the unique identifier of the video file
  - `google_asr_text`: the videos' text recognition result from Google Cloud Speech-to-Text API
  - `stt_confidence`: the confidence score of the text recognition result

## 4. Thank You

<p align="center"><strong>We would like to thank our supporters!</strong></p><br>

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
