算法概述：

该算法是一个求最短路径的算法，具体算法的思想为：

1. 找出离源点O最近的点，把该点设为S；
2. 以S点为中转点，查看如果以S点为中转点，计算源点O中转S点到各点的距离transfer_distance；
3. 对比O到各点的距离对比transfer_distance，如果transfer_distance距离更短，则把S点到该点的距离调整为transfer_distance；
4. 将S点标注为已算，计算下个个点S2，重复步骤2

算法具体计算过程：

1. 计算邻接矩阵$A$，$A_{ij}$为点i到点j的最短路径距离；
2. 源点i，对应邻接矩阵$A$所在的$i$行，为点i到其他各点的距离；
3. 找到该行中距离$i$最近的点$j$，并将j列为已计算的点，下次不再计算；
4. 以$j$为中转站，计算$i$到各点的距离，如果距离小于之前已有的最短距离，则更新该点的数据；
5. 更新完数据后，重复3，4两步；
6. 最终得到$i$点到其他各点的最短距离。

为了更好的理解该算法，本文打算以上海地铁中转为例，通过代码将以上的算法实现。

需要注意的是：

1. 地铁线路之间存在换乘时间，该时间也应该计算在总路程之内；
2. 初始化邻接矩阵的时候，计算两点间最短距离时，两点应处在同一条线路。

