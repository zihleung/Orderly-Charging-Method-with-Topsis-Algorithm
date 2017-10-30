# -*- coding: utf-8 -*-
"""
Created on Thu May 18 14:21:11 2017

@author: Leung
"""

import numpy as np

class AISITERO:
    def __init__(self,weight,num,sercost):
    #程序初始化
        self.weight=weight                              #topsis算法权重
        self.num=num                                    #电动汽车及充电桩数量
        self.sercost=sercost                            #服务费
        self.price=[]                                   #峰谷平电价
        self.residentload=[]                            #居民用电负荷
        self.bodong=[]                                  #居民用电负荷波动
        self.avapiles=[]                                #可用充电桩数量
        self.carimf=[]                                  #电动汽车信息
        self.lefttime=[]#np.zeros(num)                     #外出时间
        self.cometime=[]#np.zeros(num)                     #回来时间
        self.cargo=[]
        self.totaltime=0                                #总等待时间
        self.offpower=np.zeros(num)                     #电量耗尽不能出行次数
        self.leftpower=np.ones(num)*0.6                 #剩余电量百分比
        self.outpower=[]#np.zeros(num)                     #出行剩余电量值
        self.ischarging=np.zeros((num,),dtype=np.int)   #未充电为0在充电为1
        self.off=0                                      #不能出行次数
        self.waittime=np.zeros(num)                     #等待时间
        self.longgest=0                                 #最长充电时间
        self.totalcost=0                                #充电金额
        self.money=[]                                   #每个时刻的充电金额
        self.isgoout=[]#np.zeros((num,),dtype=np.int)      #不出行为0出行为1
        self.where=np.zeros((num,),dtype=np.int)        #在外为1在小区为0
        self.tempwhere=np.zeros((num,),dtype=np.int)    #前一个状态
        self.chargingnum=[]                             #充电数量
        self.staytime=np.zeros(num)                     #停留时间
        self.day=30                                     #仿真天数
        self.ke=0                                       #仿真时刻
        self.nengcho=0                                  #能充电的数量
        self.totalload=[]                               #总负荷
        self.satisfaction=np.zeros(7)                   #充电满意程度规律
        self.zuidari=0
        self.zuidashi=0
        self.riqi=0

    def readimf(self):
    #获取初始数据
        self.residentload=np.loadtxt('小区居民日常负荷数据.txt')
        self.carimf=np.loadtxt('carimf.txt')
        self.price=np.loadtxt('price.txt')
        self.cargo=np.loadtxt('cargo.txt')

    def newdaystate(self,riqi):
    #每天生成新状态
        i=0
        self.lefttime=[]
        self.cometime=[]
        self.isgoout=[]
        self.outpower=[]
        che=self.cargo[(riqi-1)*60:riqi*60]
        while i<self.num:
            self.isgoout.append(int(che[i][2]))
            self.lefttime.append(che[i][0])
            self.cometime.append(che[i][1])
            self.outpower.append(che[i][3])
            i+=1
        self.offpower=np.zeros(self.num)
        
    def newstate(self):
    #变动新状态
        self.bodong=self.residentload[int(self.ke*4)][1]#+random.uniform(-5,5)
        i=0
        while i<self.num:                               #记录上一个状态，不能直接赋值，不然会有问题
            if self.where[i]==0:
                self.tempwhere[i]=0
            else:
                self.tempwhere[i]=1
            i+=1
        i=0
        while i<self.num:                               #判断电动汽车是否在外
            if self.lefttime[i]>self.ke:
                self.where[i]=0
            elif self.cometime[i]>self.ke:
                self.where[i]=1
            else:
                self.where[i]=0
            i+=1
        i=0
        self.where=list(map(lambda x,y:x*y,self.where,self.isgoout))
        print('是否外出：')
        print(self.where)
        while i<self.num:
            if self.tempwhere[i]!=self.where[i]:    #状态发生改变的
                if self.where[i]==0:                #从外面回来？
                    self.waittime[i]=0
                    self.staytime=list(map(lambda x,y:y-x,self.lefttime,np.ones(self.num)*self.ke))
                else:                               #从小区出去？
                    self.ischarging[i]=0
                    if self.leftpower[i]==1:
                        self.satisfaction[0]+=1
                        self.satisfaction[6]+=1
                    elif self.leftpower[i]>0.9:
                        self.satisfaction[1]+=1
                        self.satisfaction[6]+=1
                    elif self.leftpower[i]>0.8:
                        self.satisfaction[2]+=1
                        self.satisfaction[6]+=1
                    elif self.leftpower[i]>0.7:
                        self.satisfaction[3]+=1
                        self.satisfaction[6]+=1
                    elif self.leftpower[i]>0.6:
                        self.satisfaction[4]+=1
                        self.satisfaction[6]+=1
                    elif self.leftpower[i]<0.2:
                        self.satisfaction[5]+=1
                        self.satisfaction[6]+=1
                    else:
                        self.satisfaction[6]+=1
                    self.leftpower[i]*=self.outpower[i]     #这里重新生成剩余电量，应该以里程来生成，而不是直接乘随机数
                    if self.leftpower[i]<0.1:
                        self.where[i]=0
                        self.waittime[i]+=0.25
                        self.offpower[i]+=1
            else:
                if self.where[i]==0:                    #未外出的
                    if self.ischarging[i]==1:
                        self.leftpower[i]+=self.carimf[i][4]
                        self.waittime[i]=0
                        if self.leftpower[i]>1:
                            self.leftpower[i]=1
                            self.ischarging[i]=0
                    else:
                        if self.isgoout[i]==1:
                            if self.leftpower[i]!=1:
                                self.waittime[i]+=0.25
                else:                                       #外出的
                    self.waittime[i]=0
            i+=1
        print('用户等待时间(小时)：')
        print(self.waittime)
        print('电动汽车剩余电量比例：')
        print(self.leftpower)
        if self.riqi>1:
            if self.longgest<max(self.waittime):
                self.longgest=max(self.waittime)
                self.zuidari=self.riqi
                self.zuidashi=self.ke
        
    def topsis(self):
    #topsis排序
        power=np.ones(self.num)-self.leftpower
        index=[self.waittime,self.staytime,power]
        np.savetxt('index.txt',index)
        index=np.loadtxt('index.txt')                   #因为列表类型的问题，写出再读入就好了，2333333
        #index=list(index)
        print("评估矩阵：")
        print(index)
        a=len(index[0])
        b=len(index)
        pfh=np.empty([b,1])
        i=0;j=0
        ndata=index*index                               
        while j<b :
            pfh[j]=sum(ndata[j])
            j+=1
        j=0
        guiy=np.empty([b,a])
        while i<a :
            while j<b :
                guiy[j][i]=index[j][i]/pfh[j]**0.5
                j+=1
            j=0;i+=1
        print("标准化评估矩阵：")
        print(guiy)
        i=0
        weigf=np.empty([b,a])
        while i<a :
            while j<b :
                weigf[j][i]=self.weight[j]*guiy[j][i]
                j+=1
            j=0;i+=1
        i=0
        print("权重标准化矩阵：")
        print(weigf)
        best=np.empty([b,1])
        worst=np.empty([b,1])
        while j<b :
            best[j]=max(weigf[j])
            worst[j]=min(weigf[j])
            j+=1
        j=0
        print("最优指标值：")
        print(best)
        print("最差指标值：")
        print(worst)
        Dbest=np.zeros(self.num)
        Dworst=np.zeros(self.num)
        while i<a :
            while j<b :
                Dbest[i]+=(best[j]-weigf[j][i])**2
                Dworst[i]+=(worst[j]-weigf[j][i])**2
                j+=1
            j=0;i+=1
        i=0
        Dbest=Dbest**0.5;Dworst=Dworst**0.5
        print("与最优指标的距离：")
        print(Dbest)
        print("与最差指标的距离：")
        print(Dworst)
        cr=np.zeros([a,1])
        while i<a :
            cr[i]=Dworst[i]/(Dbest[i]+Dworst[i])
            i+=1
        i=0
        while i<a :
            if self.ischarging[i]==1:
                cr[i]=0
            if self.where[i]==1:
                cr[i]=0
            if self.leftpower[i]==1:
                cr[i]=0
            i+=1
        i=0
        rank=np.zeros(a)
        while i<self.nengcho :
            lo=cr.argmax()
            if cr[lo]!=0:                
                rank[lo]=i+1
                cr[lo]=0
            i+=1
        print("优先度：")
        print(cr)
        print('topsis排序：')
        print(rank)
        i=0
        if self.nengcho!=0:
            while i<a:
                if rank[i]!=0:
                    self.ischarging[i]=1
                    self.totaltime+=self.waittime[i]
                    self.waittime[i]=0
                i+=1

    def avanum(self):
    #可用充电桩数量
        t=0
        t=sum(self.ischarging)
        self.chargingnum.append(t)
        self.nengcho=np.floor((1000-self.bodong)/9)-t
        if self.nengcho<0:
            self.nengcho=0
        #if self.ke>21 and self.ke<24:
            #self.nengcho=np.round(self.ke%21)
        print('还能充电充电桩个数：%d'%self.nengcho)
        #self.nengcho=60

    def totload(self):
    #记录总负荷
        charging=0;i=0
        while i<self.num:
            if self.ischarging[i]==1:
                charging+=1
            i+=1
        load=7*charging+self.bodong
        self.totalload.append([load,self.bodong])

    def cantout(self):
    #计算不能出行的次数
        i=0
        while i<self.num:
            if self.offpower[i]!=0:
                self.off+=1
            i+=1

    def totprice(self):
    #总充电金额
        prices=0;i=0
        while i<self.num:
            if self.ischarging[i]==1:
                prices+=self.price[int(self.ke*4)][2]*0.25
                prices+=self.sercost*0.25               #服务要不要加？
            i+=1
        self.totalcost+=prices
        self.money.append(self.totalcost)

    def savedata(self):
    #保存数据
        np.savetxt('totalload.txt',self.totalload)
        np.savetxt('chargingnumber.txt',self.chargingnum)
        np.savetxt('totalmoney.txt',self.money)
        np.savetxt('totalcost.txt',[self.totalcost,self.totalcost])     #为什么保存一个数会出错？？
        np.savetxt('satisfaction.txt',self.satisfaction)

       
    
    def Run(self):
    #主程序逻辑
        self.readimf()
        for i in np.linspace(1,self.day,self.day):
            self.riqi=int(i)
            self.newdaystate(self.riqi)
            self.cantout()
            self.ke=0
            print('\n\n第%d天:' % int(i))
            while self.ke<24:
                print('\n时间：第%d天 %2d:%2d\n'% (int(i),int(self.ke),int((60*self.ke)%60)))
                self.newstate()
                self.avanum()

                #if self.ke<22 and self.ke>7:   #是否避开峰时
                if (self.ke>10 and self.ke<15) or (self.ke>18 and self.ke<21):
                    self.ischarging=np.zeros(self.num)
                    self.chargingnum[int(self.ke*4)]=0
                    self.nengcho=0
                if self.nengcho>0:
                    self.topsis()
                print('每个充电桩状态：')
                print(self.ischarging)
                self.totload()
                self.totprice()
                self.ke+=0.25

        ttt=self.totaltime/self.num/self.day
        print('总充电时间：%f'%self.totaltime)
        print('总充电金额：%f'%self.totalcost)
        print('电量耗尽总次数：%d'%self.off)
        print('最长等待时间：%.2f'%self.longgest)
        print('日期：%d，'%self.zuidari,'时间：%.2f'%self.zuidashi)
        print('平均等待时间：%.2f'%ttt)
        print('充电完成情况：')
        print(self.satisfaction)
        self.savedata()

def main():
    AI=AISITERO([0.25,0.25,0.5],60,0.8)
    AI.Run()
if __name__=='__main__':
    main()
