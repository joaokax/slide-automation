import json
import os.path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/presentations.readonly", "https://www.googleapis.com/auth/presentations",
#           "https://www.googleapis.com/auth/drive.file"]

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']

TEMPLATE_ID = os.getenv("TEMPLATE_ID")
TEMPLATE_NAME = "Mercado Topográfico Review Template"
NEW_PRESENTATION_NAME = 'Mercado Topográfico Review 2'
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
SPRINT_VALUE = 43


def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        slide_service = build("slides", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)

        # presentation_result = drive_service.files().list(q=f"name='{TEMPLATE_NAME}'").execute().get('files')[0]
        # presentation_id = presentation_result['id']
        # print(f"ID TEMPLATE ---- {presentation_result['id']}")

        presentation = slide_service.presentations().get(presentationId=TEMPLATE_ID).execute()

        # Criar uma cópia da apresentação
        copy_title = 'Cópia da Apresentação Mercado - 6'
        copy_body = {'name': copy_title}
        copied_presentation = (
            drive_service.files().copy(fileId=TEMPLATE_ID, body=copy_body).execute()
        )

        presentation_copy_id = copied_presentation.get("id")
        print(f'A apresentação foi copiada, ID: {presentation_copy_id}')

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
