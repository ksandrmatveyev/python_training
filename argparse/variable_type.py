import argparse
parser = argparse.ArgumentParser()
parser.add_argument('nums', nargs=2, type=int)
args = parser.parse_args()

print("~ Nums: {}".format(args.nums))
