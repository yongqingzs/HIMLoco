## log
## note
```bash
# cuda:1
CUDA_VISIBLE_DEVICES=1 python3 train.py

# watch gpu
gpustat -i 1
```

### base
- 1117
```bash
python3 train.py --headless --task go1 --max_iterations 2000 --resume --sim_device cuda:0 --load_run Nov14_10-07-07_ --seed 66 --num_envs 8192

python3 play.py --headless --task go1 --sim_device cuda:0 --load_run Nov17_10-32-33_ --checkpoint 12500
```

### no_foot_clearance
set 'foot_clearance' to 0 in go1_config.py   
- 1117
```bash
python3 train.py --headless --task go1 --max_iterations 5000 --resume --sim_device cuda:0 --run_name no_foot_clearance --load_run Nov17_08-39-59_no_foot_clearance --seed 66 --num_envs 8192

python3 play.py --headless --task go1 --sim_device cuda:0 --load_run Nov17_08-39-59_no_foot_clearance --checkpoint 1000

python3 play.py --headless --task go1 --sim_device cuda:0 --load_run Nov18_02-11-25_no_foot_clearance --checkpoint 2000
```