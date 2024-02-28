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
        # pprint.pprint(work_item.id)
    # break
pprint.pprint(work_item_ids)

# USER PROJECT LIST
# core_client = connection.clients.get_core_client()
# get_projects_response = core_client.get_projects()
# index = 0
# while get_projects_response is not None:
#     for project in get_projects_response:
#         pprint.pprint("[" + str(index) + "] " + project.name)
#         index += 1
#     break
