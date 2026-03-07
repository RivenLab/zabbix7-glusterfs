#!/usr/bin/python3
import json
import subprocess
import sys

gstatus_output = subprocess.check_output("gstatus -a -o json", shell=True).decode()
gluster_info = json.loads(gstatus_output)

data = gluster_info.get("data", {})
volume_list = data.get("volume_summary", [])

def find_volume(name):
    for volume in volume_list:
        if volume.get("name") == name:
            return volume
    return None

def get_cluster_value(key):
    if key == "status":
        return data.get("cluster_status", 0)
    if key == "nodes_active":
        return data.get("nodes_active", 0)
    if key == "node_count":
        return data.get("node_count", 0)
    if key == "volume_count":
        return data.get("volume_count", 0)
    if key == "snapshot_count":
        return sum(v.get("snapshot_count", 0) for v in volume_list)
    if key == "sh_enabled":
        return 0
    if key == "sh_active":
        return 0
    if key == "used_capacity":
        return sum(v.get("size_used", 0) for v in volume_list)
    if key == "usable_capacity":
        return sum(v.get("size_total", 0) for v in volume_list)
    if key == "raw_capacity":
        return sum(v.get("size_total", 0) for v in volume_list)
    return 0

def get_volume_value(volume, key):
    if key == "state":
        return volume.get("health", "down")
    if key == "used_capacity":
        return volume.get("size_used", 0)
    if key == "usable_capacity":
        return volume.get("size_total", 0)
    if key == "snapshot_count":
        return volume.get("snapshot_count", 0)
    return volume.get(key, 0)

nargs = len(sys.argv)

if nargs == 1:
    discovered = []
    for volume in volume_list:
        if volume.get("name"):
            discovered.append({"{#VOLUME_NAME}": volume["name"]})
    print(json.dumps({"data": discovered}))

elif nargs == 2:
    print(get_cluster_value(sys.argv[1]))

elif nargs == 3:
    field = sys.argv[1]
    volume_name = sys.argv[2]
    volume = find_volume(volume_name)
    if volume:
        print(get_volume_value(volume, field))
    else:
        print("down" if field == "state" else 0)

else:
    print("Wrong arguments")
