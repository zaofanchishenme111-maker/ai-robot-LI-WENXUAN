import pybullet as p
import pybullet_data
import time
import numpy as np
import math

class QuadrupedController:
    """优化后的四足机器人控制器（适配 Laikago 真实关节）"""

    def __init__(self, robot_id):
        self.robot_id = robot_id

        # Laikago 真实的关节 ID 映射
        # 每个腿依次为：Hip（侧摆）, Thigh（大腿俯仰）, Calf（小腿俯仰）
        self.leg_joints = {
            'LF': [0, 1, 2],    # 左前
            'LH': [4, 5, 6],    # 左后
            'RF': [8, 9, 10],   # 右前
            'RH': [12, 13, 14]  # 右后
        }

        # 连杆长度（Laikago 的近似物理参数）
        self.l_thigh = 0.25
        self.l_calf = 0.25

        # 步态参数
        self.stance_height = 0.38  # 站立高度（稍微加高，防止肚皮贴地）
        self.step_height = 0.03    # 抬腿高度
        self.step_length = 0.04    # 步长（不宜过大，否则容易滑倒）

    def analytical_ik(self, x, z):
        """二维几何逆运动学计算 (计算大腿和小腿角度)"""
        # 目标点到髋关节的距离
        d = np.sqrt(x**2 + z**2)
        if d > (self.l_thigh + self.l_calf):
            d = self.l_thigh + self.l_calf

        # 余弦定理计算
        cos_calf = (self.l_thigh**2 + self.l_calf**2 - d**2) / (2 * self.l_thigh * self.l_calf)
        cos_calf = np.clip(cos_calf, -1.0, 1.0)
        calf_angle = np.pi - np.arccos(cos_calf)  # 小腿通常向后弯曲

        # 大腿角度计算
        alpha = np.arctan2(x, z)
        cos_alpha2 = (self.l_thigh**2 + d**2 - self.l_calf**2) / (2 * self.l_thigh * d)
        cos_alpha2 = np.clip(cos_alpha2, -1.0, 1.0)
        alpha2 = np.arccos(cos_alpha2)
        
        thigh_angle = alpha + alpha2
        
        return thigh_angle, calf_angle

    def trot_gait(self, t, leg_name, frequency=1.5):
        """Trot 步态轨迹生成"""
        # 对角腿同相
        if leg_name in ['LF', 'RH']:
            phase = 0
        else:
            phase = np.pi

        # 步态周期位置
        cycle_phase = (2 * np.pi * frequency * t + phase) % (2 * np.pi)

        # 轨迹计算 (x 为前后移动，z 为相对于基座的垂向高度)
        if cycle_phase < np.pi:  # 摆动相（腿抬起向前推进）
            progress = cycle_phase / np.pi
            x = self.step_length * (0.5 - progress)  # 从后向前摆动
            z = self.stance_height - self.step_height * np.sin(np.pi * progress)
        else:  # 支撑相（腿着地向后推，驱动身体向前）
            progress = (cycle_phase - np.pi) / np.pi
            x = self.step_length * (progress - 0.8)  # 从前向后支撑
            z = self.stance_height

        # 核心：计算逆运动学角度
        thigh, calf = self.analytical_ik(x, -z)
        
        # Hip 关节保持 0（不侧摆），只靠大腿和小腿前后走动
        hip = 0.0 
        
        return [hip, thigh, calf]

    def step(self, t, frequency=0.8):
        """执行一步控制"""
        for leg_name, joint_ids in self.leg_joints.items():
            target_angles = self.trot_gait(t, leg_name, frequency)

            # Laikago 的右侧腿结构镜像，关节方向需要取反
            if leg_name in ['RF', 'RH']:
                target_angles[1] = -target_angles[1] # 大腿
                target_angles[2] = -target_angles[2] # 小腿

            for joint_id, angle in zip(joint_ids, target_angles):
                p.setJointMotorControl2(
                    self.robot_id,
                    joint_id,
                    p.POSITION_CONTROL,
                    targetPosition=angle,
                    force=40  # 增大电机驱动力，确保能支撑起身体
                )

def main():
    # 初始化 PyBullet
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")

    # 修正初始姿态：让机器狗平正地出生在空中，然后落到地面站立
    # 移除原先不必要的 math.pi / 2 翻转
    start_orientation = p.getQuaternionFromEuler([math.pi / 2, 0, math.pi / 2]) # Keeps the robot facing forward
    robotId = p.loadURDF("laikago/laikago_toes.urdf", [0, 0, 0.5],start_orientation)

    # 创建控制器
    controller = QuadrupedController(robotId)

    # 仿真参数
    t = 0
    dt = 1./240.

    print("开始仿真，机器狗即将起立并走动... 按Ctrl+C停止")

    try:
        while True:
            # frequency 控制走动速度，1.5Hz 是一个比较稳定的频率
            controller.step(t, frequency=1.5)
            p.stepSimulation()
            time.sleep(dt)
            t += dt

    except KeyboardInterrupt:
        print("仿真结束")

    p.disconnect()

if __name__ == '__main__':
    main()