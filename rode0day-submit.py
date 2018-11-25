__author__ = 'mcrxx'

import requests, optparse, time
from os import listdir
from os.path import isfile
from os.path import isdir

def main(file=None, dir=None, challenge_id=None, key=None):
    if file is not None and isfile(file):
        response = send_request(file, challenge_id, key)
        parse_response(response)
    elif dir is not None and isdir(dir):
        if not dir.endswith('/'):
            dir = dir + '/'
        score = get_score(challenge_id,key)
        directory_list = listdir(dir)
        for file in directory_list:
            response = send_request(dir + file, challenge_id, key)
            score = parse_response(file, response, score)

def get_score(challenge_id, key):
    #Send an empty file to get score
    empty_file = 'empty.txt'
    f = open(empty_file,'w+')
    f.close()

    score = 0
    response = send_request('empty.txt', challenge_id, key) 
    for line in response.splitlines():
        line = line.split(":")
        if 'score' in line[0]:
            score = line[1].replace(" ","")
        if 'remain' in line[0]:
            print "Requests available: %s" % (line[1].replace(" ", ""))
    return score

def send_request(file, challenge_id, key):
    response = ""
    url = 'https://rode0day.mit.edu/api/1.0/submit'

    multipart = {'input': open(file,'rb')}
    data = {'challenge_id': challenge_id, 'auth_token': key}
    r = requests.post(url, data=data, files = multipart)
    #print file
    if r.status_code == 200:
        response = r.text
    time.sleep(1)
    return response

def parse_response(file, response, score):
    new_score = score
    for line in response.splitlines():
        line = line.split(":")
        if 'score' in line[0]:
            tmp_score = line[1].replace(" ", "")
            if score < tmp_score:
                new_score = tmp_score
                print "[*] Valid rode0day crash. File = %s - Score = %s" % (file, new_score)
    return new_score
       

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
