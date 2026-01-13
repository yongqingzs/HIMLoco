- 0109
```txt
原始 go1_trot_config

NOTE：
1. 3 m/s 1000 后震荡
```
```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1_trot --max_iterations 5000 --seed 1 --num_envs 4096 --run_name base

CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1_trot --load_run Jan09_03-22-41_base

# command = 2 很轻松就达到了，于是 resume 提高到 3
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1_trot --max_iterations 5000 --seed 1 --num_envs 4096 --run_name based1 --resume --load_run Jan09_03-22-41_base --checkpoint 600

python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/export_policy.py --headless --task go1_trot --load_run Jan09_05-19-54_based1 --checkpoint 1000
```

- 0109-1
```txt
like 0109, but:
    terrain_proportions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0]

NOTE:
1. 2 m/s 前震荡
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1_trot --max_iterations 5000 --seed 1 --num_envs 4096 --run_name uni
```

- 0109-2
```txt
like 0109, but:
    max_forward_curriculum = 2.5 
```
```bash
CUDA_VISIBLE_DEVICES=1 python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1_trot --max_iterations 5000 --seed 1 --num_envs 4096 --run_name base1
```

- 0113
```txt
use normal ppo:
    max_forward_curriculum = 2.5 
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1_trot --max_iterations 5000 --seed 1 --num_envs 4096 --run_name ppo --policy ppo
```
