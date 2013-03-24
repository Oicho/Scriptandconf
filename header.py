#! /usr/bin/python3

import argparse
import datetime

#We create a function to clearify the code
#Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str,
                    help="the class name")
parser.add_argument("-p", "--project_name", type=str,
                    help="the project name", default="None")
args = parser.parse_args()
now = datetime.datetime.now()
file = open(args.file_name + ".hh", "w")

try:
    file.write("/*\n**    " + args.file_name + ".hh\n**      Created on: ")
    file.write(str(now.day) + "/" + str(now.month) + "/" + str(now.year))
    file.write("""\n**      By Gauthier \"Oicho\" FRIDIERE
**      Contact at: gauthier.fridiere@gmail.com
**    Project name: """)

    file.write(args.project_name + "\n*/\n\n")
    # Now we write preprocessor
    classname = args.file_name.capitalize()
    up = args.file_name.upper() + "_HH"
    file.write("#ifndef " + up + "\n# define " + up + "\n\nclass " + classname)
    file.write("\n{\n// \const /dec\n  public:\n    ")
    file.write(classname + "();\n    virtual ~" + classname)
    # The comment is for the generatecc script to generate getter setter
    file.write("""();\n\n// \members declarations\n  private:\n
// \getter /setter\n  public:\n\n// \methods\n  public:\n\n};\n
#endif //! """)
    file.write(up)

except OSError:
    print ("Can't create the header file.")
    quit()
