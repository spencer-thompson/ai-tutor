import json

with open("../mongo/snapshots/users_latest.json", "r") as f:
    data = json.load(f)

print(data[0])
