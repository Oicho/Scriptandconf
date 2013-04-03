#! /usr/bin/python3

import argparse
import datetime
import os
global eofpos
global file_name

gspos = -1


def methodswrite(classname, typeid, identifier, params, file_cc):
    file_cc += typeid + "\n" + classname + "::" + identifier + "(" + params
    file_cc += ")\n{\n}\n"


class Member(object):
    """Represent a class members and its setter/getter

    attributes: name_, typeid_
    """
    def __init__(self, input):
        temp = input.split()
        self.name_ = temp[len(temp) - 1].replace(";", "")
        i = 1
        self.typeid_ = temp[0]
        while i < len(temp) - 1:
            self.typeid_ += " " + temp[i]
            i += 1

    def gen_set_proto(self):
        temp = "    void " + self.name_ + "set(" + self.typeid_ + " input);\n"
        return temp

    def gen_get_proto(self):
        temp = "    " + self.typeid_ + " " + self.name_ + "get();\n"
        return temp

    def gen_get_def(self, classname):
        temp = "inline\n" + self.typeid_ + "\n" + classname + "::" + self.name_
        temp += "get()\n{\n    return this->" + self.name_ + ";\n}\n\n"
        return temp

    def gen_set_def(self, classname):
        temp = "inline\nvoid\n" + classname + "::" + self.name_ + "set(" + self.typeid_
        temp += " input)\n{\n    this->" + self.name_ + " = input;\n}\n\n"
        return temp


def aux_parse(l_string, i, methods_list, members_list):
    while i < len(l_string) and l_string[i].find("// \\") == -1:
        i += 1

    if i == len(l_string):
        return i
    print("curline is " + str(i) + ": " + l_string[i])

    if l_string[i] == "// \\getter /setter\n":
        print("found getter.setter")
        i += 2
        global gspos
        gspos = i
        print("gspos = " + str(i))
        return i
    elif l_string[i] == "// \\const /dec\n":
        print("found destructor/const")
        i += 2
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
                print("new members" + l_string[i])
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
        i = aux_parse(l_string, i, methods_list, members_list)
    print(members_list)
    l_string.insert(i + 1, "\n# include \"" + file_name.replace(".hh", ".hxx") + "\"\n")
    print(l_string)
    # ajouter les getter/setter dans les .hh
    if gspos == -1:
        print("Incorrect header file.")
        quit()

    for i in range(len(members_list)):
        l_string.insert(gspos, members_list[i].gen_get_proto())
        l_string.insert(gspos, members_list[i].gen_set_proto())
        file_hxx += members_list[i].gen_set_def(classname)
        file_hxx += members_list[i].gen_get_def(classname)
    file_hxx += "#endif " + (file_name.replace(".hh", "_HXX")).upper()
    fhxx = open(argument.file_name.replace(".hh", ".hxx"), "w")
    fhxx.write(file_hxx)
    # Verifier l argument force
    new_header = open(argument.file_name, "w")
    for j in range(len(l_string)):
        new_header.write(l_string[j])


def comment_header(project_name, file_type, now):
    f = "/*\n**    " + file_name.replace(".hh", "") + file_type
    f += "\n**      Created on: "
    f += str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    f += """\n**      By Gauthier \"Oicho\" FRIDIERE
**      Contact at: gauthier.fridiere@gmail.com
**    Project name: """
    f += project_name + "\n*/\n\n"
    return f


parser = argparse.ArgumentParser(prog="""Cc_generator""",
                                 description="""    This script generates .cc
and .hxx files by parsing a header file. The input header file must generates
respect the tag convention written in the README file. I strongly recommend you
to use my header generator.""",
                                 epilog="""AUTHORS: Gauthier \"Oicho\" FRIDIERE
Contact at: gauthier.fridiere@gmail.com
Under the beer ware license(Revision 42):
http://en.wikipedia.org/wiki/Beerware""")
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
now = datetime.datetime.now()
f_tab = args.file_name.rsplit("/")
file_name = f_tab[len(f_tab) - 1]
file_cc = comment_header(args.project_name, ".cc", now)
file_hxx = comment_header(args.project_name, ".hxx", now)
file_cc += "#include \"" + file_name + "\"\n\n"
preprocessdef = (file_name.replace(".hh", "_HXX")).upper()
file_hxx += "#ifndef " + preprocessdef + "\n# define " + preprocessdef
file_hxx += "\n\n# include \"" + file_name + "\"\n\n"

try:
    h_file = open(args.file_name, "r")
    parse_header(args, file_cc, file_hxx)
except OSError:
    print("Incorrect input header file")
