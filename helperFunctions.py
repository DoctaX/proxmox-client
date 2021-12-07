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


def list_to_column(rows, max_disks, max_ips, max_vlans):
    for row in rows:
        for idx in range(max_disks):
            counter = idx + 1
            if counter > len(row['disk']) or not row['disk']:
                row[f'disk{counter}'] = ''
                continue

            row[f'disk{counter}'] = row['disk'][idx]
        del row['disk']

        for idx in range(max_ips):
            counter = idx + 1
            if counter > len(row['ip']) or not row['ip']:
                row[f'ip{counter}'] = ''
                continue

            row[f'ip{counter}'] = row['ip'][idx]
        del row['ip']

        for idx in range(max_vlans):
            counter = idx + 1
            if counter > len(row['vlan']) or not row['vlan']:
                row[f'vlan{counter}'] = ''
                continue

            row[f'vlan{counter}'] = row['vlan'][idx]
        del row['vlan']
    return rows


def isValid(csv_filepath):
    if csv_filepath != string.whitespace and csv_filepath is not None:
        try:
            full_path = Path(csv_filepath)
            parent_path = full_path.parents[0]

        except FileNotFoundError:
            return False

        except IndexError:
            return False

        if not parent_path.is_dir():
            return False

        return True
    return False


