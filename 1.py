import numpy as np
import sys, os
import PIL.Image
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from diffusers.pipelines.stable_diffusion import StableDiffusionSAGPipeline
from diffusers.schedulers import KarrasDiffusionSchedulers

import PIL.Image
import numpy as np

import torch
from diffusers import UNet2DConditionModel, AutoencoderKL, LMSDiscreteScheduler
from PIL import Image
from torchvision.transforms.functional import to_tensor, to_pil_image

# GPU 사용 설정 (CUDA 사용 가능한지 확인)
device = 'cuda:1' if torch.cuda.is_available() else 'cpu'

# 이미지 로드 및 전처리
image_path = "test.png"  # 이미지 경로 설정
original_image = Image.open(image_path).convert("RGB")
original_image = to_tensor(original_image).unsqueeze(0).to(device)  # (C, H, W) -> (1, C, H, W), GPU로 이동

# 모델 및 스케줄러 초기화
model_id = "runwayml/stable-diffusion-v1-5"
scheduler = KarrasDiffusionSchedulers.DDIMScheduler

# 모델 및 오토인코더 로드, GPU로 이동
vae = AutoencoderKL

# 원본 이미지를 잠재 공간으로 인코딩
with torch.no_grad():
    latents = vae.encode(original_image).latent_dist.sample()

# Timestep 시퀀스 생성
timesteps = torch.arange(1, 401, 20, dtype=torch.long).to(device)

# 각 timestep에서 노이즈 추가
for timestep in timesteps:
    noise = torch.randn_like(latents)  # latents와 같은 모양의 랜덤 노이즈 생성
    noisy_latents = scheduler.add_noise(latents, noise, torch.tensor([timestep]).to(device))

    # 결과 이미지 디코딩 (옵션, 시각화를 위해)
    with torch.no_grad():
        noisy_image = vae.decode(noisy_latents)

    # 결과 이미지를 PIL 이미지로 변환 및 저장
    noisy_image_pil = to_pil_image(noisy_image.squeeze(0).cpu())  # GPU에서 CPU로 이동
    noisy_image_pil.save(f"noisy_image_at_timestep_{timestep.item()}.jpg")  # 결과 이미지 저장



# # load model and scheduler
# pipe = StableDiffusionSAGPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16,
#     safety_checker=None
# )
# pipe = pipe.to("cuda:1")

# image = pipe('', guidance_scale=0, sag_scale=0, drop_rate=1.0, drop_types=['cross-attn'], guidance_applied_layers=['down']).images[0]
    

# image.save('test_0.png')