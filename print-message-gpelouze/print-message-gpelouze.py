
import argparse
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')


arg_parser.add_argument('--message', action='store', type=str, required='True', dest='message')


args = arg_parser.parse_args()
print(args)

id = args.id

message = args.message



print(message)
