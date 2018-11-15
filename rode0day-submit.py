__author__ = 'mcrxx'

import requests, optparse
from os import listdir
from os.path import isfile

def main(file=None, dir=None, challenge_id=None, key=None):
    if file is not None and isfile(file):
        send_request(file, challenge_id, key)
    else:
        if not dir.endswith('/'):
            dir = dir + '/'
        directory_list = listdir(dir)
        for file in directory_list:
            send_request(dir + file, challenge_id, key)

def send_request(file, challenge_id, key):
    url = 'https://rode0day.mit.edu/api/1.0/submit'

    multipart = {'input': open(file,'rb')}
    data = {'challenge_id': challenge_id, 'auth_token': key}
    r = requests.post(url, data=data, files = multipart)
    print r.status_code
    print r.text

def print_help(parser):
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", help="File containing the crash to submit", dest="file", type="string")
    parser.add_option('-d','--dir', action="store", help="Directory with crashes to submit", dest="dir",type="string")
    parser.add_option('-k','--key', action="store", help="API key", dest="key", type="string")
    parser.add_option('-c','--challenge', action="store", help="Challenge ID (included in info.yaml)", dest="challenge_id", type="string")
    (opts, args) = parser.parse_args()
    if (opts.file is not None or opts.dir is not None) and opts.key is not None and opts.challenge_id is not None:
        main(opts.file, opts.dir, opts.challenge_id, opts.key)
    else:
        print_help(parser)
