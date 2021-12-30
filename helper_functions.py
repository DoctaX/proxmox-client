from pathlib import Path
import string


def _strtodict(data):
    rtn = {}
    chunks = data.split(',')
    for chunk in chunks:
        if '=' not in chunk:
            continue
        key, value = chunk.split('=')
        rtn[key] = value
    return rtn


# tag
def _get_vlan(str):
    opts = _strtodict(str)
    if 'tag' in opts:
        return opts['tag']
    return


# ip
def _get_ip(str):
    opts = _strtodict(str)
    if 'ip' in opts:
        return opts['ip'].split('/')[0]


# size
def _get_disksize(str):
    opts = _strtodict(str)
    if 'size' in opts:
        return opts['size']


def _get_param(str, attr):
    opts = _strtodict(str)

    if attr in opts:
        if attr == "ip":
            return opts[attr].split("/")[0]
        return opts[attr]


def _extract_ip_from_agent(agentdata, csvdata):
    if not "result" in agentdata:
        return

    if len(agentdata["result"]) == 0:
        return

    for result in agentdata["result"]:
        if not "ip-addresses" in result:
            continue

        for ipdata in result["ip-addresses"]:
            if ipdata["ip-address-type"] != "ipv4" or ipdata["ip-address"] == "127.0.0.1":
                continue

            if ipdata["ip-address"] not in csvdata:
                csvdata.append(ipdata["ip-address"])



