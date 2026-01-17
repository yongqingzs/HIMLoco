#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

import os
import sys
import argparse
# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
# Import torch first to avoid isaacgym import issues
import torch
import copy
import torch.nn.functional as F

from rsl_rl.modules import HIMActorCritic


class PolicyExporterHIM(torch.nn.Module):
    def __init__(self, actor_critic):
        super().__init__()
        self.actor = copy.deepcopy(actor_critic.actor)
        self.estimator = copy.deepcopy(actor_critic.estimator.encoder)

    def forward(self, obs_history):
        parts = self.estimator(obs_history)[:, 0:19]
        vel, z = parts[..., :3], parts[..., 3:]
        z = F.normalize(z, dim=-1, p=2.0)
        return self.actor(torch.cat((obs_history[:, 0:45], vel, z), dim=1))


def infer_model_dims(checkpoint):
    if 'model_state_dict' in checkpoint:
        model_params = checkpoint['model_state_dict']
    else:
        model_params = checkpoint
    
    actor_layers = sorted([k for k in model_params.keys() if k.startswith('actor.') and '.weight' in k],
                         key=lambda x: int(x.split('.')[1]))
    first_actor_weight = model_params[actor_layers[0]]
    mlp_input_dim_a = first_actor_weight.shape[1]
    num_one_step_obs = mlp_input_dim_a - 3 - 16
    
    last_actor_weight = model_params[actor_layers[-1]]
    num_actions = last_actor_weight.shape[0]
    
    encoder_layers = sorted([k for k in model_params.keys() if k.startswith('estimator.encoder.') and '.weight' in k],
                           key=lambda x: int(x.split('.')[2]))
    first_encoder_weight = model_params[encoder_layers[0]]
    enc_input_dim = first_encoder_weight.shape[1]
    temporal_steps = enc_input_dim // num_one_step_obs
    num_actor_obs = temporal_steps * num_one_step_obs
    
    return num_actor_obs, num_one_step_obs, num_actions


def export_policy(checkpoint_path, output_path):
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    if 'model_state_dict' in checkpoint:
        model_state = checkpoint['model_state_dict']
    else:
        model_state = checkpoint
    
    num_actor_obs, num_one_step_obs, num_actions = infer_model_dims(checkpoint)
    
    # Infer num_critic_obs from critic layer
    critic_weight = model_state['critic.0.weight']
    num_critic_obs = critic_weight.shape[1]
    
    print(f"Model dimensions: obs={num_actor_obs}, critic_obs={num_critic_obs}, one_step_obs={num_one_step_obs}, actions={num_actions}")
    
    actor_critic = HIMActorCritic(num_actor_obs, num_critic_obs, num_one_step_obs, num_actions)
    model_dict = actor_critic.state_dict()
    pretrained_dict = {k: v for k, v in model_state.items() if k in model_dict}
    model_dict.update(pretrained_dict)
    actor_critic.load_state_dict(model_dict)
    actor_critic.eval()
    
    exporter = PolicyExporterHIM(actor_critic)
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    exporter.to('cpu')
    traced_script_module = torch.jit.script(exporter)
    traced_script_module.save(output_path)
    
    file_size = os.path.getsize(output_path) / 1024
    print(f"✓ Policy exported to: {output_path} ({file_size:.2f} KB)")
    
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, required=True, help='Path to checkpoint .pt file')
    parser.add_argument('--output', type=str, default='policy.pt', help='Output path')
    args = parser.parse_args()
    
    export_policy(args.checkpoint, args.output)