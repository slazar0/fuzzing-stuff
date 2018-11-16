__author__ = 'mcrxx'

import subprocess, optparse, re, sys, struct, string
from os.path import isfile
from os.path import isdir

def main(input_file, output):

    if not isfile(input_file) and not isdir(output):
        print ("Provide a file and a directory which exist.")
        exit(1)

    if not output.endswith('/'):
        output = output + '/'

    get_constants(input_file, output)
    get_strings(input_file, output)


def get_constants(input_file, output):
    array = list()
    cmd = 'objdump -d %s' % (input_file)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while True:
        out = p.stdout.readline()
        if out == '' and p.poll() != None:
            break
        if out != '':
            out = out.rstrip()
            match = re.search(r"\$0x[0-9a-f]+",out)
            if match:
                item = match.group()[1:]
                if item not in array:
                    array.append(item)

    #When loop ends
    for item in array:
        f = open(output + item,'w+')
        value =  "".join(struct.pack("<I" if len(item) <= 11 else "<Q", int(item,0)))
        f.write(value)
        f.close()

def get_strings(input_file, output):
    f = open('dict.txt', 'w+')
    for s in strings(input_file):
        f.write('"' + s.rstrip()+ '"' + '\n')
    f.close()

def strings(filename, min=4):
    with open(filename, "rb") as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:  # catch result at EOF
            yield result


def print_help(parser):
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', action="store", help="Input binary to analyze", dest="input_file", type="string")
    parser.add_option('-o','--output', action="store", help="Output directory for generated files", dest="output",type="string")
    (opts, args) = parser.parse_args()
    if opts.input_file is not None and opts.output is not None:
        main(opts.input_file, opts.output)
    else:
        print_help(parser)
