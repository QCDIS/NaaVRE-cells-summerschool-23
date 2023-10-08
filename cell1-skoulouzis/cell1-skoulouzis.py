
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id



conf_b = 'configuration'

conf_b = 'configuration'

res1 = conf_b + 'c'

import json
filename = "/tmp/res1_" + id + ".json"
file_res1 = open(filename, "w")
file_res1.write(json.dumps(res1))
file_res1.close()
