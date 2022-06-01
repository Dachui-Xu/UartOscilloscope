# 项目说明
X-Y串口示波器，传统的显示是X轴是点数（时间），y轴是数据；  
## 起因
我在网上苦苦找寻了很久能把两个数据整合到x-y的方法，无果，所以自己做一个。
## 实现方案
本来只想开个数据线程，主线程走数据绘图，没有UI还好说，UI复杂后反而不好实现，所以就开了两个QTime线程，为了保险时间都是20ms，我也无法确定两个的时间间隔改变会不会出现数据BUG
# 数据格式
单片机输出数据：x,y\n或者x,y\rn  
串口显示数据：x,y
# 其他
那个HEX，就是显示16进制的代码我删除了，但UI上选项没有删除，因为本项目是实现串口数据绘图，意义不大，我也懒得改UI或者加代码。  
# 碎碎念
其实是要做一个电化学上位机工作站，但是还没弄完，就把其中的一部分拿出来，就成了这种串口示波器，感觉这还是挺通用的。
最后的最后，我想说Python果然是世界上最好的语言！！！我开始用C++写了一个问题又多，代码看起量还挺大。
Python的缺点就是打包的.exe文件有点大，内存占用大。