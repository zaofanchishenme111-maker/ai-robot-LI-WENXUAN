## 四足机器人入门 <br>
1. 关节 ID 映射的修正 (Leg Joint Mapping) <br>
在 __init__ 中，修改了四足机器人四个腿部的关节 ID。因为真实 Laikago 模型的每个腿部基座和连杆之间跳过了特定的传感器或特定轴（每条腿占用了4个 ID 间隔）。 <br>
修正为符合 Laikago 真实 URDF 的 ID： <br>
左前 (LF): [0, 1, 2] <br>
左后 (LH): [4, 5, 6] <br>
右前 (RF): [8, 9, 10] <br>
右后 (RH): [12, 13, 14] <br>
2. 引入了真实的几何逆运动学 (Analytical IK) <br>
显式定义了连杆长度：大腿 self.l_thigh = 0.25，小腿 self.l_calf = 0.25。根据目标点 $(x, z)$ 的欧氏距离 $d$，利用余弦定理精确计算出大腿俯仰角（thigh_angle）和小腿俯仰角（calf_angle），并加入了 np.clip 截断防止数学越界。 <br>
3. 步态轨迹与坐标系方向修正 (Gait & Coordinates) <br>
为了让机器狗正常向前走而不是往后退或乱晃，对 trot_gait 函数内部的轨迹方向和坐标符号进行了调整：高度符号对齐：在调用逆运动学时，将 z 取反传入 self.analytical_ik(x, -z)。因为在 PyBullet 坐标系中，足端在身体下方，高度相对于 Hip 应该是负值。 <br>
摆动/支撑相轨迹微调：摆动相的 $x$ 轴移动方向进行了对调，变更为 self.step_length * (0.5 - progress)。支撑相的 $x$ 轴移动中心点变更为 (progress - 0.8)，用于微调机器狗的身体重心。 <br>
4. 右侧腿部关节镜像反向 (Mirroring for Right Legs) <br>
对称结构机器人在控制时，左右两侧电机的正方向往往是相反的 <br>
5. 动力学参数与控制循环微调 (Physics Tuning) <br>
为了能让机器人稳稳地站起来并克服摩擦力，对控制层的物理参数进行了放大： <br>

增大电机驱动力：在 p.setJointMotorControl2 中，将最大控制力 force 从原来的 20 提升到了 40。 <br>

调整步态基础参数： <br>

站立高度 stance_height 从 0.3 提高到 0.38（防止肚皮贴地）。 <br>

抬腿高度 step_height 从 0.05 降低到 0.03，步长 step_length 从 0.1 缩小到 0.04（动作变柔和，小碎步更加防滑稳健）。 <br>
![这是效果图](1.png) <br>