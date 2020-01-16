#!/usr/bin/python3

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("greeting", help="your favorite greeting", type=str)
parser.add_argument("age", help="person's age", type=int)
parser.add_argument("--name", help="person's name", type=str)

args = parser.parse_args()

print(args)
print(args.name)
