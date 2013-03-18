#! /usr/bin/python3

import argparse
import datetime

def print_init_header(arguments):
    now = datetime.datetime.now()
    file = open(args.file_name + ".hh", "w")
    file.write("/*\n**    " + args.file_name + ".hh" + "\n**      Created on: ")
    file.write()
    file.write("**      By Gauthier \"Oicho\" FRIDIERE\n**      Contact at:")
    
parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str, 
                    help="the class name")
parser.add_argument("-p","--project_name", type=str,
                    help="the project name", default="None")
args = parser.parse_args()
print (args.file_name)
print (args.project_name)
print_init_header(args)