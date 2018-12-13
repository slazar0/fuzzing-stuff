__author__ = 'slazar0'

import lief, optparse

def main(binary_name, function_name):

	binary = lief.parse(binary_name)	
	find_exported_function(binary, function_name)


def find_exported_function(binary, function):
    
    if function in binary.exported_functions:
        print "[*] Function %s found." % (function)
    else:
        print "[*] Function %s not found." % (function)

def print_help(parser):
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-b', '--binary', action="store", help="Binary to analyze", dest="binary_name", type="string")
    parser.add_option('-f','--function', action="store", help="Function to find in the binary", dest="function_name",type="string")
    (opts, args) = parser.parse_args()
    if opts.binary_name is not None and opts.function_name is not None:
        main(opts.binary_name, opts.function_name)
    else:
        print_help(parser)