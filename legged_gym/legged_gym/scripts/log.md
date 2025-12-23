## log
## note
```bash
# cuda:1
CUDA_VISIBLE_DEVICES=1 python3 train.py

# watch gpu
gpustat -i 1

# tmux
tmux new -s go1_train
tmux attach -t go1_train
```

### base
- 1117
```bash
python3 train.py --headless --task go1 --max_iterations 2000 --resume --sim_device cuda:0 --load_run Nov14_10-07-07_ --seed 66 --num_envs 8192

python3 play.py --headless --task go1 --sim_device cuda:0 --load_run Nov17_10-32-33_ --checkpoint 12500
```

- 1119
```txt
change
```
```python
class control( LeggedRobotCfg.control ):
    # PD Drive parameters:
    control_type = 'P'
    stiffness = {'joint': 20.}
    damping = {'joint': 0.5}
    # action scale: target angle = actionScale * action + defaultAngle
    action_scale = 0.25
    # decimation: Number of control action updates @ sim DT per policy DT
    decimation = 4

class asset( LeggedRobotCfg.asset ):
    file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/go1/urdf/go1.urdf'
    name = "go1"
    foot_name = "foot"
    penalize_contacts_on = ["thigh", "calf"]
    terminate_after_contacts_on = ["base"]
    self_collisions = 1 # 1 to disable, 0 to enable...bitwise filter
```

```bash
python3 train.py --headless --task go1 --max_iterations 3000 --sim_device cuda:0 --seed 1 --num_envs 8192
```

- 1201
```bash
CUDA_VISIBLE_DEVICES=1 python3 train.py --headless --task go1 --max_iterations 3000 --seed 1

python3 play.py --headless --task go1 --load_run Dec01_02-03-31_ --checkpoint 10000
```

- 1204  
```txt
change like 1119
```
```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec04_08-35-35_ --checkpoint 3000
```

- 1208
```txt
替换成新的 go1.urdf，和 unitree 官方保持一致  
NOTE: 如果后面未提及 urdf，均与该日期的 urdf 保持一致  
change like 1119  
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192  --run_name kp20

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec08_03-51-52_kp20 --checkpoint 4800
```

```txt
对比1208, 仅改变 kp=40, kd=1
```
```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 -run_name kp40
```

- 1209
```txt
kp=20,kd=0.5

randomize_motor_strength = True
motor_strength_range = [0.9, 1.1]

NOTE: 表现正常
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name random_motor_strength
```

- 1210
```txt
resume 1209

NOTE：震荡
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --resume --load_run Dec09_06-58-12_random_motor_strength --seed 1 --num_envs 8192

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec10_03-27-11_ --checkpoint 10000
```

- 1210-1
```txt
change from 1209

NOTE: 失败
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name domain_rand_v1

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec10_10-25-50_domain_rand_v1 --checkpoint 4800
```

- 1211
```txt
like 1209, but:
num_rows= 6 # number of terrain rows (levels)
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec11_03-39-53_ --checkpoint 5000
```

- 1212
```txt
kp_range = [0.8, 1.2]
kd_range = [0.8, 1.2]
num_rows= 6 

NOTE：不好说
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec12_03-38-39_ --checkpoint 4900
```

- 1213
```txt
max_curriculum = 3.0
num_rows= 6

NOTE：失败，发散
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192
```

- 1213
```txt
randomize_link_mass = True
num_rows= 6

NOTE: 表现正常
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name link_mass_rand

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec13_08-20-10_link_mass_rand --checkpoint 3300
```

- 1214
```txt
randomize_link_mass = True
num_rows= 6

max_curriculum = 1.5

NOTE: 没有发散，但髋关节偏移
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name lmr_1d5

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec14_03-22-06_lmr_1d5 --checkpoint 4600
```

- 1215
```txt
randomize_link_mass = True
num_rows= 6

max_curriculum = 1.5

randomize_restitution = True
dof_pos_limits = -0.01
dof_vel_limits = -0.01
torque_limits = -0.001
```

```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name pl_rr
```

- 1215-1
```txt
修改为分层命令课程

randomize_link_mass = True
num_rows= 6

max_curriculum = 3
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name part_cmds
```

- 1216
```txt
更新分层命令课程
--resume --load_run Dec13_08-20-10_link_mass_rand --checkpoint 2000

randomize_link_mass = True
num_rows= 6
max_curriculum = 3
resampling_time = 25. 
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name part_cmds1 --resume --load_run Dec13_08-20-10_link_mass_rand --checkpoint 2000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec16_05-52-49_part_cmds1 --checkpoint 500
```

- 1216-1
```txt
和1216一致的速度课程

randomize_link_mass = True
num_rows= 6
max_curriculum = 2
resampling_time = 25. 

default_joint_angles = { # = target angles [rad] when action = 0.0
    'FL_hip_joint': 0.0,   # [rad]
    'RL_hip_joint': 0.0,   # [rad]
    'FR_hip_joint': -0.0,  # [rad]
    'RR_hip_joint': -0.0,   # [rad]

    'FL_thigh_joint': 0.8,     # [rad]
    'RL_thigh_joint': 0.8,   # [rad]
    'FR_thigh_joint': 0.8,     # [rad]
    'RR_thigh_joint': 0.8,   # [rad]

    'FL_calf_joint': -1.5,   # [rad]
    'RL_calf_joint': -1.5,    # [rad]
    'FR_calf_joint': -1.5,  # [rad]
    'RR_calf_joint': -1.5,    # [rad]
}

说明: 2200 后 rew_base_height 震荡
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name pc_mc2

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec16_09-07-55_pc_mc2 --checkpoint 4500
```

- 1216-2
```txt
和1216一致的速度课程
--resume --load_run Dec16_05-52-49_part_cmds1 --checkpoint 500

randomize_link_mass = True
num_rows= 6
max_curriculum = 2
resampling_time = 25. 
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name part_cmds2 --resume  --load_run Dec16_05-52-49_part_cmds1 --checkpoint 500

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec16_09-25-58_part_cmds2 --checkpoint 4700
```

- 1217
```txt
更新为 flat、rough flat 速度课程
--resume --load_run Dec16_09-07-55_pc_mc2 --checkpoint 2200

default_joint_angles 0 化
randomize_link_mass = True
num_rows= 6
max_curriculum = 2
resampling_time = 25. 

generator = 'flat_mix' # add flat/rough-flat into terrain mix

NOTE：后期震荡
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name flat_cmds --resume  --load_run Dec16_09-07-55_pc_mc2 --checkpoint 2200
```

- 1217-1
```txt
速度课程和 1216 一致
--resume --load_run Dec16_09-07-55_pc_mc2 --checkpoint 2200

default_joint_angles 0 化
randomize_link_mass = True
num_rows= 6
max_curriculum = 1.5
resampling_time = 25. 

NOTE: gap 失败
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name pc_mc1d5 --resume  --load_run Dec16_09-07-55_pc_mc2 --checkpoint 2200

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec17_05-36-50_pc_mc1d5 --checkpoint 1500
```

- 1217-2
```txt
相比 1217-1

base_height = -3.0

NOTE: gap 失败
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name pc_mc1d5_h3 --resume  --load_run Dec16_09-07-55_pc_mc2 --checkpoint 2200

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec17_05-57-38_pc_mc1d5_h3 --checkpoint 1300
```

- 1218
```txt
default_joint_angles 回归正常

randomize_link_mass = True
num_rows= 6
max_curriculum = 1.5
resampling_time = 25. 
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name n1d5

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec18_02-11-29_n1d5 --checkpoint 1300
```

- 1218-1
```txt
 --resume  --load_run Dec13_08-20-10_link_mass_rand --checkpoint 2000

use_terrain_aware_commands = True
randomize_link_mass = True
num_rows= 6
max_curriculum = 1.5
resampling_time = 25. 
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name n1d5_re --resume  --load_run Dec13_08-20-10_link_mass_rand --checkpoint 2000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec18_05-36-57_n1d5_re --checkpoint 1000
```

- 1218-2
```txt
--resume  --load_run Dec11_03-39-53_ --checkpoint 5000

max_forward_curriculum = 1.5  # x_vel 限制 [-1.0, 1.5]
max_backward_curriculum = 1.0
max_lat_curriculum = 1.0  # y_vel 限制 [-1.0, 1.0]

randomize_link_mass = False
base_height = -5.0

# more
hip_pos = -0.12
thigh_pose = -0.05
calf_pose = -0.03

NOTE： 抗扰能力下降
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit --resume  --load_run Dec11_03-39-53_ --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec18_10-11-21_p_limit --checkpoint 5300
```

- 1218-3
```txt
--resume  --load_run Dec11_03-39-53_ --checkpoint 5000
奖励设置太复杂，基本参考 aliengo_stairs_config

NOTE: sim2real 有前倾趋势
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name a_stairs --resume  --load_run Dec11_03-39-53_ --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec18_15-24-59_a_stairs --checkpoint 5200
```

- 1219
```txt
--resume  --load_run Dec11_03-39-53_ --checkpoint 5000
class scales:
    termination = -0.0
    tracking_lin_vel = 1.0
    tracking_ang_vel = 0.5
    lin_vel_z = -2.0
    ang_vel_xy = -0.05
    orientation = -0.2
    dof_acc = -2.5e-7
    joint_power = -2e-5
    base_height = -5.0
    foot_clearance = -0.01
    action_rate = -0.01
    smoothness = -0.01
    feet_air_time =  0.1
    collision = -0.0
    feet_stumble = -0.0
    stand_still = -0.
    torques = -0.0
    dof_vel = -0.0
    dof_pos_limits = -0.01
    dof_vel_limits = -0.01
    torque_limits = -1e-3
    # more
    hip_pos = -0.08
    thigh_pose = -0.03
    calf_pose = -0.01
    feet_contact_forces = -0.00015

only_positive_rewards = False # if true negative total rewards are clipped at zero (avoids early termination problems)
tracking_sigma = 0.20 # tracking reward = exp(-error^2/sigma)
soft_dof_pos_limit = 1. # percentage of urdf limits, values above this limit are penalized
soft_dof_vel_limit = 1.
soft_torque_limit = 1.
base_height_target = 0.30
max_contact_force = 100. # forces above this value are penalized
clearance_height_target = -0.20
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit1 --resume  --load_run Dec11_03-39-53_ --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec19_01-54-34_p_limit1 --checkpoint 5300
```

- 1219-1
```txt
like 1219, but:
    resume  him1214_lmr_2000.pt
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit2 --resume  --load_run Dec13_08-20-10_link_mass_rand --checkpoint 2000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec19_03-48-03_p_limit2 --checkpoint 500
```

- 1219-2
```txt
like 1219, but:
    resume  him1214_lmr_2000.pt
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit2 --resume  --load_run Dec13_08-20-10_link_mass_rand --checkpoint 2000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec19_03-48-03_p_limit2 --checkpoint 500
```

- 1219-2
```txt
like 1219, but:
    no resume
num_rows= 10
feet_air_time =  0.0
base_height = -2.0

hip_pos = -0.04
thigh_pose = -0.02
calf_pose = -0.005

NOTE: 往后撅屁股
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit3

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec19_10-07-11_p_limit3
```

- 1219-3
```txt
like 1219-2, but:
    base_height = -1.5
    hip_pos = -0.03
    # thigh_pose = -0.02
    # calf_pose = -0.005

NOTE: 稳定性欠佳
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit4

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec19_15-01-06_p_limit4
```

- 1220
```txt
like 1219-3, but:
    randomize_link_mass = True
    link_mass_range = [0.9, 1.1]

NOTE: 脚有内缩趋势
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit5

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec20_03-10-11_p_limit5
```

- 1221
```txt
like 1220, but:
    randomize_kp = True
    kp_range = [0.8, 1.2]
    
    randomize_kd = True
    kd_range = [0.8, 1.2]

NOTE: 压低姿态
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit6

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec21_01-54-19_p_limit6
```

- 1221-1
```txt
like 1220, but:
    stiffness = {'joint': 30.}
    damping = {'joint': 0.75}

NOTE: 姿态奇怪
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit7

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec21_02-01-17_p_limit7
```

- 1222
```txt
like 1219-3, but:
    randomize_kp = True
    kp_range = [0.8, 1.2]
    
    randomize_kd = True
    kd_range = [0.8, 1.2]
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit8
```

- 1222-1
```txt
like 1219-3, but:
    randomize_kp = True
    kp_range = [0.8, 1.2]
    
    randomize_kd = True
    kd_range = [0.8, 1.2]

    randomize_motor_strength = False 
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit9
```

- 1222-2
```txt
--resume  --load_run Dec19_15-01-06_p_limit4 --checkpoint 5000
like 1219-3, but:
    payload_mass_range = [-1, 3]
    friction_range = [0.2, 2.75]
NOTE: 稳定性进一步下降
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit10 --resume  --load_run Dec19_15-01-06_p_limit4 --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec22_09-16-41_p_limit10
```

- 1222-3
```python
stiffness = {'joint': 30.}
damping = {'joint': 0.75}
class domain_rand( LeggedRobotCfg.domain_rand ):
        randomize_payload_mass = True
        payload_mass_range = [-1, 3]

        randomize_com_displacement = True
        com_displacement_range = [-0.05, 0.05]

        randomize_link_mass = False
        link_mass_range = [0.9, 1.1]
        
        randomize_friction = True
        friction_range = [0.2, 2]
        
        randomize_restitution = False
        restitution_range = [0., 1.0]
        
        randomize_motor_strength = True
        motor_strength_range = [0.9, 1.1]
        
        randomize_kp = True
        kp_range = [0.8, 1.2]
        
        randomize_kd = True
        kd_range = [0.8, 1.2]
        
        randomize_initial_joint_pos = True
        initial_joint_pos_range = [0.5, 1.5]
        
        disturbance = True
        disturbance_range = [-30.0, 30.0]
        disturbance_interval = 8
        
        push_robots = True
        push_interval_s = 16
        max_push_vel_xy = 1.

        delay = True

class rewards( LeggedRobotCfg.rewards ):
    class scales:
        termination = -0.0
        tracking_lin_vel = 1.0
        tracking_ang_vel = 0.5
        lin_vel_z = -2.0
        ang_vel_xy = -0.05
        orientation = -0.2
        dof_acc = -2.5e-7
        joint_power = -2e-5
        base_height = -5
        foot_clearance = -0.01
        action_rate = -0.01
        smoothness = -0.01
        feet_air_time =  0.0
        collision = -0.0
        feet_stumble = -0.0
        stand_still = -0.
        torques = -0.0
        dof_vel = -0.0
        dof_pos_limits = -0.01
        dof_vel_limits = -0.01
        torque_limits = -1e-3
        # more
        # hip_pos = -0.03
        # thigh_pose = -0.02
        # calf_pose = -0.005
        feet_contact_forces = -0.00015

    only_positive_rewards = False # if true negative total rewards are clipped at zero (avoids early termination problems)
    tracking_sigma = 0.20 # tracking reward = exp(-error^2/sigma)
    soft_dof_pos_limit = 1. # percentage of urdf limits, values above this limit are penalized
    soft_dof_vel_limit = 1.
    soft_torque_limit = 1.
    base_height_target = 0.30
    max_contact_force = 100. # forces above this value are penalized
    clearance_height_target = -0.20

NOTE： 关节欠佳
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit11 

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec22_10-45-03_p_limit11
```

- 1222-4
```txt
like 1222-3, but:
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]

NOTE: 关节欠佳
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit12 

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec22_14-14-52_p_limit12
```

- 1223
```txt
like 1219-3,
 --resume  --load_run Dec19_15-01-06_p_limit4 --checkpoint 5000
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit4d1 --resume  --load_run Dec19_15-01-06_p_limit4 --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec23_01-41-25_p_limit4d1 --checkpoint 6000
```

- 1223-1
```txt
like 1220, but:
    base_height = -3
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit5d1 --resume  --load_run Dec20_03-10-11_p_limit5 --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit5d1 --resume  --load_run Dec23_05-50-12_p_limit5d1

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec23_07-15-16_p_limit5d1 --checkpoint 6000
```

- 1223-2
```txt
like 1220, but:
    base_height = -3
    trot = 0.1
    cycle_time=0.5
 --resume  --load_run Dec23_07-15-16_p_limit5d1 --checkpoint 7200
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name phase --resume  --load_run Dec23_07-15-16_p_limit5d1 --checkpoint 7200
```

- 1223-2
```txt
like 1220, but:
    base_height = -3
    trot = 0.1
    cycle_time=0.5
no resume
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name phase1
```