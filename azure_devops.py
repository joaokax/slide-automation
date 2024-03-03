import re

from azure.devops.connection import Connection
from azure.devops.v7_0.work.work_client import Client, WorkClient
from azure.devops.v7_1.work import TeamContext
from azure.devops.v7_1.work_item_tracking import Wiql, WorkItemTrackingClient
from msrest.authentication import BasicAuthentication
import pprint
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()


# personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
# organization_url = os.getenv("ORGANIZATION_URL")
#
# credentials = BasicAuthentication('', personal_access_token)
# connection = Connection(base_url=organization_url, creds=credentials)

# TODO VERIFICAR SE É POSSÍVEL TRAZER A ITERAÇÃO MAIS RECENTE
# TODO INTEGRAR A RESPOSTA DO AZURE COM A APRESENTAÇÃO
# TODO MONTAR O OBJETO next_sprint com os work items em progresso e os que estão em to do
# WORK ITEMS LIST
# project_name = "Mercado Topográfico"
# sprint: str = "44"
# work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
# sql = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
#                  f"FROM WorkItems "
#                  f"WHERE ([System.WorkItemType] = 'Product Backlog Item' OR [System.WorkItemType] = 'Bug') "
#                  f"AND [System.IterationPath] = 'Mercado Topográfico\\Sprint {sprint}'")
# work_item_list = work_item_tracking_client.query_by_wiql(sql)
#
# azure_object = {
#     "project": project_name,
#     "sprint": sprint,
#     "work_items": [],
#     "next_sprint": []
# }


def get_azure_work_items():
    personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
    organization_url = os.getenv("ORGANIZATION_URL")

    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    # FUNCIONANDO
    core_client = connection.clients.get_core_client()

    project_name = os.getenv("PROJECT_NAME")
    project_id = None
    get_projects_response = core_client.get_projects()
    for project in get_projects_response:
        if project.name == project_name:
            project_id = project.id

    team_name = os.getenv("TEAM_NAME")
    team_id = None
    get_teams_response = core_client.get_teams(project_id=project_id)
    for team in get_teams_response:
        if team.name == team_name:
            team_id = team.id

    team_context = TeamContext(project_id=project_id, team_id=team_id)
    work_client = connection.clients.get_work_client()
    current_sprint = work_client.get_team_iterations(team_context=team_context, timeframe="Current")
    current_sprint_path = current_sprint[0].path
    current_sprint_number = re.findall(r"\d+", current_sprint[0].name)[0]

    azure_object = {
        "project": project_name,
        "sprint": current_sprint_number,
        "work_items": [],
        "next_sprint": []
    }

    # Process work items
    # if work_item_list.work_items is not None:
    #
    #     work_item_ids: list = []
    #
    #     for work_item in work_item_list.work_items:
    #         work_item_ids.append(work_item.id)
    #
    #     for work_item_id in work_item_ids:
    #         work_item = work_item_tracking_client.get_work_item(id=work_item_id)
    #         work_item_dict = {
    #             "id": work_item.id,
    #             "type": work_item.fields['System.WorkItemType'],
    #             "state": work_item.fields['System.State'],
    #             "title": work_item.fields['System.Title'],
    #             "tasks": []
    #         }
    #
    #         query_for_tasks = Wiql(query=f"SELECT [System.Id], [System.Title], [System.WorkItemType] "
    #                                      f"FROM WorkItems "
    #                                      f"WHERE [System.WorkItemType] = 'Task' "
    #                                      f"AND ([System.State] = 'Done' OR [System.State] = 'In Progress') "
    #                                      f"AND [System.Parent] = {work_item.id} "
    #                                      f"AND [System.IterationPath] = {current_sprint_path}")
    #         task_list = work_item_tracking_client.query_by_wiql(wiql=query_for_tasks)
    #
    #         task_ids: list = []
    #         if task_list.work_items is not None:
    #             for task in task_list.work_items:
    #                 task_ids.append(task.id)
    #
    #             for task_id in task_ids:
    #                 task = work_item_tracking_client.get_work_item(id=task_id)
    #                 task_dict = {
    #                     "task_id": task.id,
    #                     "task_type": task.fields['System.WorkItemType'],
    #                     "task_state": task.fields['System.State'],
    #                     "task_title": task.fields['System.Title']
    #                 }
    #                 work_item_dict["tasks"].append(task_dict)
    #
    #         azure_object["work_items"].append(work_item_dict)
    #
    # formatted_json = json.dumps(azure_object, indent=4)
    # print(formatted_json)


# def get_sprint_work_items():
#     work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
#     sql = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
#                      f"FROM WorkItems "
#                      f"WHERE ([System.WorkItemType] = 'Product Backlog Item' OR [System.WorkItemType] = 'Bug') "
#                      f"AND [System.IterationPath] = 'Mercado Topográfico\\Sprint {sprint}'")
#     work_item_list = work_item_tracking_client.query_by_wiql(sql)

def process_work_items(organization_url, credentials, current_sprint_path, project_name, current_sprint_number):
    azure_object = {
        "project": project_name,
        "sprint": current_sprint_number,
        "work_items": [],
        "next_sprint": []
    }

    # Consulta e retorna todos os work items da sprint atual, seja PBIs ou Bugs
    work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
    work_item_query = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
                                 f"FROM WorkItems "
                                 f"WHERE [System.WorkItemType] IN ('Product Backlog Item', 'Bug') "
                                 f"AND NOT [System.State] = 'New' "
                                 f"AND [System.IterationPath] = {current_sprint_path}")
    work_item_list = work_item_tracking_client.query_by_wiql(work_item_query)

    if work_item_list.work_items is not None:
        # work_item_list só traz os ids e as urls do work items, nada mais
        for item in work_item_list.work_items:
            # Requisição para trazer mais informações sobre o work item
            work_item = work_item_tracking_client.get_work_item(id=item.id)
            work_item_dict = {
                "id": work_item.id,
                "type": work_item.fields['System.WorkItemType'],
                "state": work_item.fields['System.State'],
                "title": work_item.fields['System.Title'],
                "tasks": []
            }

            # Consulta para trazer somente Tasks
            task_query = Wiql(query=f"SELECT [System.Id], [System.Title], [System.WorkItemType] "
                                    f"FROM WorkItems "
                                    f"WHERE [System.WorkItemType] IN ('Task', 'Impediment') "
                                    f"WHERE [System.State] IN ('Done', 'In Progress') "
                                    f"AND [System.Parent] = {work_item.id} "
                                    f"AND [System.IterationPath] = {current_sprint_path}")
            task_list = work_item_tracking_client.query_by_wiql(wiql=task_query)

            if task_list.work_items is not None:
                for task_item in task_list.work_items:
                    task = work_item_tracking_client.get_work_item(id=task_item.id)
                    task_dict = {
                        "task_id": task.id,
                        "task_type": task.fields['System.WorkItemType'],
                        "task_state": task.fields['System.State'],
                        "task_title": task.task_title
                    }
                    work_item_dict["tasks"].append(task_dict)

            azure_object["work_items"].append(work_item_dict)

    # Consulta e retorna todos os work items para a próxima sprint, seja PBIs ou Bugs
    work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
    work_item_query = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
                                 f"FROM WorkItems "
                                 f"WHERE [System.WorkItemType] IN ('Product Backlog Item', 'Bug') "
                                 f"AND NOT [System.State] = 'Done' "
                                 f"AND [System.IterationPath] = {current_sprint_path}")
    work_item_list = work_item_tracking_client.query_by_wiql(work_item_query)

    if work_item_list.work_items is not None:
        # work_item_list só traz os ids e as urls do work items, nada mais
        for item in work_item_list.work_items:
            # Requisição para trazer mais informações sobre o work item
            work_item = work_item_tracking_client.get_work_item(id=item.id)
            work_item_dict = {
                "id": work_item.id,
                "type": work_item.fields['System.WorkItemType'],
                "state": work_item.fields['System.State'],
                "title": work_item.fields['System.Title'],
                "tasks": []
            }

            # Consulta para trazer somente Tasks
            task_query = Wiql(query=f"SELECT [System.Id], [System.Title], [System.WorkItemType] "
                                    f"FROM WorkItems "
                                    f"WHERE [System.WorkItemType] IN ('Task', 'Impediment') "
                                    f"AND NOT [System.State] = 'Done' "
                                    f"AND [System.Parent] = {work_item.id} "
                                    f"AND [System.IterationPath] = {current_sprint_path}")
            task_list = work_item_tracking_client.query_by_wiql(wiql=task_query)

            if task_list.work_items is not None:
                for task_item in task_list.work_items:
                    task = work_item_tracking_client.get_work_item(id=task_item.id)
                    task_dict = {
                        "task_id": task.id,
                        "task_type": task.fields['System.WorkItemType'],
                        "task_state": task.fields['System.State'],
                        "task_title": task.task_title
                    }
                    work_item_dict["tasks"].append(task_dict)

            azure_object["next_sprint"].append(work_item_dict)



if __name__ == "__main__":
    get_azure_work_items()
