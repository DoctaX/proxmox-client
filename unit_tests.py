import unittest
from helper_functions import _get_param, _get_vlan, _get_ip, _get_disksize
from proxmox_nodes_and_vms import Prox


class testProxFunctions(unittest.TestCase):

    def test_get_vlan_matches_getparam(self):
        vlan_test1 = "virtio=3A:53:6F:41:21:78,bridge=vmbr0,firewall=1,tag=1616"
        assert int(_get_param(vlan_test1, 'tag')) == 1616
        assert int(_get_vlan(vlan_test1)) == int(_get_param(vlan_test1, 'tag'))

        vlan_test2 = "virtio=52:DA:C3:E4:40:18,bridge=vmbr0,firewall=1,tag=68"
        assert int(_get_param(vlan_test2, 'tag')) == 68
        assert int(_get_vlan(vlan_test2)) == int(_get_param(vlan_test2, 'tag'))

    def test_get_ip_matches_getparam(self):
        ip_test1 = "ip=10.10.132.101/24,gw=10.10.132.1"
        assert _get_param(ip_test1, 'ip') == '10.10.132.101'
        assert _get_ip(ip_test1) == _get_param(ip_test1, 'ip')

        ip_test2 = "ip=10.10.128.221/8,gw=10.10.128.1"
        assert _get_param(ip_test2, 'ip') == '10.10.128.221'
        assert _get_ip(ip_test2) == _get_param(ip_test2, 'ip')

    def test_get_disksize_matches_getparam(self):
        disksize_test1 = 'VM_Data:vm-107-disk-0,size=64G'
        assert _get_param(disksize_test1, 'size') == '64G'
        assert _get_disksize(disksize_test1) == _get_param(disksize_test1, 'size')

        disksize_test2 = '/dev/disk/by-id/scsi-35000c50063229fcb,size=3907018584K'
        assert _get_param(disksize_test2, 'size') == '3907018584K'
        assert _get_disksize(disksize_test2) == _get_param(disksize_test2, 'size')

    def test(self):
        test = Prox()
        test.connect(2, 2, 2, 2, False)


if __name__ == '__main__':
    unittest.main()
