import json
import os
from pprint import pprint

import requests

# with open("../mongo/snapshots/users_latest.json", "r") as f:
#     data = json.load(f)
#
# print(data[0])

PLAUSIBLE_API_KEY = os.getenv("PLAUSIBLE_API_KEY")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {PLAUSIBLE_API_KEY}"}


def query_v1_api(endpoint, period, prop, filters):
    url = f"https://analytics.aitutor.live/api/v1/stats/{endpoint}?period={period}&site_id=aitutor.live&property=event:{prop}&filters=event:{filters[0]}%3D%3D{filters[1]}"

    r = requests.get(url, headers=headers)

    return r.json()


# url = "https://analytics.aitutor.live/api/v1/query"
# url = "https://analytics.aitutor.live/api/v2/query"
#
#
# data = {
#     "site_id": "aitutor.live",
#     "metrics": ["events"],
#     "dimensions": [
#         # "time:day",
#         # "event:goal",
#         # "event:page",
#         "event:props:canvas_id",
#         "event:props:length",
#     ],
#     "date_range": "month",
# }
#
#
# r = requests.post(url, json=data, headers=headers)
#
# # pprint(r.json()["query"])
# pprint(r.json()["results"])
#
# url2 = "https://analytics.aitutor.live/api/v1/stats/breakdown?site_id=aitutor.live&property=event:props:canvas_id"
url = "https://analytics.aitutor.live/api/v1/stats/breakdown?period=30d&site_id=aitutor.live&property=event:props:canvas_id"
r = requests.get(url, headers={"Authorization": f"Bearer {PLAUSIBLE_API_KEY}"})
#
#
pprint(r.json()["results"])
results = r.json()["results"]

canvas_ids = [i.get("canvas_id") for i in results]

for id in canvas_ids:
    print(id)
    pprint(query_v1_api("timeseries", "30d", "props:length", ["props:canvas_id", id]))
    print()
