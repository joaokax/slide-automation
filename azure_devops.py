from azure.devops.connection import Connection
from azure.devops.v7_1.work_item_tracking import Wiql, WorkItemTrackingClient
from msrest.authentication import BasicAuthentication
import pprint
from dotenv import load_dotenv
import os
import json

load_dotenv()
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
organization_url = os.getenv("ORGANIZATION_URL")

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# WORK ITEMS LIST
project_name = "Mercado Topográfico"
sprint: str = "44"
work_item_tracking_client = WorkItemTrackingClient(organization_url, credentials)
sql = Wiql(query=f"SELECT [System.Id], [System.Title], [System.State] "
                 f"FROM WorkItems "
                 f"WHERE ([System.WorkItemType] = 'Product Backlog Item' OR [System.WorkItemType] = 'Bug') "
                 f"AND [System.IterationPath] = 'Mercado Topográfico\\Sprint {sprint}'")
work_item_list = work_item_tracking_client.query_by_wiql(sql)

json_data = {"project": project_name, "sprint": sprint, "work_items": []}

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

        json_data["work_items"].append(work_item_dict)

formatted_json = json.dumps(json_data, indent=4)
print(formatted_json)

