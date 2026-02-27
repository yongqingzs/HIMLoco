
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
```

- 0227-1
```txt
A40
like mr_lag13, but:
    thigh_pose0 = -0.02
    calf_pose0 = -0.02

mr_lag20

3500后发散，走路姿势奇怪
```