from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint
from dotenv import load_dotenv
import os

load_dotenv()
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")
organization_url = os.getenv("ORGANIZATION_URL")

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

core_client = connection.clients.get_core_client()

get_projects_response = core_client.get_projects()
index = 0
while get_projects_response is not None:
    for project in get_projects_response:
        pprint.pprint("[" + str(index) + "] " + project.name)
        index += 1
    break
