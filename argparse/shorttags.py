import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v',
    action='store_true',
    help='verbose flag' )

args = parser.parse_args()

if args.verbose:
    print("~ Verbose!")
else:
    print("~ Not so verbose")
