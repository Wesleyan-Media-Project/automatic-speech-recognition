# CREATIVE --- Automatic Speech Recognition

Welcome! This repo contains scripts for performing automatic speech recognition (ASR) on political ad videos.

This repo is a part of the [Cross-platform Election Advertising Transparency Initiative (CREATIVE)](https://www.creativewmp.com/). CREATIVE has the goal of providing the public with analysis tools for more transparency of political ads across online platforms. In particular, CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook. CREATIVE is a joint project of the [Wesleyan Media Project (WMP)](https://mediaproject.wesleyan.edu/) and the [privacy-tech-lab](https://privacytechlab.org/) at [Wesleyan University](https://www.wesleyan.edu).

To analyze the different dimensions of political ad transparency we have developed an analysis pipeline. The scripts in this repo are part of the Data Processing Step in our pipeline.

![A picture of the pipeline diagram](images/CREATIVE_step2_032524.png)

## Table of Contents

- [1. Overview](#1-overview)
- [2. Setup](#2-setup)
  - [2.1 Access Authorization](#21-access-authorization)
  - [2.2 Project Setup](#22-project-setup)
  - [2.3 Install Dependencies](#23-install-dependencies)
  - [2.4 Run the Scripts](#24-run-the-scripts)
- [3. Results Storage](#3-results-storage)
- [4. Thank You!](#4-thank-you)

## 1. Overview

The scripts in this repository work to perform automatic speech recognition on political ad videos, producing a `.csv` file that contains the videos' text recognition results.

## 2. Setup

### 2.1 Project Creation & Access Authorization

The Automatic Speech Recognition (ASR) codes require Google Cloud credentials to interact with Google Cloud Storage, Google BigQuery, and the Google Cloud Speech-to-Text API.

To run the script in this repo, you need to have your own Google Cloud credentials in the form of a JSON file.

Here is how you can set up the credentials:

1. Register with [Google Cloud Platform (GCP)](https://cloud.google.com/) and create a project.

   **NOTE**: If you are on a restricted Google account, such as a school account, that prevents you from creating a Google Cloud project, you will need to use a different account.

2. Set up your Google Cloud project for Speech-to-Text and BigQuery:

   - Go to the [Google Cloud Console](https://console.cloud.google.com).
   - Click the [project drop-down](https://console.cloud.google.com/projectselector2/home/dashboard) and select or create the project for which you want to add an API key.
   - Click the navigation menu (three lines in the top left corner) and select "API & Services".
   - Click "Library" in the left side panel, then search for and enable the "Cloud Speech-to-Text API", "BigQuery API", "Cloud Resource Manager API" and "Service Usage API".

3. Create a Service Account:

   - In the Cloud Console, click the navigation menu and select "IAM & Admin".
   - Click "Service Accounts" in the left side panel.
   - Click "Create Service Account" located on the top under the search bar.
   - Enter a name for the service account.
   - Grant the service account access to your project by assigning it the **BigQuery Admin** and **Storage Object Admin** roles. There's no need to grant any users access to the service account, and so you can click through to "Done" after assigning the roles.
   - Click on the service account you just created.
   - Under the "Keys" tab on the top, click "Add Key", click "Create New Key", choose "JSON", and click "Create". This will download a JSON key file, which you should save in your local.

   For more information about setting up Google Cloud credentials for ASR, you can go to [Google's ASR documentation](https://cloud.google.com/speech-to-text/docs/before-you-begin).

4. Install the Google Cloud CLI:

   - In order to handle access authorization as well as copy files between your local drive and Google Storage, you need to install the `gsutil` and `gcloud` command-line tools, which can be achieved by installing the Google Cloud CLI. Follow [these instructions](https://cloud.google.com/storage/docs/gsutil_install#sdk-install) in order to download the required package, using your new service account email and project ID as credentials when walking through the `gcloud init` command.

   **NOTE**: If you are receiving the error `gcloud: command not found`, try opening a new terminal window in order to have your changes take effect.

5. Then, in order to confirm the authorization of the gcloud CLI using a service account key, run the following command, where `KEY_FILE` is replaced with the full path to your service account key file ([source](https://cloud.google.com/sdk/docs/authorizing#key))

   ```bash
   gcloud auth login --cred-file=KEY_FILE
   ```

   If you're told that the account is already authenticated, then you are good to go, and do not have to overwrite the existing credentials.
   You can double-check the list of accounts whose credentials are stored on the local system using the command:

   ```bash
   gcloud auth list
   ```

   and switch the active account by running the command below, where `ACCOUNT` is the full email address of the account:

   ```bash
   gcloud config set account ACCOUNT
   ```

   Make sure that the service account you just created is the active account.

### 2.2 Project Setup

The ASR scripts require that you have a dataset and table within your project. Instructions on how to create a dataset is found [here](https://cloud.google.com/bigquery/docs/datasets), and instructions on how to create a table is found [here](https://cloud.google.com/bigquery/docs/tables).

### 2.3 Install Dependencies

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

### 2.4 Run the Scripts

Here is how we run the files `01_asr.py` and `02_asr.py`:

1. Run the following bash code to copy wav files to Google Storage. If you have not yet created a Cloud Storage Bucket within your Google Cloud project, you can do so easily by following [these instructions](https://cloud.google.com/storage/docs/creating-buckets). The placeholder `...` should be replaced with your full local path leading up to the asr folder, whereas `storage_bucket_path` should be replaced with the path and/or name of your Storage Bucket.

   ```bash
   gsutil -m cp -r .../automatic-speech-recognition/sample_wavs gs://storage_bucket_path
   ```

2. Look through the scripts and insert your own credentials/filepaths wherever it is specified. Comments in the code indicate where this is necessary.

3. Run the scripts in order:

   ```bash
   python3 01_asr.py
   python3 02_asr.py
   ```

4. (Optional) After running both scripts, run the the following bash code if you wish to copy the csv file directly from Google storage to your local storage. The placeholder `asr_demo` should be replaced with the path and/or name of your Storage Bucket. Note that the fields of the `csv` that is retrieved using this command are not in order, which is why in `02_asr.py` we choose to manually make a query in order to retrieve the results.

   ```bash
   gsutil cp gs://asr_demo/results/*.csv ./Results/
   ```

## 3. Results Storage

When you run `01_asr.py` and `02_asr.py`, the resulting data is saved in two locations: a `Results` folder located in your local `automatic-speech-recognition`, and a `results` folder located in your chosen Storage Bucket. The data will be in `csv` format, entitled `asr_results.csv` in your local and `gs_asr_results.csv` in the Storage Bucket.

- Individual records of data `asr_results.csv` contain the following fields:

  - `filename`: the unique identifier of the video file
  - `google_asr_text`: the videos' text recognition result from Google Cloud Speech-to-Text API
  - `stt_confidence`: the confidence score of the text recognition result

## 4. Thank You

<p align="center"><strong>We would like to thank our supporters!</strong></p><br>

<p align="center">This material is based upon work supported by the National Science Foundation under Grant Numbers 2235006, 2235007, and 2235008.</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2235006">
    <img class="img-fluid" src="images/nsf.png" height="150px" alt="National Science Foundation Logo">
  </a>
</p>

<p align="center">The Cross-Platform Election Advertising Transparency Initiative (CREATIVE) is a joint infrastructure project of the Wesleyan Media Project and privacy-tech-lab at Wesleyan University in Connecticut.

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://www.creativewmp.com/">
    <img class="img-fluid" src="images/CREATIVE_logo.png"  width="220px" alt="CREATIVE Logo">
  </a>
</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://mediaproject.wesleyan.edu/">
    <img src="images/wmp-logo.png" width="218px" height="100px" alt="Wesleyan Media Project logo">
  </a>
</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://privacytechlab.org/" style="margin-right: 20px;">
    <img src="images/plt_logo.png" width="200px" alt="privacy-tech-lab logo">
  </a>
</p>
