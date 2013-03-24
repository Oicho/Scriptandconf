#! /usr/bin/python3

import argparse


def parse_header(header_file):
    header_file


def getterwrite(classname, identifier, idtype, file_hxx):
    file_hxx += "inline\nvoid\n" + classname + "::" + identifier + "get("
    parameter = " param_" + identifier
    file_hxx += idtype + parameter + ")\n{\n  this->" + identifier + " = "
    file_hxx += parameter + ";\n}\n\n"


def setterwrite(classname, identifier, idtype, file_hxx):
    file_hxx += "inline\nvoid\n" + classname + "::" + identifier
    file_hxx += "set()\n{\n  return this->" + identifier + ";\n}\n\n"


def consdeswrite(classname, identifier, file_cc):
    file_cc += classname + "::" + identifier + "\n{\n\n\n}\n"


def methodswrite(classname, typeid, identifier, params, file_cc):
    file_cc += typeid + "\n" + classname + "::" + identifier + "(" + params
    file_cc += ")\n{\n}\n"


parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str,
                    help="the header file name")
parser.add_argument("-p", "--project_name", type=str,
                    help="the project name", default="None")
parser.add_argument("-f", "--force",
                    help="You can use this option if you want the script\
                    to overwrite your header file without asking")
parser.add_argument("-v", "--verbose", type=int, help="Level of information you \
                    want to be print on the standard output between 0 and 3",
                    default=0)
args = parser.parse_args()
file_cc = "#include \"" + args.file_name + "\"\n\n"
preprocessdef = (args.file_name.replace(".hh.", "_HXX")).upper()
file_hxx = "#ifndef " + preprocessdef + "\n# define " + preprocessdef

try:
    h_file = open(args.file_name, "r")
except OSError:
    print("Incorrect input header file")
