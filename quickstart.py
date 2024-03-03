import json
import os.path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

azure_object = {
    "project": "My Project",
    "sprint": "44",
    "work_items": [
        {
            "id": 18062,
            "type": "Product Backlog Item",
            "state": "Desenvolvendo",
            "title": "Infra: CI/CD",
            "tasks": [
                {
                    "task_id": 24961,
                    "task_type": "Task",
                    "task_state": "In Progress",
                    "task_title": "Actions AWS"
                },
                {
                    "task_id": 24962,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Script de teste de conex\u00e3o"
                }
            ]
        },
        {
            "id": 23521,
            "type": "Product Backlog Item",
            "state": "Done",
            "title": "Informa\u00e7\u00e3o de novas formas de pagamento",
            "tasks": [
                {
                    "task_id": 24926,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Deploy - Produ\u00e7\u00e3o "
                }
            ]
        },
        {
            "id": 24190,
            "type": "Product Backlog Item",
            "state": "Done",
            "title": "Adequa\u00e7\u00f5es Whitelabel - Pagamento",
            "tasks": [
                {
                    "task_id": 24907,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Homologa\u00e7\u00e3o"
                },
                {
                    "task_id": 25012,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Deploy em produ\u00e7\u00e3o"
                },
                {
                    "task_id": 25013,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Merge e altera\u00e7\u00f5es necess\u00e1rias"
                }
            ]
        },
        {
            "id": 24231,
            "type": "Product Backlog Item",
            "state": "Done",
            "title": "Tela de informa\u00e7\u00f5es profissionais (Data Professional)",
            "tasks": [
                {
                    "task_id": 24680,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Tela Informa\u00e7\u00f5es Profissionais refinada"
                }
            ]
        },
        {
            "id": 24426,
            "type": "Product Backlog Item",
            "state": "Done",
            "title": "SSO - Login Facebook",
            "tasks": [
                {
                    "task_id": 24872,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Homologa\u00e7\u00e3o"
                },
                {
                    "task_id": 24972,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Produ\u00e7\u00e3o"
                }
            ]
        },
        {
            "id": 24581,
            "type": "Product Backlog Item",
            "state": "New",
            "title": "Adequa\u00e7\u00f5es whitelabel - cadastro usu\u00e1rio",
            "tasks": [
                {
                    "task_id": 24735,
                    "task_type": "Task",
                    "task_state": "In Progress",
                    "task_title": "Adequa\u00e7\u00e3o do cadastro (tela e m\u00e9todo)"
                }
            ]
        },
        {
            "id": 24860,
            "type": "Product Backlog Item",
            "state": "Desenvolvendo",
            "title": "Tradu\u00e7\u00e3o de Rota(URL)",
            "tasks": [
                {
                    "task_id": 24864,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Traduzindo rotas"
                },
                {
                    "task_id": 25011,
                    "task_type": "Task",
                    "task_state": "In Progress",
                    "task_title": "Buscando e alterando URL/rotas hard coded sem tradu\u00e7\u00e3o"
                }
            ]
        },
        {
            "id": 24963,
            "type": "Bug",
            "state": "Done",
            "title": "Fix - Cupom de plano",
            "tasks": [
                {
                    "task_id": 24964,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Investiga\u00e7\u00e3o"
                },
                {
                    "task_id": 24965,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Implementa\u00e7\u00e3o da solu\u00e7\u00e3o"
                },
                {
                    "task_id": 24966,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Deploy"
                }
            ]
        },
        {
            "id": 24970,
            "type": "Product Backlog Item",
            "state": "New",
            "title": "Adequa\u00e7\u00f5es whitelabel - cadastro de produto",
            "tasks": []
        },
        {
            "id": 24973,
            "type": "Product Backlog Item",
            "state": "Desenvolvendo",
            "title": "SEO - Performance de carregamento das p\u00e1ginas",
            "tasks": [
                {
                    "task_id": 24974,
                    "task_type": "Task",
                    "task_state": "In Progress",
                    "task_title": "Identifica\u00e7\u00e3o e listagem de melhorias de performance"
                }
            ]
        },
        {
            "id": 24984,
            "type": "Product Backlog Item",
            "state": "Desenvolvendo",
            "title": "[SEO] Corre\u00e7\u00f5es H1, Meta Descriptions Duplicados",
            "tasks": [
                {
                    "task_id": 25025,
                    "task_type": "Task",
                    "task_state": "In Progress",
                    "task_title": "Adi\u00e7\u00e3o das tags H1"
                },
                {
                    "task_id": 25026,
                    "task_type": "Task",
                    "task_state": "In Progress",
                    "task_title": "Corre\u00e7\u00e3o das meta descriptions"
                }
            ]
        },
        {
            "id": 25015,
            "type": "Bug",
            "state": "Done",
            "title": "Fix: Erro ao realizar compra sem telefone ",
            "tasks": [
                {
                    "task_id": 25016,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Investiga\u00e7\u00e3o"
                },
                {
                    "task_id": 25017,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Implementa\u00e7\u00e3o da solu\u00e7\u00e3o"
                },
                {
                    "task_id": 25018,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Realizando testes"
                },
                {
                    "task_id": 25019,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Deploy em produ\u00e7\u00e3o"
                }
            ]
        }
    ],
    "next_sprint": [
        {
            "id": 18062,
            "type": "Product Backlog Item",
            "state": "Desenvolvendo",
            "title": "Tarefa 1",
            "tasks": [
                {
                    "task_id": 24961,
                    "task_type": "Task",
                    "task_state": "In Progress",
                    "task_title": "Actions AWS"
                },
                {
                    "task_id": 24962,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Script de teste de conex\u00e3o"
                }
            ]
        },
        {
            "id": 23521,
            "type": "Product Backlog Item",
            "state": "Done",
            "title": "Tarefa 2",
            "tasks": [
                {
                    "task_id": 24926,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Deploy - Produ\u00e7\u00e3o "
                }
            ]
        },
        {
            "id": 24190,
            "type": "Product Backlog Item",
            "state": "Done",
            "title": "Tarefa 3",
            "tasks": [
                {
                    "task_id": 24907,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Homologa\u00e7\u00e3o"
                },
                {
                    "task_id": 25012,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Deploy em produ\u00e7\u00e3o"
                },
                {
                    "task_id": 25013,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Merge e altera\u00e7\u00f5es necess\u00e1rias"
                }
            ]
        },
        {
            "id": 24231,
            "type": "Product Backlog Item",
            "state": "Done",
            "title": "Tarefa 4",
            "tasks": [
                {
                    "task_id": 24680,
                    "task_type": "Task",
                    "task_state": "Done",
                    "task_title": "Tela Informa\u00e7\u00f5es Profissionais refinada"
                }
            ]
        }
    ]
}

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

        # # Criar uma cópia da apresentação
        # copy_title = 'Cópia da Apresentação Mercado - 6'
        # copy_body = {'name': copy_title}
        # copied_presentation = (
        #     drive_service.files().copy(fileId=TEMPLATE_ID, body=copy_body).execute()
        # )
        # presentation_copy_id = copied_presentation.get("id")
        # print(f'A apresentação foi copiada, ID: {presentation_copy_id}')

        # TODO SUBSTITUIR AS CHAVES DESSA CÓPIA. EX: {{SPRINT}} PARA NÚMERO DA SPRINT
        # texts_to_replace = ["{{sprint}}", "{{type_1}}", "{{id_1}}"]
        # replacement_texts = ["Sprint 44", "PB1", "123456"]
        # presentation_copy_id = "1qdnAr293rt7cKSO7gUBMnQVUXOVM6lcDHEPQTYQuwB0"
        #
        # for text, replacement in zip(texts_to_replace, replacement_texts):
        #     body = {
        #         "requests": [
        #             {
        #                 "replaceAllText": {
        #                     "containsText": {"text": text},
        #                     "replaceText": replacement,
        #                 }
        #             }
        #         ]
        #     }
        #     slide_service.presentations().batchUpdate(
        #         presentationId=presentation_copy_id, body=body
        #     ).execute()
        #
        # print("Os textos foram substituidos com sucesso!")

        # TODO CLONAR SLIDES DA APRESENTAÇÃO CLONE
        # presentation_copy_id = '1qdnAr293rt7cKSO7gUBMnQVUXOVM6lcDHEPQTYQuwB0'
        # copied_presentation = slide_service.presentations().get(presentationId=presentation_copy_id).execute()
        # slide_indices = [2, 4]
        # requests = []
        # for index in slide_indices:
        #     requests.append({
        #         'duplicateObject': {
        #             'objectId': presentation_copy.get('slides')[index]['objectId'],
        #         }
        #     })
        #
        # body = {'requests': requests}
        # slide_service.presentations().batchUpdate(presentationId=presentation_copy_id, body=body).execute()
        # print("Slide 3 e 5 foram copiados com sucesso.")

        # TODO CRIAR A QUANTIDADE DE SLIDES EXATA PARA COMPORTAR O NÚMERO DE WORK ITEMS
        presentation_copy_id = '1qdnAr293rt7cKSO7gUBMnQVUXOVM6lcDHEPQTYQuwB0'
        presentation_copy = slide_service.presentations().get(presentationId=presentation_copy_id).execute()

        next_sprint_number = int(azure_object["sprint"]) + 1
        replace_text_globally(slide_service, presentation_copy_id, "{{sprint}}", azure_object["sprint"])
        replace_text_globally(slide_service, presentation_copy_id, "{{next_s}}", str(next_sprint_number))

        # Posição dos slides que serão clonados
        item_slide_original_index = 2
        item_slide_original_id = presentation_copy.get('slides')[item_slide_original_index]['objectId']

        next_sprint_item_slide = 4
        next_sprint_item_slide_id = presentation_copy.get('slides')[next_sprint_item_slide]['objectId']

        items_per_slide = 3
        number_of_slides = []

        item_slide_copy_id = ""

        for iteration_index, (items_list, initial_slide_id) in enumerate([
            (azure_object["work_items"], item_slide_original_id),
            (azure_object["next_sprint"], next_sprint_item_slide_id)
        ]):
            total_list_items = len(items_list)
            for index in range(total_list_items):
                if index % items_per_slide == 0:
                    number_of_slides.append(index)
                    item_slide_copy_id = create_copy_of_item_slide_original(
                        slide_service, presentation_copy_id, initial_slide_id
                    )
                replace_text_in_each_column_of_the_item_slide_copy(
                    slide_service, presentation_copy_id, item_slide_copy_id, index,
                    items_list[index]
                )

        delete_slide(slide_service, presentation_copy_id, item_slide_original_id)
        delete_slide(slide_service, presentation_copy_id, next_sprint_item_slide_id)
        print(f"{len(number_of_slides)} slides copiados com sucesso.")

        # for index in range(work_items_total):
        #
        #     # Calculo que cria um novo slide a cada 3 work items, a partir do slide original
        #     if index % items_per_slide == 0:
        #         number_of_slides.append(index)
        #
        #         # Cria o novo slide e retorna seu próprio ID
        #         item_slide_copy_id = create_copy_of_item_slide_original(
        #             slide_service, presentation_copy_id, item_slide_original_id)
        #
        #         # Altera os textos em cada coluna desse slide que acabou de ser criado
        #         replace_text_in_each_column_of_the_item_slide_copy(
        #             slide_service, presentation_copy_id, item_slide_copy_id, index,
        #             azure_object["work_items"][index]
        #         )
        #
        #     # Colunas 2 e 3, 4 e 5, etc. Apenas alteram o texto mas não cria outro slide
        #     else:
        #         # for text, replacement in zip(texts_to_replace, replacement_texts):
        #         replace_text_in_each_column_of_the_item_slide_copy(
        #             slide_service, presentation_copy_id, item_slide_copy_id, index,
        #             azure_object["work_items"][index]
        #         )
        #
        # for index in range(next_sprint_work_items_total):
        #
        #     # Calculo que cria um novo slide a cada 3 work items, a partir do slide original
        #     if index % items_per_slide == 0:
        #         number_of_slides.append(index)
        #
        #         # Cria o novo slide e retorna seu próprio ID
        #         item_slide_copy_id = create_copy_of_item_slide_original(
        #             slide_service, presentation_copy_id, next_sprint_item_slide_id)
        #
        #         # Altera os textos em cada coluna desse slide que acabou de ser criado
        #         replace_text_in_each_column_of_the_item_slide_copy(
        #             slide_service, presentation_copy_id, item_slide_copy_id, index,
        #             azure_object["next_sprint"][index]
        #         )
        #
        #     # Colunas 2 e 3, 4 e 5, etc. Apenas alteram o texto mas não cria outro slide
        #     else:
        #         # for text, replacement in zip(texts_to_replace, replacement_texts):
        #         replace_text_in_each_column_of_the_item_slide_copy(
        #             slide_service, presentation_copy_id, item_slide_copy_id, index,
        #             azure_object["next_sprint"][index]
        #         )




    except HttpError as err:
        print(err)


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


def replace_text_in_each_column_of_the_item_slide_copy(
        slide_service, presentation_id: str, slide_id: int, index: int, azure_work_items):

    tasks_text = ""
    for task in azure_work_items["tasks"]:
        tasks_text += f"{task['task_title']}\n"

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


if __name__ == "__main__":
    main()
