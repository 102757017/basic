# coding: utf-8
#!/usr/bin/python
import rsa
import chardet
'''
RSA的算法涉及三个参数，n、e、d
n是两个大质数p、q的积，n的二进制表示时所占用的位数，就是所谓的密钥长度,理论上对n分解质因数可以得到p、q，实际上由于目前计算机算力难以对极大整数做因数分解，因此RSA目前破解不了
e可以任意取，但要求e与(p-1)*(q-1)互质；
根据e、n求d，要求(d*e1)mod((p-1)*(q-1))=1
(n，e)为公钥，用来对数据进行加密，是公开的，其余数字都是不公开的。
(n，d)为私钥，用来对数据进行解密
'''

#生成公匙参数n为1024位（二进制位数）的密匙对
(pubkey, privkey) = rsa.newkeys(1024)
print("公匙参数e：",pubkey.e)
print("公匙参数n：",pubkey.n)
print("公匙参数n位数(10进制)：",len(str(pubkey.n)))
print("公匙参数n位数(2进制)：",len(str(bin(pubkey.n))))
print("转换公匙为pkcs1格式",pubkey.save_pkcs1())

print("私匙参数d：",privkey.d)
print("私匙参数d位数(10进制)：",len(str(privkey.d)))
print("私匙参数d位数(2进制)：",len(str(bin(privkey.d))))
print("转换私匙为pkcs1格式",privkey.save_pkcs1())

msg="密码"
msg = msg.encode('utf-8')
print("对要加密的信息进行编码：",msg)

#使用公匙对信息进行加密
decrypt=rsa.encrypt(msg,pubkey)
#得到的密文是bytes数据类型，相当于n个10进制整数的串连。
print([x for x in decrypt])
print("密文的长度：",len(decrypt))

#使用私匙对信息进行解密
content = rsa.decrypt(decrypt, privkey)
#解密得到的也是bytes数据类型
print("解密后的文本",content)
print("对文本进行解码：",content.decode('utf-8'))
