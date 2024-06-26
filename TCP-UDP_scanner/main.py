import argparse
import sys

import scanner


def parse(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', dest='tcp', action='store_true',
                        help='the program scan tcp ports.')
    parser.add_argument('-u', dest='udp', action='store_true',
                        help='the program scan udp ports.')
    parser.add_argument('-p', '--ports', action='store', nargs=2, type=int,
                        default=[1, 65535], help='Ports range to scan.')
    parser.add_argument('host', action='store', help='host for scanning')

    args = parser.parse_args(args)
    if not args.tcp and not args.udp:
        args.tcp = True

    return args


def main(args):
    args = parse(args[1:])

    scan = scanner.Scanner(args.host, args.ports[0], args.ports[1], args.tcp, args.udp, workers=20)
    try:
        scan.start()
    except KeyboardInterrupt:
        scan.stop()


if __name__ == "__main__":
    main(sys.argv)
