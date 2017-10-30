# -*- coding: utf-8 -*-
"""
Created on Thu May 18 14:41:50 2017

@author: Leung
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import  MultipleLocator

zw=matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simhei.ttf')

group_labels=['06:00','09:00','12:00','15:00','18:00','21:00','00:00','03:00','06:00','09:00']
group_labels2=['0th day','开始','第一天','第二天','第三天','第四天','第五天','第六天','第七天']

totalload1=np.loadtxt('totalload.txt')
#totalload2=np.loadtxt('totalload2.txt')
#print(totalload1)
#totalload=[totalload1[33*4-1:57*4,0],totalload2[33*4-1:57*4,:]]
totalload=totalload1[33*4-1:57*4]
#000print(totalload)
chang=totalload
changdu=len(chang)
plt.figure(1)#,figsize=(10,5))
x=np.linspace(0,24,changdu)
ax1=plt.subplot(111)
std=np.std(totalload)

ax1.plot(x,totalload[:,0],label='总功率负荷',linewidth=2)
ax1.plot(x,totalload[:,1],'--',label='基础负荷')
ax1.plot(x,np.linspace(1000,1000,changdu),'--r',label='限制负荷')
#ax1.legend(pic1,('总功率负荷','基础负荷','限制负荷'),loc='lower left')
ax1.legend(loc='lower left',prop=zw)
plt.axis([0,24,400,1200])
plt.grid()
plt.xticks(x,group_labels,fontproperties=zw)
xmajorLocator = MultipleLocator(3)
ymajorLocator=MultipleLocator(100)
ax1.xaxis.set_major_locator(xmajorLocator)
ax1.yaxis.set_major_locator(ymajorLocator)
plt.xlabel('24小时仿真时间',fontproperties=zw,fontsize=12)
plt.ylabel('总功率负荷（kW）',fontproperties=zw,fontsize=12)
plt.title('居民小区功率负荷曲线',fontproperties=zw,fontsize=16)
plt.show()
#plt.savefig('平谷排序充电总负荷.png')
pjgl=sum(totalload1)[0]/len(totalload1)
chazhi=0
for i in totalload1:
    chazhi+=np.abs(pjgl-i[0])
pianc=chazhi/len(totalload1)


chargingnum1=np.loadtxt('chargingnumber.txt')
#chargingnum2=np.loadtxt('chargingnumber2.txt')
chargingnum=chargingnum1[33*4-1:57*4]
plt.figure(2)#,figsize=(10,5))
ax2=plt.subplot(111)
pic2=ax2.plot(x,chargingnum)
plt.axis([0,24,0,50])
plt.legend(prop=zw)
#ax2.legend(pic2,('充电数量'),loc='upper left')
plt.grid()
plt.xticks(x,group_labels,fontproperties=zw)
xmajorLocator = MultipleLocator(3)
ymajorLocator=MultipleLocator(5)
ax2.xaxis.set_major_locator(xmajorLocator)
ax2.yaxis.set_major_locator(ymajorLocator)
plt.xlabel('24小时仿真时间',fontproperties=zw)
plt.ylabel('电动汽车充电数量',fontproperties=zw)
plt.title('充电数量曲线',fontproperties=zw)           #这个可能用柱状图会要一点
plt.show()
#plt.savefig('平谷排序充电数量.png')
plt.bar(range(len(chargingnum)),chargingnum)

totalmoney1=np.loadtxt('totalmoney.txt')
#totalmoney2=np.loadtxt('totalmoney2.txt')
totalmoney=totalmoney1[0:168*4]
chd=len(totalmoney)
y=np.linspace(0,168,chd)
plt.figure(3)#,figsize=(10,5))
ax3=plt.subplot(111)
pic3=ax3.plot(y,totalmoney)
plt.axis([0,168,0,3000])
plt.legend(prop=zw)
#ax3.legend(pic3,('充电金额'),loc='lower right')
plt.grid()
plt.xticks(y,group_labels2,fontproperties=zw)
xmajorLocator = MultipleLocator(24)
ymajorLocator=MultipleLocator(300)
ax3.xaxis.set_major_locator(xmajorLocator)
ax3.yaxis.set_major_locator(ymajorLocator)
plt.xlabel('一周仿真时间',fontproperties=zw)
plt.ylabel('充电金额（元）',fontproperties=zw)
plt.title('充电金额曲线',fontproperties=zw)

plt.show()
#plt.savefig('平谷排序充电金额.png') 

pjz1=sum(totalload1[:,0])/len(totalload1[:,0])
#pjz2=sum(totalload2[:,0])/len(totalload2[:,0])
#np.savetxt('无序平均值.txt',pjz1)
chaz1=max(totalload1[:,0])-min(totalload1[:,0])
#chaz2=max(totalload2[:,0])-min(totalload2[:,0])
pfh1=totalload1[:,0]*totalload1[:,0]
pfh1=pfh1.sum()
#pfh2=totalload2[:,0]*totalload2[:,0]
#pfh2=pfh2.sum()
var1=pfh1/changdu-pjz1**2
#var2=pfh2/changdu-pjz2**2
#np.savetxt('无序方差.txt',var1)
print('标准差为：\n%f' %(std))
print('差值为：\n %.2f' %(chaz1))
print('平均值为：\n %.2f' %(pjz1))
print('方差为：\n %.2f' %(var1))


