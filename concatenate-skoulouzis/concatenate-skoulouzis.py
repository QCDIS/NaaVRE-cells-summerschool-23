
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--b', action='store', type=str, required='True', dest='b')


args = arg_parser.parse_args()
print(args)

id = args.id

import json
b = json.loads(args.b.replace('\'','').replace('[','["').replace(']','"]'))



res = ''
for elem in b:
    res += elem

print(res)

