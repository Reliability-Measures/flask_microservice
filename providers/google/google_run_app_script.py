"""
RM usage of the Apps Script API.

"""
import logging
from googleapiclient import errors
from googleapiclient.discovery import build

from providers.google.get_credentials import GoogleCredentials
from providers.google.create_quiz_app import QUIZ_CODE, QUIZ_MANIFEST
from common.config import initialize_config
from providers.myssql_db import MySqlDB

SCRIPT_ID = '1FJi_cMqS8i1g5tvDMZa7qC60NW0vWSDf4pIOeggLSt5eIwbuPuyjJrB2'
logger = logging.getLogger(__name__)


def run_app_script(credentials=None, script_id=SCRIPT_ID,
                   function_name="myFunction",
                   params=None):
    """Calls the Apps Script API.
    """
    # store = oauth_file.Storage('token2.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('client.json', SCOPES)
    #     creds = tools.run_flow(flow, store)

    if not credentials:
        credentials = GoogleCredentials().get_credential_local()
    service = build('script', 'v1', credentials=credentials)

    # Call the Apps Script API
    result = []
    try:
        # Create an execution request object.
        request = {"function": function_name, "parameters": params}
        response = service.scripts().run(body=request,
                                         scriptId=script_id).execute()

        if 'error' in response:
            # The API executed, but the script returned an error.

            # Extract the first (and only) set of error details. The values of
            # this object are the script's 'errorMessage' and 'errorType', and
            # an list of stack trace elements.
            error = response['error']['details'][0]
            error_msg = "Script error message: {0}".format(error['errorMessage'])
            logger.error(error_msg)

            result = {'error': error_msg}

            if 'scriptStackTraceElements' in error:
                # There may not be a stacktrace if the script didn't start
                # executing.
                #print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    logger.error("\t{0}: {1}".format(trace['function'],
                                              trace['lineNumber']))
            return result
        else:
            # The structure of the result depends upon what the Apps Script
            # function returns.
            result = response['response'].get('result', {})
            if not result:
                logger.warning('No result returned!')

    except errors.HttpError as e:
        # The API encountered a problem before the script started executing.
        logger.error("ERROR", e.content)
        result = {'error': e.content}

    return result


def execute_app_script(credentials=None):
    """Calls the Apps Script API.
    """
    if not credentials:
        credentials = GoogleCredentials().get_credential_local()
    service = build('script', 'v1', credentials=credentials)

    # Call the Apps Script API
    try:
        # Create a new project
        request = {'title': 'My Script'}
        response = service.projects().create(body=request).execute()

        # Upload two files to the project
        request = {
            'files': [{
                'name': 'createQuiz',
                'type': 'SERVER_JS',
                'source': QUIZ_CODE
            }, {
                'name': 'appsscript',
                'type': 'JSON',
                'source': QUIZ_MANIFEST
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
    #execute_app_script()
    initialize_config()

    from quiz.create_quiz import process_items, create_quiz_form_db
    # SCRIPT_ID = "1PGHEjAEw4GeNCd_LfmrmclpU4E9_rnq9vhcO6mzYMzSFpF0Ylr_bNVq3"
    sql = "select id, text, subject, topic, sub_topics, type, " \
          "choices, metadata, answer " \
          "from items where subject='Islam' limit 50"
    options = {'required': 0x03, 'show_correct': 0, 'summary': 1}
    user = {'email': 'farrukh503@gmail.com', 'givenName': 'Farrukh'}
    results = create_quiz_form_db({'quiz_name': 'test', 'options': options,
                                   'user_profile': user}, sql=sql)

    print(results)
