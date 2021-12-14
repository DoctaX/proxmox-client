from proxmoxNodesAndVMs import prox


def logic(dns, user, pwd, port, file_type, file_path):

    instance = prox()

    if not instance.is_valid_path(file_path):
        print("The file path you have entered is not valid")
        return

    instance.connect(dns, user, pwd, port)
    nodes = instance.get_nodes()
    vms = instance.get_vms(nodes)

    if file_type == 'csv':
        rows, max_disks, max_ips, max_vlans = instance.format_CSV(vms)
        rows = instance.list_to_column(rows, max_disks, max_ips, max_vlans)
        instance.output_to_file(file_path, rows)

    # instance.connect('pmx.nsis-au.nxcrd.net', 'cajaje@pve', 'c@6Un8r1T', 443, "C:\\nothing_file\\test42.csv")


