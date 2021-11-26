import argparse
from proxmoxNodesAndVMs import proxmoxData


class terminal:
    def main(self):
        parser = argparse.ArgumentParser(description='_______________/\/\/\/\/\/\/\/\ This script retrieves an inventory of nodes '
                                                     'and vm\'s in a Proxmox cluster /\/\/\/\/\/\/\/\\_______________')
        parser.add_argument('-dns', '--dnsname', type=str, metavar='', required=True,
                            help='The Subject Alternate Name or DNS Name of the host/cluster (can be retrieved '
                                 'from certificate under \'Subject Alternate Name\')')
        parser.add_argument('-user', '--username', type=str, metavar='', required=True,
                            help='The Username that will be used to sign in with')
        parser.add_argument('-pwd', '--password', type=str, metavar='', required=True,
                            help='Password credentials to authenticate user')
        parser.add_argument('-p', '--port', type=int, metavar='', required=True,
                            help='The port that connection will be made to')
        parser.add_argument('-c', '--csv', type=str, metavar='', required=True,
                            help='Export data as a csv to this location')

        args = parser.parse_args()

        data = proxmoxData()
        data.getProx(args.dnsname, args.username, args.password, args.port, args.csv)


if __name__ == '__main__':
    run = terminal()
    run.main()
