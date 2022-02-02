import requests.exceptions
from proxmoxer import ProxmoxAPI
from helper_functions import _get_param, _extract_ip_from_agent
from pathlib import Path
import csv
import yaml
import string
import getpass


class Prox:
    _connection = None
    _nodeFQDN = None
    _vmFQDN = None

    def authenticate(self):
        return getpass.getpass()

    def connect(self, DNSName, user, password, port, skip_ssl):

        # Connect and authenticate to Proxmox server
        try:
            if skip_ssl:
                self._connection = ProxmoxAPI(DNSName, user=user, password=password, port=port, verify_ssl=False)
                return True

            self._connection = ProxmoxAPI(DNSName, user=user, password=password, port=port)
            return True

        except requests.exceptions.ConnectionError as c:
            print("\n** Connection error **\n")
            return False

    def get_nodes(self):

        # Iterate through each node in Proxmox cluster
        prox_nodes = []
        for node in self._connection.nodes.get():
            prox_nodes.append(node)
        return prox_nodes

    def get_vms(self, prox_nodes):

        vmList = []
        for prox_node in prox_nodes:
            for vm in self._connection.nodes(prox_node['node']).get('qemu'):

                vm['nodename'] = prox_node['node']
                vm['config'] = self._connection.nodes(prox_node['node']).qemu(vm['vmid']).config.get()

                try:
                    agent_data = self._connection.nodes(prox_node['node']).qemu(vm['vmid']).agent.get(
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

            if vm['template'] == 1:
                continue

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

    def format_YAML(self, nodes, vms):

        output = {"all": {"hosts": {}, "children": {}}}

        for node in nodes:
            self._nodeFQDN = "." + self._connection.nodes(node['node']).get('dns')['search']

            output["all"]["hosts"][node['node'] + self._nodeFQDN] = None
            output["all"]["children"][node['node'] + self._nodeFQDN] = {"hosts": {}}

        for vm in vms:

            try:
                self._vmFQDN = "." + vm['config']['searchdomain']
            except:
                self._vmFQDN = self._nodeFQDN

            if vm['template'] != 1:
                output["all"]["hosts"][vm["name"] + self._vmFQDN] = None
                output["all"]["children"][vm["nodename"] + self._nodeFQDN]["hosts"][vm["name"] + self._vmFQDN] = None

        return output

    def output_to_CSV_file(self, csv_filename, rows):
        full_path = Path(csv_filename)
        parent_path = full_path.parents[0]

        try:
            with open(csv_filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[*rows[0]])
                writer.writeheader()

                for row in rows:
                    writer.writerow(row)

                print("\nData has been populated to:", str(parent_path) + '\\' + full_path.name)

        except PermissionError as e:
            print(e)
            print("Insufficient permissions to write to file:", str(parent_path) + '\\' + full_path.name)
        return

    def output_to_YAML_file(self, data, yaml_filename):
        full_path = Path(yaml_filename)
        parent_path = full_path.parents[0]

        yamlstring = yaml.dump(data)
        yamlstring = yamlstring.replace(": null", ":")

        try:
            with open(yaml_filename, 'w') as yamlfile:
                yamlfile.write(yamlstring)
                yamlfile.close()

            print("\nData has been populated to:", str(parent_path) + '\\' + full_path.name)

        except PermissionError as p:
            print(p)
            print("Insufficient permissions to write to file:", str(parent_path) + '\\' + full_path.name)

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

            except (FileNotFoundError, IndexError):
                return False

            if not parent_path.is_dir():
                return False

            return True
        return False
