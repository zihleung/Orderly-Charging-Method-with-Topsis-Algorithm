# 居民区停车场 *Topsis* 有序充电仿真
*Power by **zihl.kdt***  

！文件说明：
- [*"Simulation.md"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/Simulation.md) 为代码解析说明文档
- [*"仿真过程.py"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/%E4%BB%BF%E7%9C%9F%E8%BF%87%E7%A8%8B.py) 为仿真过程代码
- [*"cargo.txt"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/cargo.txt) 为随机生成的电动汽车出行数据，格式为[离开时间，回来时间，是否出行，剩余电量百分比]，其中*是否出行* *1*表示出行，*0*表示不出行
- [*"cargo.py"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/cargo.py) 为生成电动汽车出行数据代码
- [*"carimf.txt"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/carimf.txt) 为电动汽车信息初始化数据，格式为[序号，电池容量，慢充时间，最大行驶里程，慢充每15分钟增加电量百分比]
- [*"price.txt"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/price.txt) 为时间价格表，格式为[时间，时段，电价]，其中，时段*1*表示峰时，时段*2*表示谷时，时段*3*表示平时
- [*"drawpic.py"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/drawpic.py) 为绘图函数
- [*"小区居民日常负荷数据.txt"*](https://github.com/zihleung/Orderly-Charging-Method-with-Topsis-Algorithm/blob/master/%E5%B0%8F%E5%8C%BA%E5%B1%85%E6%B0%91%E6%97%A5%E5%B8%B8%E8%B4%9F%E8%8D%B7%E6%95%B0%E6%8D%AE.txt) 为通过蒙特卡洛方法生成的小区居民日常负荷数据
