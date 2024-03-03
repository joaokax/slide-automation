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

    # Consulta e retorna os work items da sprint atual classificados como PBIs ou Bugs
    work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
    sql = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
                     f"FROM WorkItems "
                     f"WHERE ([System.WorkItemType] = 'Product Backlog Item' OR [System.WorkItemType] = 'Bug') "
                     f"AND [System.IterationPath] = {current_sprint_path}")
    work_item_list = work_item_tracking_client.query_by_wiql(sql)

    azure_object = {
        "project": project_name,
        "sprint": current_sprint_number,
        "work_items": [],
        "next_sprint": []
    }

    # Process work items
    if work_item_list.work_items is not None:

        work_item_ids: list = []

        for work_item in work_item_list.work_items:
            work_item_ids.append(work_item.id)

        for work_item_id in work_item_ids:
            work_item = work_item_tracking_client.get_work_item(id=work_item_id)
            work_item_dict = {
                "id": work_item.id,
                "type": work_item.fields['System.WorkItemType'],
                "state": work_item.fields['System.State'],
                "title": work_item.fields['System.Title'],
                "tasks": []
            }

            query_for_tasks = Wiql(query=f"SELECT [System.Id], [System.Title], [System.WorkItemType] "
                                         f"FROM WorkItems "
                                         f"WHERE [System.WorkItemType] = 'Task' "
                                         f"AND ([System.State] = 'Done' OR [System.State] = 'In Progress') "
                                         f"AND [System.Parent] = {work_item.id} "
                                         f"AND [System.IterationPath] = 'Mercado Topográfico\\Sprint {sprint}'")
            task_list = work_item_tracking_client.query_by_wiql(wiql=query_for_tasks)

            task_ids: list = []
            if task_list.work_items is not None:
                for task in task_list.work_items:
                    task_ids.append(task.id)

                for task_id in task_ids:
                    task = work_item_tracking_client.get_work_item(id=task_id)
                    task_dict = {
                        "task_id": task.id,
                        "task_type": task.fields['System.WorkItemType'],
                        "task_state": task.fields['System.State'],
                        "task_title": task.fields['System.Title']
                    }
                    work_item_dict["tasks"].append(task_dict)

            azure_object["work_items"].append(work_item_dict)

    formatted_json = json.dumps(azure_object, indent=4)
    print(formatted_json)


# def get_sprint_work_items():
#     work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
#     sql = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
#                      f"FROM WorkItems "
#                      f"WHERE ([System.WorkItemType] = 'Product Backlog Item' OR [System.WorkItemType] = 'Bug') "
#                      f"AND [System.IterationPath] = 'Mercado Topográfico\\Sprint {sprint}'")
#     work_item_list = work_item_tracking_client.query_by_wiql(sql)


if __name__ == "__main__":
    get_azure_work_items()
