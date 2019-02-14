要满足最后官方规定的比赛要求，就必须使用加入视觉辅助了，同时芯片加多了一块，方便拓展和满足比赛要求

整体设计可分为识别和控制部分

+ all
  + control
    + move
    + pick up
      + up and down
      + clamp and loosen
  + recognition
    + blue
    + red

控制部分动作取决于结构设计，结构图[这里看](https://github.com/Docupa/little_mv/tree/master/structure)

电路帮助芯片控制，电路图[这里看](https://github.com/Docupa/little_mv/tree/master/circuit)

整体采用两个芯片，分别负责对应的工作

+ chip
  + stm32F1
    + pick up
  + openmv
    + move
    + recognition

移动控制交给 openmv 模块的原因是避免使用耗时更长的通讯方式，捡取动作可以通过 4 个高低电平控制即可

程序流程

启动 -----> ②寻找目标 -----> 移动 -----> 夹取 -----> 寻找目标 -----> 移动 -----> 释放 -----> ②

具体代码，[这里看](https://github.com/Docupa/little_mv/tree/master/code)
