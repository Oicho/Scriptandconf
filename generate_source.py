#! /usr/bin/python3


def getterwrite(classname, identifier, idtype):
    file_hxx.write("inline\nvoid\n" + classname + "::" + identifier + "get(")
    parameter = " param_" + identifier
    file_hxx.write(idtype + parameter + ")\n{\n  this->" + identifier + " = ")
    file_hxx.write(parameter + ";\n}\n\n")


def setterwrite(classname, identifier, idtype):
    file_hxx.write("inline\nvoid\n" + classname + "::" + identifier + "set()\n{\n")
    file_hxx.write("  return this->" + identifier + ";\n}\n\n")


def consdeswrite(classname, identifier):
    file_hxx.write(classname + "::" + identifier + "\n{\n\n\n}\n")


def methodswrite(classname, typeid, identifier):
    file_hxx.write(typeid + classname + "::" + identifier)
