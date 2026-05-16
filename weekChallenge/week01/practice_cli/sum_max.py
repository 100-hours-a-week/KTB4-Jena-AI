import argparse

parser = argparse.ArgumentParser(description='Add sum integers.')
parser.add_argument('integers', type=int, nargs='+', help='integer list')
parser.add_argument('--sum', action='store_const', const=sum, default=max, help='sum the integers (default: fine the max)')

args = parser.parse_args()

print(args.sum(args.integers))