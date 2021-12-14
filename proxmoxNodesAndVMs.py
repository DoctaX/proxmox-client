from proxmoxer import ProxmoxAPI
from helperFunctions import _get_param, _extract_ip_from_agent
from pathlib import Path
import csv
import string
import operator


class prox:
    _connection = None

    def connect(self, DNSName, user, password, port):

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

    def list_to_column(self, rows, max_disks, max_ips, max_vlans):
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

    def is_valid_path(self, csv_filepath):
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

    def format_YAML(self, nodes, vms):

        hosts = []
        children = []
        temp = {}
        finalDict = {}
        vms_organised = {}

        for node in nodes:
            vms_organised[node['node']] = []
            for vm in vms:
                if vm['nodename'] == node['node']:
                    vms_organised[node['node']].append(vm['name'])

        nodes = [node['node'] for node in nodes]
        vms = [vm['name'] for vm in vms]

        print(nodes, '\n--------------------------\n', vms)
        finalDict['all'] = {
            'hosts': [],
            'children': {'node': {'hosts': []}}
        }



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


test = prox()
test.connect('pmx.nsis-au.nxcrd.net', 'cajaje@pve', 'c@6Un8r1T', 443)
nodes = test.get_nodes()
vms = test.get_vms(nodes)
test.format_YAML(nodes, vms)
