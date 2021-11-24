from proxmoxer import ProxmoxAPI
from helperFunctions import _get_param, _extract_ip_from_agent
import yaml
import csv


def getProx(DNSName, user, password, port, csv_filename=None):
    # 'pmx.nsis-au.nxcrd.net', user='cajaje@pve', password='c@6Un8r1T', port=443
    hosts = []
    children = {}
    finalDict = {}
    temp = {}

    vm_data = {}

    # Connect and authenticate to Proxmox server
    proxmox = ProxmoxAPI(DNSName, user=user, password=password, port=port)
    nodes = proxmox.nodes

    # Iterate through each node in Proxmox cluster
    for node in nodes.get():
        dotFQDN = "." + nodes(node['node']).get('dns')['search']
        hosts.append(node['id'] + dotFQDN)
        childrenTemp = []
        hostsTemp = {}

        # Iterate through each VM in each node
        for vm in nodes(node['node']).get('qemu'):
            vm_data[vm['name']] = {
                'vm': vm,
                'config': nodes(node['node']).qemu(vm['vmid']).config.get(),
            }

            try:
                agentdata = nodes(node['node']).qemu(vm['vmid']).agent.get('network-get-interfaces')
                vm_data[vm['name']]['network-agent'] = agentdata
            except:
                pass

            childrenTemp.append(vm['name'] + dotFQDN)
            hosts.append(vm['name'] + dotFQDN)

        hostsTemp['hosts'] = childrenTemp
        children[node['id']] = hostsTemp

    # Converge all data gathered in the nested-for-loop into a Python Dictionary
    temp['hosts'] = hosts
    temp['children'] = children
    finalDict['all'] = temp
    rows = []

    if csv_filename:

        max_disks = 0
        max_ips = 0
        max_vlans = 0

        for vm, data in vm_data.items():
            vmdata = data['vm']
            vmconfig = data['config']
            csvdata = {
                'name': vm,
                'status': vmdata['status'],
                'cpus': vmdata['cpus'],
                'memory': vmconfig['memory'],
                'vlan': [],
                'ip': [],
                'disk': [],
            }

            for chunk in ['net', 'scsi', 'ipconfig', 'virtio']:
                for iter in range(5):
                    iterchunk = f"{chunk}{iter}"
                    if iterchunk in vmconfig:

                        if chunk == 'net':
                            tmp = _get_param(vmconfig[iterchunk], "tag")
                            if tmp:
                                csvdata['vlan'].append(tmp)

                        if chunk == 'ipconfig':
                            tmp = _get_param(vmconfig[iterchunk], "ip")
                            if tmp:
                                csvdata['ip'].append(tmp)

                            if 'network-agent' in data and data['network-agent']:
                                _extract_ip_from_agent(data['network-agent'], csvdata['ip'])

                        if chunk in ('scsi', 'virtio'):
                            tmp = _get_param(vmconfig[iterchunk], "size")
                            if tmp:
                                csvdata['disk'].append(tmp)

            max_disks = max(len(csvdata['disk']), max_disks)
            max_ips = max(len(csvdata['ip']), max_ips)
            max_vlans = max(len(csvdata['vlan']), max_vlans)

            rows.append(csvdata)

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

        # with open(csv_filename, 'w') as csvfile:
        #     # writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        #     writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        #     writer.writeheader()
        #     for row in rows:
        #         writer.writerow(row)

        return

    # Convert above dictionary into YAML
    proxYAML = yaml.dump(finalDict, sort_keys=False)


getProx('pmx.nsis-au.nxcrd.net', 'cajaje@pve', 'c@6Un8r1T', 443, "C:\\nothing_file\\test5.csv")
