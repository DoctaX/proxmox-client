from proxmoxNodesAndVMs import prox
from helperFunctions import is_valid_path, list_to_column

instance = prox()
instance.connect('pmx.nsis-au.nxcrd.net', 'cajaje@pve', 'c@6Un8r1T', 443, "C:\\nothing_file\\test41.csv")
nodes = instance.get_nodes()
vms = instance.get_vms(nodes)

rows, max_disks, max_ips, max_vlans = instance.format_CSV(vms)

rows = list_to_column(rows, max_disks, max_ips, max_vlans)

if is_valid_path("C:\\nothing_file\\test41.csv"):
    instance.output_to_file("C:\\nothing_file\\test41.csv", rows)