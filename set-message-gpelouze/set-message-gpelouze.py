
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




message = "Hello world!"

import json
filename = "/tmp/message_" + id + ".json"
file_message = open(filename, "w")
file_message.write(json.dumps(message))
file_message.close()
