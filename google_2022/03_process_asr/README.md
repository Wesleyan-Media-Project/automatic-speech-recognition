### Access authorization

The Automatic Speech Recognition (ASR) codes require Google Cloud credentials to interact with Google Cloud Storage and the Google Cloud Speech-to-Text API. 

To run the script in this repo, you need to have your own Google Cloud credentials in the form of a JSON file. 

Here is how you can set up the credentials:
1) Set up your Google Cloud project for Speech-to-Text

   - Go to the [Google Cloud Console](console.cloud.google.com).
   - Click the [project drop-down](https://console.cloud.google.com/projectselector2/home/dashboard) and select or create the project for which you want to add an API key.
   - Navigate to the "API & Services" > "Library", then search for and enable the "Cloud Speech-to-Text API".
2) Create a Service Account:

   -  In the Cloud Console, go to the "IAM & Admin" > "Service Accounts" page.
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