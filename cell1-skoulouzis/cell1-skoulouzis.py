
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--param_a', action='store', type=str, required='True', dest='param_a')

args = arg_parser.parse_args()
print(args)

id = args.id


param_a = args.param_a

conf_b = 'configuration'

conf_b = 'configuration'

res1 = conf_b + 'c' + param_a 

import json
filename = "/tmp/res1_" + id + ".json"
file_res1 = open(filename, "w")
file_res1.write(json.dumps(res1))
file_res1.close()
