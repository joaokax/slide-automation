import os.path
import emoji
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from azure_devops import get_azure_work_items

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']


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
        print(emoji.emojize(":green_circle: Autenticado. Começando o processo..."))
        slide_template_id = os.getenv("SLIDE_TEMPLATE_ID")
        slide_service = build("slides", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)

        print(emoji.emojize(":blue_circle: Obtendo informações no Azure Devops"))
        azure_object = get_azure_work_items()

        print(emoji.emojize(":blue_circle: Criando a apresentação no Google Drive"))
        presentation_copy_id = create_copy_of_presentation(drive_service, slide_template_id, azure_object)
        next_sprint_number = int(azure_object["sprint"]) + 1

        print(emoji.emojize(":blue_circle: Alterando textos globalmente"))
        replace_text_globally(slide_service, presentation_copy_id, "{{sprint}}", azure_object["sprint"])
        replace_text_globally(slide_service, presentation_copy_id, "{{next_s}}", str(next_sprint_number))

        presentation_copy = slide_service.presentations().get(presentationId=presentation_copy_id).execute()

        # Posição exata dos slides que serão clonados.
        item_slide_original_index = 2
        item_slide_original_id = presentation_copy.get('slides')[item_slide_original_index]['objectId']
        next_sprint_item_slide = 4
        next_sprint_item_slide_id = presentation_copy.get('slides')[next_sprint_item_slide]['objectId']
        items_per_slide = 3

        print(emoji.emojize(":blue_circle: Gerando slides com work items"))
        generate_slides_with_work_items(
            slide_service, presentation_copy_id, items_per_slide, azure_object, item_slide_original_id,
            next_sprint_item_slide_id
        )

        print(emoji.emojize(":fire: Deletando slides de referência"))
        delete_slide(slide_service, presentation_copy_id, item_slide_original_id)
        delete_slide(slide_service, presentation_copy_id, next_sprint_item_slide_id)

        print(emoji.emojize(":fire: Limpando variáveis não usadas"))
        clear_unused_variables_globally(slide_service, presentation_copy_id, items_per_slide)

        print(emoji.emojize(":thumbs_up: Apresentação foi gerada com sucesso!"))

    except HttpError as err:
        print(err)


def generate_slides_with_work_items(
        slide_service, presentation_copy_id: str, items_per_slide: int, azure_object, item_slide_original_id: str,
        next_sprint_item_slide_id: str):
    number_of_slides_created = []
    item_slide_copy_id = ""

    # Iteração em work items da sprint atual e da próxima
    for iteration_index, (items_list, initial_slide_id) in enumerate([
        (azure_object["work_items"], item_slide_original_id),
        (azure_object["next_sprint"], next_sprint_item_slide_id)
    ]):
        total_list_items = len(items_list)
        for index in range(total_list_items):
            # Cria um novo slide a cada 3 work items
            if index % items_per_slide == 0:
                number_of_slides_created.append(index)
                item_slide_copy_id = create_copy_of_item_slide_original(
                    slide_service, presentation_copy_id, initial_slide_id
                )
            # Altera os valores de uma coluna do slide por vez
            replace_text_in_each_column_of_the_item_slide_copy(
                slide_service, presentation_copy_id, item_slide_copy_id, index,
                items_list[index]
            )
    print(emoji.emojize(f"  :check_mark_button: {len(number_of_slides_created)} slides criados com sucesso."))


def create_copy_of_presentation(drive_service, slide_template_id: str, azure_object):
    body = {
        "name": f"Mercado Topográfico - Sprint {azure_object['sprint']}"
    }
    response = drive_service.files().copy(fileId=slide_template_id, body=body).execute()
    new_presentation_id = response.get("id")
    print(emoji.emojize(f"  :check_mark_button: Apresentação criada com id {new_presentation_id}"))
    return new_presentation_id


def create_copy_of_item_slide_original(slide_service, presentation_id: str, item_slide_original_id: str):
    body = {
        'requests': [
            {
                'duplicateObject': {
                    'objectId': item_slide_original_id
                }
            }
        ]
    }
    response = slide_service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
    new_item_slide_id = response["replies"][0]["duplicateObject"]["objectId"]
    print(emoji.emojize(f"  :check_mark_button: Criado uma cópia do slide original com id {new_item_slide_id}"))
    return new_item_slide_id


def replace_text_globally(slide_service, presentation_id: str, old_text: str, new_text: str):
    body = {
        "requests": [
            {
                "replaceAllText": {
                    "containsText": {"text": old_text},
                    "replaceText": new_text,
                }
            }
        ]
    }
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id, body=body
    ).execute()
    print(emoji.emojize(f"  :check_mark_button: Texto alterado de '{old_text}' para '{new_text}'"))


def replace_text_in_each_column_of_the_item_slide_copy(
        slide_service, presentation_id: str, slide_id: int, index: int, azure_work_items):
    # tasks_text = ""
    # for task in azure_work_items["tasks"]:
    #     tasks_text += f"{task['task_title']}\n"
    tasks_text = ""
    for i, task in enumerate(azure_work_items["tasks"]):
        tasks_text += f"{task['task_title']}"
        if i < len(azure_work_items["tasks"]) - 1:  # Verifique se não é o último item
            tasks_text += "\n"

    # Intervado de 1 a 3 sempre
    index_range: str = str(1 + (index % 3))

    body = {
        "requests": [
            {
                "replaceAllText": {
                    "containsText": {"text": "{{type_" + index_range + "}}"},
                    "replaceText": azure_work_items["type"],
                    "pageObjectIds": [
                        slide_id
                    ]
                }
            },
            {
                "replaceAllText": {
                    "containsText": {"text": "{{id_" + index_range + "}}"},
                    "replaceText": str(azure_work_items["id"]),
                    "pageObjectIds": [
                        slide_id
                    ]
                }
            },
            {
                "replaceAllText": {
                    "containsText": {"text": "{{title_" + index_range + "}}"},
                    "replaceText": azure_work_items["title"],
                    "pageObjectIds": [
                        slide_id
                    ]
                }
            },
            {
                "replaceAllText": {
                    "containsText": {"text": "{{task_" + index_range + "}}"},
                    "replaceText": tasks_text,
                    "pageObjectIds": [
                        slide_id
                    ]
                }
            }
        ]
    }
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id, body=body
    ).execute()
    print(emoji.emojize(f"      :check_mark_button: Texto adicionado na Coluna {index_range} do Slide id {slide_id}"))


def clear_unused_variables_globally(slide_service, presentation_id, items_per_slide):
    for index in range(items_per_slide):
        index_range: str = str(index + 1)
        body = {
            "requests": [
                {
                    "replaceAllText": {
                        "containsText": {"text": "{{type_" + index_range + "}}"},
                        "replaceText": ""
                    }
                },
                {
                    "replaceAllText": {
                        "containsText": {"text": "{{id_" + index_range + "}}"},
                        "replaceText": ""
                    }
                },
                {
                    "replaceAllText": {
                        "containsText": {"text": "{{title_" + index_range + "}}"},
                        "replaceText": ""
                    }
                },
                {
                    "replaceAllText": {
                        "containsText": {"text": "{{task_" + index_range + "}}"},
                        "replaceText": ""
                    }
                }
            ]
        }
        slide_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body
        ).execute()


def delete_slide(slide_service, presentation_id: str, slide_id: str):
    body = {
        "requests": [
            {
                "deleteObject": {
                    "objectId": slide_id
                }
            }
        ]
    }
    slide_service.presentations().batchUpdate(
        presentationId=presentation_id, body=body
    ).execute()
    print(emoji.emojize(f"  :check_mark_button: Slide deletado com id {slide_id}"))


if __name__ == "__main__":
    main()
