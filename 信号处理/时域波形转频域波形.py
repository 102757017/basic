# coding: utf-8
#!/usr/bin/python
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import seaborn


#64个采样点
x=np.linspace(0,np.pi*6,64)      

#设置需要采样的信号
y=7*np.sin(x)

yy=fft(y)                     #快速傅里叶变换

yf=abs(fft(y))                # 取绝对值
yf1=abs(fft(y))/len(x)           #归一化处理
yf2 = yf1[range(int(len(x)/2))]  #由于对称性，只取一半区间

xf = np.arange(len(y))        # 频率
xf2 = xf[range(int(len(x)/2))]  #取一半区间


plt.subplot(211)
plt.plot(x,y)   
plt.title('Original wave')



plt.subplot(212)
#显示的波形在x=3处有峰值，表示在64个采样点区间内，波形重复了3次，频率为3
#将采样点扩展到1s的时间内，即可获得该波形1s内重复的次数（该波形的真实频率）
plt.plot(xf2,yf2,'b')
plt.title('FFT of Mixed wave)',fontsize=10,color='#F08080')


plt.show()
