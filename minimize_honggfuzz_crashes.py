__author__ = 'mcrxx'

import optparse
from os.path import isfile
from os.path import isdir
from os.path import exists
from os import listdir
from os import makedirs
from shutil import copyfile



def main(crashes_dir, output_dir):

    if not isdir(crashes_dir):
        print "[!] Directory %s not found." % (crashes_dir)
        exit(-1)

    if not exists(output_dir):
        print "[*] Creating directory : %s " % (output_dir)
        makedirs(output_dir)

    if not crashes_dir.endswith('/'):
        crashes_dir += '/'

    if not output_dir.endswith('/'):
        output_dir += '/'

    minimize_honggfuzz(crashes_dir, output_dir)

def minimize_honggfuzz(crashes_dir, output_dir):
    uniq_crashes = list()
    for file_name in listdir(crashes_dir):
        stack_signature = get_signature_honggfuzz(file_name)

        if stack_signature != -1:
            if not verify_signature(uniq_crashes, stack_signature):
                uniq_crashes.append(file_name)

    #Copy and print uniq crashes
    print "[*] Total uniq crashes: %d" % (len(uniq_crashes))
    for crash in uniq_crashes:
        print "[*] %s" % (crash)
        copyfile(crashes_dir + crash, output_dir + crash)


def verify_signature(uniq_crashes, stack_signature):
    found = False
    i = 0
    while not found and i < len(uniq_crashes):
        crash_signature = get_signature_honggfuzz(uniq_crashes[i])
        if crash_signature == stack_signature:
            found = True
        i += 1

    return found


def get_signature_honggfuzz(file_name):
    stack_signature = -1
    signal = -1
    values = file_name.split(".")
    if len(values) > 10:
        stack_signature = values[4]
    return stack_signature

def print_help(parser):
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-d', '--dir', action="store", help="Directory with honggfuzz crashes", dest="crashes_dir", type="string")
    parser.add_option('-o', '--output', action="store", help="Output directory to copy uniq crashes", dest="output_dir", type="string")
    
    (opts, args) = parser.parse_args()
    if opts.crashes_dir is not None and opts.output_dir is not None:
        main(opts.crashes_dir, opts.output_dir)
    else:
        print_help(parser)
