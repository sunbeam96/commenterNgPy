#!/usr/bin/env python

import sys
import os

######################################
##           #commenterNG#          ##
##         simple script to         ##
##        comment out lines         ##
##  needed for software I worked on ##
##   https://github.com/sunbeam96   ##
######################################

class States():
    Accept = 0
    Skip_include = 1
    Skip_namespace = 2
    Skip_block = 3
    Skip_line = 4

filenameExt = sys.argv[1]


# below are sample usecases
# modify to vary behaviour

def determine_state(line, current_state, filename):
        if current_state == States.Accept:
                if "static_assert" in line:
                        return States.Skip_line
                elif "#include <boost/" + ".hpp>" in line:
                        return States.Skip_include
                elif "if (a != b)" in line:
                        return States.Skip_block
                elif "namespace " + filename in line:
                        return States.Skip_namespace
                else:
                        return States.Accept
        elif current_state == States.Skip_include:
                        return States.Accept
        elif current_state == States.Skip_line:
                if "static_assert" in line:
                        return current_state
                else:
                        return States.Accept
        elif current_state == States.Skip_namespace:
                if "}  // namespace " + filename in line:
                        return States.Skip_line
                else:
                        return States.Skip_namespace
        elif current_state == States.Skip_block:
                if "}" in line:
                        return States.Skip_line
                else:
                        return States.Skip_block

def parse():

        with open("output.tmp", "w") as temp_output:

                with open(filenameExt, "r+") as operand:
                        sep = '.'
                        filename = filenameExt.split(sep, 1)[0]
                        current_state = States.Accept
                        for line in operand:
                                current_state = determine_state(line, current_state, filename)
                                if current_state != States.Accept:
                                        line = '// [commenter] ' + line
                                temp_output.write(line)

        os.remove(filenameExt)
        os.rename("output.tmp", filenameExt)

parse()