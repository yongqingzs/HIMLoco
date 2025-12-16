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