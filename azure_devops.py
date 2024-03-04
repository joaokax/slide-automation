import emoji
from azure.devops.connection import Connection
from azure.devops.v7_1.work import TeamContext
from azure.devops.v7_1.work_item_tracking import Wiql, WorkItemTrackingClient
from msrest.authentication import BasicAuthentication
from dotenv import load_dotenv
import os
import re

load_dotenv()


def get_azure_work_items():
    personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
    organization_url = os.getenv("ORGANIZATION_URL")
    project_name = os.getenv("PROJECT_NAME")

    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    core_client = connection.clients.get_core_client()

    project_id = get_project_id(core_client)

    team_id = get_team_id(core_client, project_id)

    current_sprint_path, current_sprint_number = get_current_sprint(connection, project_id, team_id)

    azure_object = get_azure_object(organization_url, credentials, project_name, current_sprint_path,
                                    current_sprint_number)

    return azure_object


def get_project_id(core_client):
    project_name = os.getenv("PROJECT_NAME")
    project_id = None
    get_projects_response = core_client.get_projects()
    for project in get_projects_response:
        if project.name == project_name:
            project_id = project.id
            print(emoji.emojize("  :check_mark_button: Nome do projeto"))
    return project_id


def get_team_id(core_client, project_id):
    team_name = os.getenv("TEAM_NAME")
    team_id = None
    get_teams_response = core_client.get_teams(project_id=project_id)
    for team in get_teams_response:
        if team.name == team_name:
            team_id = team.id
            print(emoji.emojize("  :check_mark_button: Informações da equipe"))
    return team_id


def get_current_sprint(connection, project_id, team_id):
    work_client = connection.clients.get_work_client()
    team_context = TeamContext(project_id=project_id, team_id=team_id)
    current_sprint = work_client.get_team_iterations(team_context=team_context, timeframe="Current")
    current_sprint_path = current_sprint[0].path
    current_sprint_path = current_sprint_path.replace('\\', '\\\\')
    current_sprint_number = re.findall(r"\d+", current_sprint[0].name)[0]
    print(emoji.emojize("  :check_mark_button: Dados da sprint atual"))
    return current_sprint_path, current_sprint_number


def get_azure_object(organization_url, credentials, project_name, current_sprint_path, current_sprint_number):
    azure_object = {
        "project": project_name,
        "sprint": current_sprint_number,
        "work_items": [],
        "next_sprint": []
    }

    print(emoji.emojize(":blue_circle: Obtendo work items da sprint atual"))
    process_work_items_for_sprint(
        organization_url, credentials, current_sprint_path, azure_object['work_items'], is_current_sprint=True)

    print(emoji.emojize(":blue_circle: Obtendo work items da próxima sprint"))
    process_work_items_for_sprint(
        organization_url, credentials, current_sprint_path, azure_object['next_sprint'])

    return azure_object


def process_work_items_for_sprint(
        organization_url, credentials, current_sprint_path, sprint_list, is_current_sprint=False):
    if is_current_sprint:
        state_condition = "!= 'New'"
        state_condition_task = "IN ('Done', 'In Progress')"
    else:
        state_condition = "!= 'Done'"
        state_condition_task = "!= 'Done'"

    # Consulta para retornar work items e suas tasks
    work_item_query = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
                                 f"FROM WorkItems "
                                 f"WHERE [System.WorkItemType] IN ('Product Backlog Item', 'Bug') "
                                 f"AND [System.State] {state_condition} "
                                 f"AND [System.IterationPath] = '{current_sprint_path}'")

    work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
    work_item_list = work_item_tracking_client.query_by_wiql(work_item_query)

    if work_item_list.work_items is not None:
        # work_item_list só traz os ids e as urls do work items, nada mais
        for item in work_item_list.work_items:
            # Requisição para trazer mais informações sobre o work item
            work_item = work_item_tracking_client.get_work_item(id=item.id)
            work_item_type = work_item.fields['System.WorkItemType']
            work_item_type = "PBI" if work_item_type == "Product Backlog Item" else work_item_type
            work_item_dict = {
                "id": work_item.id,
                "type": work_item_type,
                "state": work_item.fields['System.State'],
                "title": work_item.fields['System.Title'],
                "tasks": []
            }

            # Consulta para trazer somente Tasks
            task_query = Wiql(query=f"SELECT [System.Id], [System.Title], [System.WorkItemType] "
                                    f"FROM WorkItems "
                                    f"WHERE [System.WorkItemType] IN ('Task', 'Impediment') "
                                    f"AND [System.State] {state_condition_task} "
                                    f"AND [System.Parent] = {work_item.id} "
                                    f"AND [System.IterationPath] = '{current_sprint_path}'")
            task_list = work_item_tracking_client.query_by_wiql(wiql=task_query)

            if task_list.work_items is not None:
                # task_list só traz os ids e as urls das tasks, nada mais
                for task_item in task_list.work_items:
                    # Requisição para trazer mais informações sobre as tasks
                    task = work_item_tracking_client.get_work_item(id=task_item.id)
                    task_dict = {
                        "task_id": task.id,
                        "task_type": task.fields['System.WorkItemType'],
                        "task_state": task.fields['System.State'],
                        "task_title": task.fields['System.Title']
                    }
                    work_item_dict["tasks"].append(task_dict)

            sprint_list.append(work_item_dict)


if __name__ == "__main__":
    get_azure_work_items()
