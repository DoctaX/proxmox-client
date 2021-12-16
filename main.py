import argparse
from thinClientLogic import logic


def main():
    parser = argparse.ArgumentParser(
        description='___________/\/\/\/\/\/\/\ This script retrieves an inventory and metadata of nodes '
                    'and vm\'s in a Proxmox cluster and outputs it to either a CSV file or YAML '
                    'file/\/\/\/\/\/\/\\___________')

    parser.add_argument('-dns <TARGET-PROX-CLUSTER>', '--dnsname', type=str, metavar='', required=True,
                        help='The Subject Alternate Name or DNS Name of the host/cluster (can be retrieved '
                             'from certificate under \'Subject Alternate Name\')')

    parser.add_argument('-user <USERNAME>', '--username', type=str, metavar='', required=True,
                        help='The Username that will be used to sign in with')

    parser.add_argument('-pwd <PASSWORD>', '--password', type=str, metavar='', required=True,
                        help='Password credentials to authenticate user')

    parser.add_argument('-port <PORT>', '--port', type=int, metavar='', default=443,
                        help='The port that connection will be made to')

    parser.add_argument('-s', '--skipSSL', action='store_true', required=False,
                        help='Optional flag to skip SSL Certificate checks')

    parser.add_argument('-ft <FILE-TYPE>', '--filetype', type=str, metavar='', required=True,
                        help='Specify output file type, either \'CSV\' OR \'YAML\'')

    parser.add_argument('-fp <FILE-PATH>', '--filepath', type=str, metavar='', required=True,
                        help='Specify the full path of the file you want to export the data to')

    try:
        args = parser.parse_args()
        logic(args.dnsname, args.username, args.password, args.port, args.filetype, args.filepath, args.skipSSL)
    except SystemExit as e:
        parser.print_help()


main()
