from proxmoxer import ProxmoxAPI
from helperFunctions import _get_param, _extract_ip_from_agent, list_to_column
from pathlib import Path
import csv


class prox:
    _connection = None

    def connect(self, DNSName, user, password, port, csv_filename=None):

        # Connect and authenticate to Proxmox server
        self._connection = ProxmoxAPI(DNSName, user=user, password=password, port=port)

    def get_nodes(self):
        # Iterate through each node in Proxmox cluster
        nodesList = []

        for node in self._connection.nodes.get():
            nodesList.append(node)

        return nodesList

    def get_vms(self, nodes):
        agent_data = None
        vmList = []
        for node in nodes:
            for vm in self._connection.nodes(node['node']).get('qemu'):

                vm['nodename'] = node['node']
                vm['config'] = self._connection.nodes(node['node']).qemu(vm['vmid']).config.get()

                try:
                    agent_data = self._connection.nodes(node['node']).qemu(vm['vmid']).agent.get(
                        'network-get-interfaces')
                    vm['network-agent'] = agent_data

                except Exception as e:
                    pass
                vmList.append(vm)

        return vmList

    def format_CSV(self, vmList):
        rows = []
        max_ips = 0
        max_disks = 0
        max_vlans = 0

        for vm in vmList:
            vmconfig = vm['config']
            csvdata = {
                'name': vm['name'],
                'status': vm['status'],
                'cpus': vm['cpus'],
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

                            if 'network-agent' in vm and vm['network-agent']:
                                _extract_ip_from_agent(vm['network-agent'], csvdata['ip'])

                        if chunk in ('scsi', 'virtio'):
                            tmp = _get_param(vmconfig[iterchunk], "size")
                            if tmp:
                                csvdata['disk'].append(tmp)

            max_disks = max(len(csvdata['disk']), max_disks)
            max_ips = max(len(csvdata['ip']), max_ips)
            max_vlans = max(len(csvdata['vlan']), max_vlans)
            print(csvdata)
            rows.append(csvdata)

        return rows, max_disks, max_ips, max_vlans

    def output_to_file(self, csv_filename, rows):
        full_path = Path(csv_filename)
        parent_path = full_path.parents[0]

        with open(csv_filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[*rows[0]])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        print("\nData has been populated to:", str(parent_path) + '\\' + full_path.name)
        return

    def proxYAML(self, nodes, vms, all):
        x = None
        ## YAML data gathering
        # temp['hosts'], temp['children'] = hosts, children
        # finalDict['all'] = temp

        # try:
        #     agentdata = nodes(node['node']).qemu(vm['vmid']).agent.get('network-get-interfaces')
        #     vm_data[vm['name']]['network-agent'] = agentdata
        # except:
        #     pass

        # for node in nodes.get():
        #     dotFQDN = "." + nodes(node['node']).get('dns')['search']
        #     hosts.append(node['id'] + dotFQDN)
        #     childrenTemp = []
        #     hostsTemp = {}
        #
        #     # Iterate through each VM in each node
        #     for vm in nodes(node['node']).get('qemu'):
        #         childrenTemp.append(vm['name'] + dotFQDN)
        #         hosts.append(vm['name'] + dotFQDN)
        #
        #     hostsTemp['hosts'] = childrenTemp
        #     children[node['id']] = hostsTemp
        #
        #     # Converge all data gathered in the nested-for-loop into a Python Dictionary
        # temp['hosts'] = hosts
        # temp['children'] = children
        # finalDict['all'] = temp
        #
        # # Convert above dictionary into YAML
        # proxYAML = yaml.dump(finalDict, sort_keys=False)
        #
        # print(proxYAML)

        # print(finalDict)
        # if csv_filename != string.whitespace and csv_filename is not None:
        #     dataProcessing = proxmox()
        #     dataProcessing.data_processing(csv_filename, vm_data)
        #     return
        #
        # print("No CSV file was passed")


