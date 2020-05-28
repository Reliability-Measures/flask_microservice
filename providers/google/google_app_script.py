"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
from __future__ import print_function

from googleapiclient import errors
from googleapiclient.discovery import build

from providers.google.get_credentials import GoogleCredentials
from common.config import initialize_config

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/script.projects']

SAMPLE_CODE = '''
function helloWorld() {
  console.log("Hello, world!");
}
'''.strip()

SAMPLE_MANIFEST = '''
{
  "timeZone": "America/Chicago",
  "exceptionLogging": "CLOUD"
}
'''.strip()


def main(creds=None):
    """Calls the Apps Script API.
    """
    # creds = None
    # # The file token.pickle stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token4.pickle'):
    #     with open('token4.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token4.pickle', 'wb') as token:
    #         pickle.dump(creds, token)

    service = build('script', 'v1', credentials=creds)

    # Call the Apps Script API
    try:
        # Create a new project
        request = {'title': 'My Script'}
        response = service.projects().create(body=request).execute()

        # Upload two files to the project
        request = {
            'files': [{
                'name': 'hello',
                'type': 'SERVER_JS',
                'source': SAMPLE_CODE
            }, {
                'name': 'appsscript',
                'type': 'JSON',
                'source': SAMPLE_MANIFEST
            }]
        }
        response = service.projects().updateContent(
            body=request,
            scriptId=response['scriptId']).execute()
        print('https://script.google.com/d/' + response['scriptId'] + '/edit')
    except errors.HttpError as error:
        # The API encountered a problem.
        print(error.content)


if __name__ == '__main__':
    initialize_config()
    creds = GoogleCredentials().get_credential_local()
    main(creds)
