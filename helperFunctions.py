def _strtodict(data):
    rtn = {}
    chunks = data.split(',')
    for chunk in chunks:
        if '=' not in chunk:
            continue
        key, value = chunk.split('=')
        rtn[key] = value
    return rtn


# # tag
# def _get_vlan(str, attr):
#     opts = _strtodict(str)
#     if attr in opts:
#         return opts[attr]
#     return


# # ip
# def _get_ip(str, attr):
#     opts = _strtodict(str)
#     if attr in opts:
#         return opts[attr].replace("/24", "")


# # size
# def _get_disksize(str, attr):
#     opts = _strtodict(str)
#     if attr in opts:
#         return opts[attr]


def _get_param(str, attr):
    opts = _strtodict(str)
    if attr in opts:
        if '/24' in opts[attr]:
            return opts[attr].replace("/24", "")
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
