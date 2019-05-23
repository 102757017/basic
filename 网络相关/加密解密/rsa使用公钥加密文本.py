# coding: utf-8
#!/usr/bin/python
import rsa

'''
RSA的算法涉及三个参数，n、e、d
n是两个大质数p、q的积，n的二进制表示时所占用的位数，就是所谓的密钥长度,理论上对n分解质因数可以得到p、q，实际上由于目前计算机算力难以对极大整数做因数分解，因此RSA目前破解不了
e可以任意取，但要求e与(p-1)*(q-1)互质；
根据e、n求d，要求(d*e1)mod((p-1)*(q-1))=1
(n，e)为公钥，用来对数据进行加密，是公开的，其余数字都是不公开的。
(n，d)为私钥，用来对数据进行解密
'''
def Gen_psw(psw):
    n="BE24E372DC1B329633A6A014A7C02797915E3C363DD6EE119377BD645329B7E6446B4A71AC5F878EBC870C6D8BFD3C06B92E6C6E93390B34192A7A9E430800091761473FAC2CC0A68A828B2589A8CB729C19161E8E27F4C0F3CDE9701FAFE48D2B65947799072AFA6A3F2D7BDBEF8B6D7429C2D115A3E5F723467D57B3AC6967"
    
    n = int(n,16)
    e=int("10001")

    #N,e是公钥
    a=rsa.PublicKey(n,e)
    pwd=psw.encode('utf8')

    #使用公钥对pwd加密得到密文
    b=rsa.encrypt(pwd, a)
    #print(b,len(b))

    hex_str = ''
    # 按位转换成16进制
    for x in b:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h
    hex_str =hex_str.upper()
    return hex_str

if __name__=="__main__":
    #使用rsa加密
    encrypt=Gen_psw('zxhhf1962')
    print(encrypt)




