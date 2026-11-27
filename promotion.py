# AI assistance: ChatGPT helped implement device detection and Blob output reading.
import heapq
import json
import os

from azure.storage.blob import ContainerClient
from user_agents import parse


def device_fields(header):
    agent = parse(header or "")
    device = "unknown"
    if agent.is_tablet:
        device = "tablet"
    elif agent.is_mobile:
        device = "mobile"
    elif agent.is_pc:
        device = "desktop"

    def family(value):
        return value if value and value != "Other" else "unknown"

    return {"deviceType": device, "browser": family(agent.browser.family),
            "os": family(agent.os.family)}


def recent_results():
    connection = os.environ.get("ANALYTICS_STORAGE_CONNECTION_STRING")
    if not connection:
        raise ValueError("Missing storage setting")
    with ContainerClient.from_connection_string(
        connection, os.environ.get("ANALYTICS_CONTAINER", "promotion")
    ) as container:
        return {
            "traffic": read_rows(container, "traffic", "window_end"),
            "alerts": read_rows(container, "alerts", "alert_time"),
        }


def read_rows(container, prefix, time_field):
    # This dedicated lab container holds only the short demonstration run.
    def records():
        for blob in container.list_blobs(name_starts_with=prefix + "/"):
            data = container.download_blob(blob.name).readall()
            for line in data.decode("utf-8-sig").splitlines():
                if line.strip():
                    yield json.loads(line)
    return heapq.nlargest(30, records(), key=lambda row: row[time_field])
