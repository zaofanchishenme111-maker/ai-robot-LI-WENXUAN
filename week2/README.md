## Week2：ROS2基本命令介绍和通信机制基础 <br>
下载Ubuntu22.04 <br>
安装ROS2 <br>
sudo apt update <br>
sudo apt install ros-humble-desktop <br>
2.2.5 验证ROS2安装 <br>
实验内容： <br>
本周学习了 ROS2 的基本命令，并使用 turtlesim 小乌龟完成简单运动控制实验。openclaw与飞书连接 <br>
实验命令 <br>
启动环境： <br>

source /opt/ros/rolling/setup.bash <br>

启动小乌龟： <br>

ros2 run turtlesim turtlesim_node <br>

查看节点： <br>

ros2 node list <br>

查看话题： <br>

ros2 topic list <br>

监听位置： <br>

ros2 topic echo /turtle1/pose <br>

画圆： <br>

ros2 topic pub --rate 10 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.0}}" <br>
![这是效果图](1.png)
![这是效果图](2.png)