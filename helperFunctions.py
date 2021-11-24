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


###### _get_vlan test cases ######
# test: virtio=3A:53:6F:41:21:78,bridge=vmbr0,firewall=1,tag=1616 |||| equals: 1616
# test: virtio=52:DA:C3:E4:40:18,bridge=vmbr0,firewall=1,tag=68 |||| equals: 68

###### _get_ip test cases ######
# test: ip=10.10.132.101/24,gw=10.10.132.1 |||| equals: 10.10.132.101
# test: ip=10.10.128.221/8,gw=10.10.128.1 |||| equals: 10.10.128.221

###### _get_disksize test cases ######
# test:  VM_Data:vm-107-disk-0,size=64G |||| equals: 64G
# test: /dev/disk/by-id/scsi-35000c50063229fcb,size=3907018584K |||| equals: 3907018584K

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
