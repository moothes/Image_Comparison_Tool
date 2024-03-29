图片可视化工具文档  
===
[English README](https://github.com/moothes/Image_Comparison_Tool/blob/master/README_en.md)  

主要用于对比多个文件夹的图片。 

使用方法概述：  
----
Blocks是设置展示的文件夹数量，可以动态调整；  
Save_path设置保存图片路径。
* 完成设置后，主页面如下图：  
![](https://github.com/moothes/Image_Comparison_Tool/blob/master/image.PNG)  
每个小图片右上角的set是设置文件夹，第一个图片必须要设置，用于加载图片列表和计算IOU;  
键盘的左右键可以控制上下一张图片。选取图片后，可用键盘上的“S”键保存到Save_path; 
在任意一张图片上进行点击可以画图，同时在其它所有图片上相同位置也会画出来  

**注意**
每个图片的文件夹最后一级最好用方法名称命名，不然可能会影响保存的结果。同时每个文件夹下相同图片的**名称**和**后缀**要保持完全一致，否则读不到图片。  
最新版已支持不同文件夹下png和jpg文件同时读取。

推荐的文档结构
----
* Folder
  * method 1
    * img_1.jpg
    * img_2.jpg 
    * ...
    * img_n.jpg 
  * method 2
    * img_1.png
    * img_2.png 
    * ...
    * img_n.png 
  * ...

**对于程序有建议或者BUG欢迎提出来，我会尽快解决**
