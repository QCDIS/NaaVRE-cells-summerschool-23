
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--a', action='store', type=str, required='True', dest='a')


args = arg_parser.parse_args()
print(args)

id = args.id

import json
a = json.loads(args.a.replace('\'','').replace('[','["').replace(']','"]'))




b = []
for elem in a:
    b.append(elem + '_a')
    

import json
filename = "/tmp/b_" + id + ".json"
file_b = open(filename, "w")
file_b.write(json.dumps(b))
file_b.close()
