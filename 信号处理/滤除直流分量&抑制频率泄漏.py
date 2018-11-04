# coding: utf-8
#!/usr/bin/python
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import scipy.signal as signal


#64个采样点
x=np.linspace(0,np.pi*7,64)

#设置需要采样的信号，波形内有直流分量
y=5+7*np.sin(x)

yy=fft(y)                     #快速傅里叶变换
yf=abs(fft(y))                # 取绝对值
yf1=abs(fft(y))/len(x)           #归一化处理
yf2 = yf1[range(int(len(x)/2))]  #由于对称性，只取一半区间

xf = np.arange(len(y))        # 频率
xf2 = xf[range(int(len(x)/2))]  #取一半区间



#直流分量会造成0频处数值很大，因此先去除直流分量
y2=y-np.mean(y)

#在很多情况下，并不能采样到整数个周期。 因此，测量到的信号就会被从周期中间切断，造成频谱泄漏，因此需要对信号加窗抑制频谱泄漏。
#创建窗口
window = signal.hanning(64)
#加窗
y2=y2*window
yy=fft(y2)                     #快速傅里叶变换
yf=abs(fft(y2))                # 取绝对值
yf1=abs(fft(y2))/len(x)           #归一化处理
yf3 = yf1[range(int(len(x)/2))]  #由于对称性，只取一半区间
xf = np.arange(len(y))        # 频率
xf3 = xf[range(int(len(x)/2))]  #取一半区间


plt.subplot(311)
plt.plot(x,y)   
plt.title('Original wave')

plt.subplot(312)
plt.plot(xf2,yf2,'b')
#改波形有直流分量并且频谱泄漏
plt.title('before',fontsize=10,color='#F08080')

plt.subplot(313)
plt.plot(xf3,yf3,'b')
plt.title('after',fontsize=10,color='#F08080')

plt.show()
