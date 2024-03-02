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
        presentation = (
            slide_service.presentations().get(presentationId=TEMPLATE_ID).execute()
        )
        slides = presentation.get("slides")
        print(f"The presentation contains {len(slides)} slides:")

        # copy_presentation(creds)

        drive_service = build("drive", "v3", credentials=creds)
        # Call the Drive v3 API
        results = (
            drive_service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])
        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            print(f"{item['name']} ({item['id']})")

        rsp = drive_service.files().list(q=f"name='{TEMPLATE_NAME}'").execute().get('files')[0]
        print(f"QUERY ---- {rsp}")

        # request = {
        #     'presentationId': TEMPLATE_ID
        # }
        # response = slide_service.presentations().copy(body=request).execute()
        # new_presentation_id = response['presentationId']
        #
        # request = {
        #     'title': NEW_PRESENTATION_NAME
        # }
        # slide_service.presentations().update(presentationId=new_presentation_id, body=request).execute()
        #
        # # Mover Apresentação para pasta
        # request = {
        #     'addParents': [{'id': DRIVE_FOLDER_ID}]
        # }
        # service.files().update(fileId=new_presentation_id, body=request).execute()

        # replace_text(service, new_presentation_id, '{{sprint}}', str(sprint_value))

        # formatted_slides = json.dumps(slides, indent=4)
        # print(formatted_slides)
        # for i, slide in enumerate(slides):
        #     print(
        #         f"- Slide #{i + 1} contains"
        #         f" {len(slide.get('pageElements'))} elements."
        #     )
    except HttpError as err:
        print(err)


# def clone_presentation(template_id, new_presentation_name, drive_folder_id, sprint_value):
#     service = build("drive", "v3", credentials=)


# def copy_presentation(creds):
#     try:
#         drive_service = build("drive", "v3", credentials=creds)
#         rsp = drive_service.files().list(q=f"name={TEMPLATE_NAME}").execute().get('files')[0]
#         body = {"name": NEW_PRESENTATION_NAME}
#         presentation_copy = drive_service.files().copy(body=body, fileId=rsp['id']).execute().get('id')
#
#         # return presentation_copy
#
#         # drive_response = (
#         #     drive_service.files().copy(fileId=TEMPLATE_ID, body=body).execute()
#         # )
#         # presentation_copy_id = drive_response.get("id")
#
#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         print("Presentations  not copied")
#         return error
#
#     return presentation_copy
#     # return presentation_copy_id


if __name__ == "__main__":
    main()
