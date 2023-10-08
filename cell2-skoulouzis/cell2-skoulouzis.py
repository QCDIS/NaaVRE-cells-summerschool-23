
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--res1', action='store', type=str, required='True', dest='res1')


args = arg_parser.parse_args()
print(args)

id = args.id

res1 = args.res1


conf_b = 'configuration'

conf_b = 'configuration'

res2 = res1 + conf_b

