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


def aux_parse(l_string, i, methods_list, members_list):
    while i < len(l_string) and l_string[i].find("// \\") == -1:
        i += 1

    if i == len(l_string):
        return i

    print("curline is " + str(i) + ": " + l_string[i])

    if l_string[i] == "// \\getter /setter\n":
        print("found getter.setter")
        i += 1
        gspos = i
        return i
    elif l_string[i] == "// \\const /dec\n":
        print("found destructor/const")
        i += 2
        print(i)
        return i
    elif l_string[i] == "// \\methods\n":
        print("found methods")
        i += 2
        while (i < len(l_string) and
               l_string[i].find("// \\") == -1 and
               l_string[i].find("}") == -1):

            if l_string[i] != "\n" and l_string[i].find("//") == -1:
                methods_list.append(l_string[i])
            i += 1
        return i
    else:
        print("default")
        i += 2
        while (i < len(l_string) and
               l_string[i].find("// \\") == -1 and
               l_string[i].find("}") == -1):

            if l_string[i] != "\n" and l_string[i].find("//") == -1:
                members_list.append(Member(l_string[i]))
                print("new members")
                print(members_list)
            i += 1
        return i


def parse_header(argument, file_cc, file_hxx):
    header_file = open(argument.file_name, "r")
    classname = (argument.file_name.replace(".hh", "")).capitalize()
    l_string = header_file.readlines()
    i = 0
    methods_list = []
    members_list = []
    print(l_string)
    while i < len(l_string):
        if l_string[i].find("}") != -1:
            print("endoffile")
            break
        print(str(i) + "main loop")
        i = aux_parse(l_string, i, methods_list, members_list)
    print(members_list)
    for i in range(len(members_list)):
        file_hxx += members_list[i].gen_set_def(classname)
        file_hxx += members_list[i].gen_get_def(classname)
    print("hxx file")
    print(file_hxx)


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
preprocessdef = (args.file_name.replace(".hh", "_HXX")).upper()
file_hxx = "#ifndef " + preprocessdef + "\n# define " + preprocessdef + "\n\n"

try:
    h_file = open(args.file_name, "r")
    parse_header(args, file_cc, file_hxx)
except OSError:
    print("Incorrect input header file")
