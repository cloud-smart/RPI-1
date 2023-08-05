import os, sys
import io
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scope for the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_authenticated_service():
    # Check if the credentials file exists
    if not os.path.exists('/home/pi/RPI-1/gdrive_upload/token.pickle'):
        print("Credentials not found. Please authorize the app.")
        creds = create_credentials()
    else:
        with open('/home/pi/RPI-1/gdrive_upload/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Refresh the access token if it's expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open('/home/pi/RPI-1/gdrive_upload/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build and return the Drive service
    return build('drive', 'v3', credentials=creds)

def create_credentials():

    # Create the flow
    flow = InstalledAppFlow.from_client_secrets_file('/home/pi/RPI-1/gdrive_upload/credentials.json', SCOPES)

    # Run the authorization process and get the credentials
    creds = flow.run_local_server(port=0)

    # Save the credentials to a file for future use
    with open('/home/pi/RPI-1/gdrive_upload/token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    return creds

def upload_file(file_path, folder_id=None):
    # Get the authenticated Google Drive service
    drive_service = get_authenticated_service()

    # Prepare file metadata
    file_metadata = {
        'name': os.path.basename(file_path),
    }

    # If a specific folder ID is provided, set it as the parent folder
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Create a media object for file upload
    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"File '{file_metadata['name']}' uploaded to Google Drive with ID: {file.get('id')}")

if __name__ == '__main__':
    # Replace 'file_to_upload.txt' with the path of the file you want to 
    file_path = sys.argv[1]

    # Replace 'your_folder_id' with the ID of the folder you want to  upload the file to (optional)
    folder_id = '1H6-c8QuZJ4utgeAg3ykWbMNPAL2JVHMI'

    upload_file(file_path, folder_id)

