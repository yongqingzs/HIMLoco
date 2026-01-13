- 1231
```python
class domain_rand( LeggedRobotCfg.domain_rand ):
    randomize_payload_mass = True
    payload_mass_range = [-1, 2]

    randomize_com_displacement = True
    com_displacement_range = [-0.05, 0.05]

    randomize_base_mass = False
    base_mass_range = [0.9, 1.1]
    
    randomize_link_mass = True
    link_mass_range = [0.9, 1.1]
    
    randomize_friction = True
    friction_range = [0.2, 1.25]
    
    randomize_restitution = False
    restitution_range = [0., 1.0]
    
    randomize_motor_strength = True
    motor_strength_range = [0.8, 1.2]
    
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

    # delay = True
    # Lag timesteps (motor delay simulation using buffer)
    randomize_lag_timesteps = True
    lag_timesteps = 6  # Number of timesteps to delay (buffer size - 1)

class rewards( LeggedRobotCfg.rewards ):
    "reward 0"
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
        # only one
        foot_clearance = -0.0
        action_rate = -0.01
        smoothness = -0.01
        feet_air_time = 1
        collision = -0.0
        feet_stumble = -0.0
        stand_still = -0.
        torques = -0.0
        dof_vel = -0.0
        dof_pos_limits = -0.01
        dof_vel_limits = -0.01
        torque_limits = -1e-3
        # more
        hip_pos = -0.05
        thigh_pose = -0.01
        calf_pose = -0.01
        feet_contact_forces = -0.00015
        trot = 0.0
        # foot_mirror_up = -0.05
        feet_mirror = -0.1
        # foot_slide_up = -0.03

    only_positive_rewards = False # if true negative total rewards are clipped at zero (avoids early termination problems)
    tracking_sigma = 0.25 # tracking reward = exp(-error^2/sigma)
    soft_dof_pos_limit = 0.9 # percentage of urdf limits, values above this limit are penalized
    soft_dof_vel_limit = 1.
    soft_torque_limit = 1.
    base_height_target = 0.28
    max_contact_force = 100. # forces above this value are penalized
    clearance_height_target = -0.22
    cycle_time=0.5  # for trot

NOTE: 能保持 ≥ 1 m/s 的速度，且机身较为稳定; 爬楼梯还行
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name mr_lag

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Dec31_05-32-00_mr_lag
```

- 101
```txt
only resume Dec31_05-32-00_mr_lag

NOTE: 
1. 能保持 ≥ 1 m/s 的速度，且机身较为稳定; 爬楼梯还行
2. 运动时出现初始几步不动的情况
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name mr_lagd1 --resume   --load_run Dec31_05-32-00_mr_lag --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan01_02-42-38_mr_lagd1

# resume more iter from Jan01_02-42-38_mr_lagd1 10000
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lagd1d1 --resume  --load_run Jan01_02-42-38_mr_lagd1 --checkpoint 10000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan06_10-41-48_mr_lagd1d1  --checkpoint 19200
```

- 101-1
```txt
like 1231, but:
    foot_clearance = -0.01
    feet_air_time = 0

NOTE: 
1. 8500 低速时比 feet_air_time 表现更好，但收敛更慢
2. 13000 低速表现更差，0.2 几乎不动
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 8000 --seed 1 --num_envs 4096 --run_name mr_lag1

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan01_13-42-39_mr_lag1

# more iter from Jan01_13-42-39_mr_lag1 8000
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name mr_lag1d1 --resume   --load_run Jan01_13-42-39_mr_lag1 --checkpoint 8000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan05_09-53-08_mr_lag1d1
```

- 102
```txt
like 1231, but:
    thigh_pose = -0.00
    calf_pose = -0.00

NOTE: 影响不大, 7300 姿态很低
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 8000 --seed 1 --num_envs 4096 --run_name mr_lag2

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan02_02-10-05_mr_lag2
```

- 104
```txt
like 1231, but:
    motor_strength_range = [0.9, 1.1]
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]

NOTE: kp kd 域随机化降低似乎会使鲁棒性下降
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag3

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan04_02-54-16_mr_lag3
```

- 105
```txt
like 1231, but:
    motor_strength_range = [0.9, 1.1]
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]
    foot_clearance = -0.01
    feet_air_time = 0
NOTE: 
1. 有些反直觉，feet_air_time 会大幅促进当前配置下的收敛
2. 当前仅能收敛到5.8
3. 低速时表现很差，呈现迈不动腿的情况，说明迈不动腿不是来自 feet_air_time
```
```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag5

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan05_10-01-24_mr_lag5
```

- 106
```txt
like 1231, but:
    control_type = 'actuator_net'
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag6
```

- 107
```txt
like 1231, but:
    motor_strength_range = [0.9, 1.1]
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]
    thigh_pose = -0.0
    calf_pose = -0.0

feat: 机身高度偏低，和 kp = [0.8, 1.2] 类似，但低速时表现更好些(不会像卡壳了一样)
```
```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag7

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan07_01-31-18_mr_lag7
```

- 109
```txt
like 1231, but:
    motor_strength_range = [0.9, 1.1]
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]
    # hip_pos = -0.05
    # thigh_pose = -0.01
    # calf_pose = -0.01
    hip_pos0 = -0.05
    thigh_pose0 = -0.01
    calf_pose0 = -0.01

NOTE： 
1. 新的 hip_pos0 等可以有效降低低速时僵硬
2. 10000 时出现一次震荡，从 9000 开始 resume(怀疑是 terrain level 继续上升导致)
3. resume 后继续训练到 19000，表现稳定，高度相比 1231 提高
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag8

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan09_01-34-04_mr_lag8 --checkpoint 9000

# more iter from Jan09_01-34-04_mr_lag8 9000
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag8d1 --resume   --load_run Jan09_01-34-04_mr_lag8 --checkpoint 9000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1 --load_run Jan10_14-04-30_mr_lag8d1 --checkpoint 10000
```

- 109-1
```txt
like 1231, but:
--resume  --load_run Jan04_02-54-16_mr_lag3 --checkpoint 10000
    motor_strength_range = [0.9, 1.1]
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]
    # hip_pos = -0.05
    # thigh_pose = -0.01
    # calf_pose = -0.01
    hip_pos0 = -0.05
    thigh_pose0 = -0.01
    calf_pose0 = -0.01

NOTE: 发散
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag9 --resume  --load_run Jan04_02-54-16_mr_lag3 --checkpoint 10000
```

- 112
```txt
like 1231, but:
    motor_strength_range = [0.9, 1.1]
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]
    hip_pos0 = -0.05
    thigh_pose0 = -0.01
    calf_pose0 = -0.01
    com_displacement_range = [-0.1, 0.1]
    friction_range = [0.2, 1.25]

NOTE：
1. 只能上升到 5.7
2. 9700 后发散
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag10
```

- 113
```txt
like 1231, but:
    motor_strength_range = [0.9, 1.1]
    kp_range = [0.9, 1.1]
    kd_range = [0.9, 1.1]
    hip_pos0 = -0.05
    thigh_pose0 = -0.01
    calf_pose0 = -0.01
    com_displacement_range = [-0.1, 0.1]
    friction_range = [0.2, 1.25]
    lag_timesteps = 4
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 1 --num_envs 4096 --run_name mr_lag11
```
