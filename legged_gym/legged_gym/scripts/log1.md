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
```
```bash
python3 /workspace/HIMLoco/legged_gym/legged_gym/scripts/train.py --headless --task go1 --max_iterations 5000 --seed 1 --num_envs 4096 --run_name mr_lag
```