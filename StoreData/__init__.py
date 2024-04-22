import logging
import os
from datetime import datetime
import json

import azure.functions as func

from azure.data.tables import (TableServiceClient, UpdateMode)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]

    req_body = req.get_json()

    updated_entity = {
        "RowKey": req_body.get('storyID'),
        "PartitionKey": "Bunkers",
        "imgURL": req_body.get("imgURL"),
        "storyImages": json.dumps(req_body.get("storyImages")),
        "messageHistory": json.dumps(req_body.get("messageHistory")),
        "messages": json.dumps(req_body.get("messages")),
        "possibleActions": json.dumps(req_body.get("possibleActions")),
    }

    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    table_client = table_service_client.get_table_client(table_name="Stories")

    logging.info(req_body)
    
    entity = table_client.upsert_entity(mode=UpdateMode.MERGE, entity=updated_entity)

    logging.info("Data saved to Surveys Table")

    return func.HttpResponse(
        "Data saved to Surveys Table",
        status_code=200
    )
