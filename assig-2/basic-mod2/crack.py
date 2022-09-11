alpha = list(map(chr, range(ord('a'), ord('z')+1)))
f = open("message.txt", "r")
lines = f.readlines()[0]
res = ""
for l in lines.split():
    r = pow(int(l), -1, 41)

    if r in range(1, 27):
        res += alpha[r-1]
    elif r in range(27, 37):
        dig = r - 27
        res += str(dig)
    else:
        res += "_"
print(res)
# picoCTF{1nv3r53ly_h4rd_c680bdc1}