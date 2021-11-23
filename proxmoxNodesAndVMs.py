from proxmoxer import ProxmoxAPI
import yaml


def getProx(DNSName, user, password, port):

    # 'pmx.nsis-au.nxcrd.net', user='cajaje@pve', password='c@6Un8r1T', port=443
    hosts = []
    children = {}
    finalDict = {}
    temp = {}

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
            childrenTemp.append(vm['name'] + dotFQDN)
            hosts.append(vm['name'] + dotFQDN)

        hostsTemp['hosts'] = childrenTemp
        children[node['id']] = hostsTemp

    # Converge all data gathered in the nested-for-loop into a Python Dictionary
    temp['hosts'] = hosts
    temp['children'] = children
    finalDict['all'] = temp

    # Convert above dictionary into YAML
    proxYAML = yaml.dump(finalDict, sort_keys=False)

    print(proxYAML)


# getProx('pmx.nsis-au.nxcrd.net', 'cajaje@pve', 'c@6Un8r1T', 443)

