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
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name random_motor_strength
```

- 1210
```txt
resume 1209
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --resume --load_run Dec09_06-58-12_random_motor_strength --seed 1 --num_envs 8192

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec10_03-27-11_ --checkpoint 10000
```

- 1210-1
```txt
change from 1209
```

1209
```python
pos = [0.0, 0.0, 0.42]
base_height_target = 0.30

class domain_rand:
    randomize_payload_mass = True
    payload_mass_range = [-1, 2]

    randomize_com_displacement = True
    com_displacement_range = [-0.05, 0.05]

    randomize_link_mass = False
    link_mass_range = [0.9, 1.1]
    
    randomize_friction = True
    friction_range = [0.2, 1.25]
    
    randomize_restitution = False
    restitution_range = [0., 1.0]
    
    randomize_motor_strength = True
    motor_strength_range = [0.9, 1.1]
    
    randomize_kp = True
    kp_range = [0.9, 1.1]
    
    randomize_kd = True
    kd_range = [0.9, 1.1]
    
    randomize_initial_joint_pos = True
    initial_joint_pos_range = [0.5, 1.5]
    
    disturbance = True
    disturbance_range = [-30.0, 30.0]
    disturbance_interval = 8
    
    push_robots = True
    push_interval_s = 16
    max_push_vel_xy = 1.

    delay = True

```

1210-1
```python
pos = [0.0, 0.0, 0.33]
base_height_target = 0.33

class domain_rand:
    randomize_payload_mass = True
    payload_mass_range = [-1, 3]

    randomize_com_displacement = True
    com_displacement_range = [-0.1, 0.1]

    randomize_link_mass = True
    link_mass_range = [0.8, 1.2]
    
    randomize_friction = True
    friction_range = [0.2, 2.75]
    
    randomize_restitution = True
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

    delay = True
```

```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192 --run_name domain_rand_v1

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/play.py --headless --task go1 --load_run Dec10_10-25-50_domain_rand_v1 --checkpoint 4800
```