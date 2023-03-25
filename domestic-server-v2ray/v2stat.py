#! /usr/bin/env python3

# Let's create a script that will store the current usage of v2ray users in a file
# This script will be called by the v2ray service every 5 minutes

import os
import json
import re

server = "127.0.0.1"
port = DOKODEMOPORT
filename = "/srv/v2fly/usage.json"

v2ctl = "/usr/bin/v2ctl"


# Run the v2ctl command to get the current usage of all users
def run_command():
    cmd = f'{v2ctl} api --server={server}:{port} StatsService.QueryStats \'reset: true\''
    print(cmd)
    result = os.popen(cmd).read()
    return result


inbound = {}
outbound = {}
user = {}


# add id and direction to a dictionary
def add_id_direction(id, direction, value, dictionary):
    if id not in dictionary:
        dictionary[id] = {}
    if direction not in dictionary[id]:
        dictionary[id][direction] = 0
    dictionary[id][direction] += int(value)


def add_block(block):
    name = block[0].split(": ")[1].strip('"')
    value = block[1].split(": ")[1] if len(block) > 1 else 0
    name_parts = name.split(">>>")
    id, direction = name_parts[1], name_parts[-1]

    dicts = {"inbound": inbound, "outbound": outbound, "user": user}

    if name_parts[0] in dicts:
        add_id_direction(id, direction, value, dicts[name_parts[0]])
    else:
        print(f"Unknown name: {name}")


# parse the result and store the data in the appropriate list
def parse_result(result):
    for block in re.finditer(r"stat: <\s*(.*?)\s+>", result, re.DOTALL):
        block = block.group(1).splitlines()
        block = [line.strip() for line in block]
        add_block(block)


# get sum for both uplink and downlink of a dictionary
def get_sum(dictionary):
    upsum = 0
    downsum = 0
    for id in dictionary:
        upsum += dictionary[id]["uplink"]
        downsum += dictionary[id]["downlink"]
    return upsum, downsum

def human_readable(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 ** 2:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1024 ** 3:
        return f"{bytes / 1024 ** 2:.2f} MB"
    elif bytes < 1024 ** 4:
        return f"{bytes / 1024 ** 3:.2f} GB"
    else:
        return f"{bytes / 1024 ** 4:.2f} TB"

def print_dictionary(dictionary):
    for id in dictionary:
        # print the id and the sum of uplink and downlink for that id in a human readable
        # format (KB, MB, GB, TB) and left justify the uplink and downlink values
        upsum, downsum = get_sum({id: dictionary[id]})
        upsum, downsum = human_readable(upsum).ljust(15), human_readable(downsum).ljust(15)
        print(f"{id}:")
        print(f"{'Uplink'.ljust(15)}{upsum}")
        print(f"{'downlink'.ljust(15)}{downsum}")
        print()


def print_results():
    categories = {"inbound": inbound, "outbound": outbound, "user": user}
    for category, data in categories.items():
        print(f"=============={category}==============")
        print_dictionary(data)
        upsum, downsum = get_sum(data)
        upsum, downsum = human_readable(upsum).ljust(15), human_readable(downsum).ljust(15)
        print("Total:")
        print(f"{'Uplink'.ljust(15)}{upsum}")
        print(f"{'downlink'.ljust(15)}{downsum}")
        print()



# read from the file
def read_from_file():
    global inbound, outbound, user
    if not os.path.exists(filename):
        return
    with open(filename, "r") as f:
        data = json.load(f)
        inbound = data["inbound"]
        outbound = data["outbound"]
        user = data["user"]


# write the data to a file
def write_to_file():
    with open(filename, "w") as f:
        json.dump({"inbound": inbound, "outbound": outbound, "user": user}, f, indent=4)



if __name__ == "__main__":
    read_from_file()
    result = run_command()
    parse_result(result)
    print_results()
    write_to_file()
