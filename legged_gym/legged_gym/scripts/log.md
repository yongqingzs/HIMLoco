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
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192
```

```txt
对比1208, 仅改变 kp=40, kd=1
```
```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 8192
```


### no_foot_clearance
set 'foot_clearance' to 0 in go1_config.py   
- 1117
```bash
python3 train.py --headless --task go1 --max_iterations 5000 --resume --sim_device cuda:0 --run_name no_foot_clearance --load_run Nov17_08-39-59_no_foot_clearance --seed 66 --num_envs 8192

python3 play.py --headless --task go1 --sim_device cuda:0 --load_run Nov17_08-39-59_no_foot_clearance --checkpoint 1000

python3 play.py --headless --task go1 --sim_device cuda:0 --load_run Nov18_02-11-25_no_foot_clearance --checkpoint 2000
```