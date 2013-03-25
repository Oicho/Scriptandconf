#! /usr/bin/python3

import argparse


global gspos


class Member(object):
    """Represent a class members and its setter/getter

    attributes: name_, typeid_
    """
    def __init__(self, input):
        temp = input.split()
        self.name_ = temp[len(temp) - 1]
        self.typeid_ = temp

    def generate_set_proto(self):
        temp = self.name_ + "set(" + self.typeid_ + "input);\n"
        return temp

    def generate_get_proto(self):
        temp = self.typeid_ + " " + self.name_ + "get();\n"
        return temp

    def gen_get_def(self, classname):
        temp = "inline\n" + self.typeid_ + "\n" + classname + "::" + self.name_
        temp += "get()\n{\n    return this->" + self.name_ + ";\n}\n\n"
        return temp

    def gen_set_def(self, classname):
        temp = "inline\nvoid\n" + classname + "::" + self.name_ + "set(" + self.typeid_
        temp += "input)\n{\n    this->" + self.name_ + " = input;\n}\n\n"
        return temp


def parse_header(header_file, file_cc, file_hxx, classname):
    l_string = header_file.readlines()
    i = 0
    methods_list = []
    members_list = []
    for i in range(len(l_string)):
        if l_string[i].find("}"):
            break
        aux_parse(l_string, i, methods_list, members_list)
    for i in range(len(members_list)):
        file_hxx += members_list[i].gen_set_def(classname)
        file_hxx += members_list[i].gen_get_def(classname)


def aux_parse(l_string, i, methods_list, members_list):
    while i < len(l_string) and not l_string[i].find("// \\"):
        i += 1
    if l_string[i] == "// \\getter /setter":
        i += 1
        gspos = i
    elif l_string[i] == "// \\const /dec":
        i += 2
    elif l_string[i] == "// \\methods":
        i += 2
        while i < len(l_string) and not l_string[i].find("// \\") and not l_string[i].find("}"):
            if l_string[i] != "\n" and not l_string[i].find("//"):
                methods_list.append(l_string[i])
            i += 1
    else:
        i += 2
        while i < len(l_string) and not l_string[i].find("// \\") and not l_string[i].find("}"):
            if l_string[i] != "\n" and not l_string[i].find("//"):
                members_list.append(Member(l_string[i]))
            i += 1


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
                    to overwrite your header file without asking",
                    action="store_true")
parser.add_argument("-v", "--verbose", type=int, help="Level of information you \
                    want to be print on the standard output between 0 and 3",
                    default=0)
args = parser.parse_args()
file_cc = "#include \"" + args.file_name + "\"\n\n"
preprocessdef = (args.file_name.replace(".hh.", "_HXX")).upper()
file_hxx = "#ifndef " + preprocessdef + "\n# define " + preprocessdef + "\n\n"

try:
    h_file = open(args.file_name, "r")
except OSError:
    print("Incorrect input header file")
