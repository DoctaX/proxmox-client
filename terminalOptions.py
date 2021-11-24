import argparse
from proxmoxNodesAndVMs import getProx

parser = argparse.ArgumentParser(description='/\/\/\/\/\/\/\/\ This script retrieves an inventory of nodes '
                                             'and vm\'s in a Proxmox cluster /\/\/\/\/\/\/\/\\')

parser.add_argument('-dns', '--dnsname', type=str, metavar='', required=True,
                    help='The Subject Alternate Name or DNS Name of the host/cluster (can be retrieved '
                         'from certificate under \'Subject Alternate Name\')\n')
parser.add_argument('-user', '--username', type=str, metavar='', required=True,
                    help='The Username that will be used to sign in with\n')
parser.add_argument('-pwd', '--password', type=str, metavar='', required=True,
                    help='Password credentials to authenticate user\n')
parser.add_argument('-p', '--port', type=int, metavar='', required=True,
                    help='The port that connection will be made to\n')

parser.add_argument('-c', '--csv', 
                    help='Export data as a csv to this location\n')


parser.print_help()

args = parser.parse_args()

getProx(args.dnsname, args.username, args.password, args.port, args.csv)
