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
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name p_limit --resume  --load_run Dec11_03-39-53_ --checkpoint 5000

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec18_10-11-21_p_limit --checkpoint 5300
```