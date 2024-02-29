from azure.devops.connection import Connection
from azure.devops.v7_1.work_item_tracking import Wiql, WorkItemTrackingClient
from msrest.authentication import BasicAuthentication
import pprint
from dotenv import load_dotenv
import os

load_dotenv()
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
organization_url = os.getenv("ORGANIZATION_URL")

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# WORK ITEMS LIST
sprint: str = "44"
work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
sql = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
                 f"FROM WorkItems "
                 f"WHERE ([System.WorkItemType] = 'Product Backlog Item' OR [System.WorkItemType] = 'Bug') "
                 f"AND [System.IterationPath] = 'Mercado Topográfico\\Sprint {sprint}'")
work_item_list = work_item_tracking_client.query_by_wiql(sql)

work_item_ids: list = []
if work_item_list.work_items is not None:
    for work_item in work_item_list.work_items:
        work_item_ids.append(work_item.id)

pprint.pprint(work_item_ids)

# GET WORK ITEM DETAILS
for work_item_id in work_item_ids:
    work_item = work_item_tracking_client.get_work_item(id=work_item_id)
    pprint.pprint(
        f"ID: {work_item.id}, Type: {work_item.fields['System.WorkItemType']}, Title: {work_item.fields['System.Title']}")


# GET TASKS FROM WORK ITEM
work_item_parent = 24984
query_for_tasks = Wiql(query=f"SELECT [System.Id] "
                             f"FROM WorkItems "
                             f"WHERE [System.WorkItemType] = 'Task' "
                             f"AND ([System.State] = 'Done' OR [System.State] = 'In Progress') "
                             f"AND [System.Parent] = {work_item_parent}")
task_list = work_item_tracking_client.query_by_wiql(query_for_tasks)

task_ids: list = []
if task_list.work_items is not None:
    for task in task_list.work_items:
        task_ids.append(task.id)
pprint.pprint(f"lista de tasks {task_ids}")

# USER PROJECT LIST
# core_client = connection.clients.get_core_client()
# get_projects_response = core_client.get_projects()
# index = 0
# while get_projects_response is not None:
#     for project in get_projects_response:
#         pprint.pprint("[" + str(index) + "] " + project.name)
#         index += 1
#     break
