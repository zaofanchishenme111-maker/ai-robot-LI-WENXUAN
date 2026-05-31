## 第12周：手机摄像头、ArUco 识别与距离测量 <br>
# 第一部分：将手机摄像头作为输入，连入 WSL 系统 <br>
1.在 WSL 中命令行安装 Tailscale <br>
在开始 WSL 端安装之前，手机端也要先做一个很简短的准备： <br>

iPhone / iPad：在 App Store 安装 Tailscale <br>
Android：在应用商店安装 Tailscale <br>
手机端登录时，使用和电脑端 同一个账号 <br>
第一次打开时允许 VPN 或网络扩展权限 <br>
手机端这一步不需要复杂配置，先保证两件事即可： <br>

手机上已经安装并登录 Tailscale :<br>
后面能和 WSL 出现在同一个 Tailnet 中 <br>
本课程统一使用 WSL 命令行 安装，不依赖图形界面。 <br>

curl -fsSL https://tailscale.com/install.sh | sh <br>
sudo service tailscaled start <br>
sudo tailscale up <br>
执行 sudo tailscale up 后，按照终端提示登录自己的账号。  <br>

这里登录的账号应当与手机端保持一致。 <br>

查看当前网络状态： <br>

tailscale status <br>
tailscale ip -4 <br>
2.加上 SSH 登录学习测试 <br>
既然手机和 WSL 已经通过 Tailscale 进入同一个虚拟网络，本周可以顺手做一个很有工程味的验证： <br>

除了“拉视频流”，这个网络还能不能让我们对 WSL 进行远程登录？ <br>

这一步的目的不是让手机作为主要开发终端，而是让大家理解： <br>

Tailscale 不只是给摄像头用 <br>
它本质上是在打通设备与设备之间的网络连接 <br>
打通之后，视频流、SSH、HTTP 服务都可以复用这条链路 <br>
先在 WSL 里安装 SSH 服务： <br>

sudo apt update <br>
sudo apt install openssh-server -y <br>
sudo service ssh start <br>
确认 SSH 服务正在监听： <br>

sudo service ssh status <br>
ss -tlnp | grep :22 <br>
然后查看 WSL 在 Tailscale 中的地址： <br>

tailscale ip -4 <br>
![这是效果图](1.jpg)