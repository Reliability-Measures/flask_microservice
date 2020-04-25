from googleapiclient.discovery import build

from providers.google.get_credentials import get_credential, \
    get_credential_from_token

#client.cr
# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

#reds = get_cred('token3.pickle', credential_file=CLIENT_SECRETS_FILE)
#print(creds.scopes)
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImY5ZDk3YjRjYWU5MGJjZDc2YWViMjAwMjZmNmI3NzBjYWMyMjE3ODMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiODA3Njg2NTA0MTk4LWs5b2I1czRnNGt1bnVma3J0YjZtYjlzNnNyM2RrYXR1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiODA3Njg2NTA0MTk4LWs5b2I1czRnNGt1bnVma3J0YjZtYjlzNnNyM2RrYXR1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAyOTE5Njg2OTIwNjYxNzU2NTU1IiwiZW1haWwiOiJmYXJydWtoNTAzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoidDJKZHpOS3pGaXdzeDk2WVpVbkVWUSIsIm5hbWUiOiJGYXJydWtoIFNoYWh6YWQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2dqeUlLMU13WGNRd1RvRm9lM3dkV0oxMDRRN1NLalF3X0tIcmR3N0E9czk2LWMiLCJnaXZlbl9uYW1lIjoiRmFycnVraCIsImZhbWlseV9uYW1lIjoiU2hhaHphZCIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNTg3ODI5NzgyLCJleHAiOjE1ODc4MzMzODIsImp0aSI6IjVmZDMyMmE3YjUzYmFiMWI5ZjU4M2FhNmMzMzllZjY2YzQ2MDJiMmYifQ.OJLWVoN51i88F_Uc9sa5YN-r2r3Dzhw4JD4yWfjnZn2-2UCv0rRniH2IdgUHNf1YwuFgVz1ny7jXBdcgt5v-xNWniDYsTAs22-8NO_qfeJu66svtRyT-r0l91KUOtVbhcQg0ZfhkZdf61n7MH3ACMu_DWCkUeKfCuJvlzH7YYv0KXXqq6eOIAeV27B6-HTmJ38qSTCesAvte0ct9ktcUxnZTImgAInwyq1p4L4q2Kit9jUrbihXShLcq_lDS6DW_sD6NwVKQjY96sxibbuFqjxB8I7Y3Sxf1FZeNOiLSH-0WbhEJsasM77PK0CIv3gZyFyHdIp3WNDHt66XmaXxR0Q"
creds = get_credential_from_token(token)
print(creds.scopes)

drive = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
files = drive.files().list().execute()

file_list = files.get('items', [])
print(len(file_list))

#print(files)
print(file_list[0])
for file in file_list:

    print(file['kind'], file['title'], file['mimeType'],
          file['modifiedDate'], file['ownerNames'])
    print("**************************************")

