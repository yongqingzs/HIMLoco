
## base
```bash
# train
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 20000 --seed 2 --num_envs 4096 --run_name XX

# continue training
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 10000 --seed 2 --num_envs 4096 --run_name XX1 --resume  --load_run XX --checkpoint 10000

# export
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_alone.py --checkpoint XX
```

NOTE：
1. 在 5090DV2 上训练时，seed=1 会出问题(发散)，建议使用 seed=2


- 0227
```python
# like mr_lag13, but:
use_terrain_max_command_ranges = True
terrain_max_command_ranges = [
    {'lin_vel_x': [-1.5, 1.5], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 0: smooth slope
    {'lin_vel_x': [-1.5, 1.5], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 1: rough slope
    {'lin_vel_x': [-1.0, 1.0], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 2: stairs up
    {'lin_vel_x': [-1.0, 1.0], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 3: stairs down
    {'lin_vel_x': [-1.0, 1.0], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 4: discrete obstacles
]

thigh_pose0 = -0.02
calf_pose0 = -0.02
# mr_lag19
'''
速度跟踪更优(数据上)，但走路姿势奇怪，6000后发散(可能来自 -0.02)
'''


# like mr_lag19, but:
max_forward_curriculum = 2.0
{'lin_vel_x': [-2.0, 2.0], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 0: smooth slope
# mr_lag21
'''
训练停止
'''


# like mr_lag19, but:
thigh_pose0 = -0.01
calf_pose0 = -0.01
# mr_lag22
'''
10000 以后训练崩溃

在 a40 上训练 mr_lag22_a40，发现 2000 时走路姿势奇怪，和 5090 表现类似
'''

# like mr_lag19, but:
max_forward_curriculum = 2.0
{'lin_vel_x': [-2.0, 2.0], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 0: smooth slope
thigh_pose0 = -0.01
calf_pose0 = -0.01
# mr_lag23
'''
7000 时测试，vel >= 1.5 时，表现不佳
12700 没有发散
'''


# like mr_lag19, but:
foot_clearance = -0.01
feet_air_time = 0
thigh_pose0 = -0.01
calf_pose0 = -0.01
# mr_lag24
'''
走路姿势奇怪，6000 后发散
'''


# like mr_lag19, but:
use_terrain_max_command_ranges = False
if self.command_ranges["lin_vel_x"][1] < 1.0:
    self.commands[env_ids, 0] = torch_rand_float(self.command_ranges["lin_vel_x"][0], self.command_ranges["lin_vel_x"][1], (len(env_ids), 1), device=self.device).squeeze(1)
else:
    self.commands[env_ids, 0] = torch_rand_float(-1.0, 1.0, (len(env_ids), 1), device=self.device).squeeze(1)
thigh_pose0 = -0.01
calf_pose0 = -0.01
# mr_lag25
'''
2000 表现类似 mr_lag13，17000 后发散
'''

# like mr_lag19, but:
thigh_pose0 = -0.01
calf_pose0 = -0.01
max_forward_curriculum = 2.0
{'lin_vel_x': [-2.0, 2.0], 'lin_vel_y': [-1.0, 1.0], 'ang_vel_yaw': [-1.0, 1.0], 'heading': [-3.14, 3.14]},  # 0: smooth slope
self._update_env_command_ranges()  # fix
# mr_lag26
'''
2000 发散
'''

# like mr_lag26, but:
max_forward_curriculum = 1.5
# mr_lag27
```

- 0227-1
```txt
A40
like mr_lag13, but:
    thigh_pose0 = -0.02
    calf_pose0 = -0.02

mr_lag20

3500 后发散，走路姿势奇怪
```