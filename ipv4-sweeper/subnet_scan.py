#!/usr/bin/env python3

import logging
from time import time
import multiprocessing as mp
from subprocess import check_call
import netifaces as ni

ITF  = ""
CPUC = mp.cpu_count()
logging.basicConfig(level=logging.INFO)

def call(itf, pack):
    l, r = pack.split(':')
    check_call(["./quick_ping.sh", itf, l, r])

def idxs(idx):
    res = []
    i = 1
    j = idx
    while j < 255:
        res.append((i,j))
        i += idx
        j += idx
    li, lj = res.pop()
    if 254 - lj != 0:
        res.append((li,254))

    return res

def scan():
    idx  = 254 // CPUC
    vals = idxs(idx)
    jobs = []
    
    for i in range(CPUC):
        l, r = vals[i]
        pack = str(l) + ":" + str(r)
        p = mp.Process(target=call, args=(ITF, pack, ))
        jobs.append(p)
        p.start()

    for j in jobs:
        j.join()

def get_ip_addr():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def itf_config():
    global ITF

    itfs = [x for x in ni.interfaces() if ("e" in x)]
    ip = get_ip_addr()
    logging.info("\tcurrent Address: "+str(ip))
    for i in itfs:
        d = ni.ifaddresses(i)
        if 2 in d and d[2][0]['addr'] == ip:
            ITF = i
            return

def banner():
    print("""
 ___________         ___     _______   ___ 
|_   _| ___ \       /   |   / / __  \ /   |
  | | | |_/ /_   __/ /| |  / /`' / /'/ /| |
  | | |  __/\ \ / / /_| | / /   / / / /_| |
 _| |_| |    \ V /\___  |/ /  ./ /__\___  |
 \___/\_|     \_/     |_/_/   \_____/   |_/
    """)

if __name__ == "__main__":
    strt = time()
    banner()
    itf_config()
    if ITF == "":
        logging.exception("unable to find interface ; "+get_ip_addr())    
    scan()
    logging.info("\trun time: "+str(round(time()-strt, 8)))

#   Sources:
#       - https://stackoverflow.com/a/38404357
#       - https://stackoverflow.com/questions/29714832/multi-processing-a-shell-script-within-python
#       - https://stackoverflow.com/questions/26432411/multiprocessing-dummy-in-python-is-not-utilising-100-cpu