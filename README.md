# 디풋젼으로 사진 잘 찍는다고 소문나자

**2024년 겨울 [AIKU](https://github.com/AIKU-Official) 활동으로 진행한 프로젝트입니다.**

**2024년 2학기 AIKU Conference 1등 수상 예정!**

## Abstract

사진에 발끝이 나와야 비율이 좋아 보인다는 암묵적 규칙이 있습니다. 하지만 종종 잘 나온 사진에 발끝이 잘려 아쉬울 때가 있죠. 본 프로젝트는 Diffusion을 이용한 Image Inpainting 을 통해 잘린 이미지를 주변 이미지와 어울리게 생성하고자 하는 목표로 시작되었습니다.

Image Inpainting은 이미지의 빠진 부분을 주변과 의미론적으로 유사하게 채우는 Task입니다. 
2022 CVPR RePaint 모델에서는 unconditional DDPM을 이용해 아는 픽셀은 forward process로 구하고, 모르는 픽셀은 reverse process에서 구하는 방법을 제안하였습니다. 
또한 2023 CVPR ControlNet 모델에서는 diffusion model의 가중치를 trainable copy와 locked copy로 복제하여, locked copy에서는 대규모 데이터셋에서 학습한 네트워크 능력을 보존하는 반면 trainable copy는 task별 데이터셋에서 학습되어 human pose와 같은 conditional control을 효과적으로 학습하는 방법을 제안했습니다. 
이를 참고하여 Stable Diffusion으로 잘린 이미지를 생성한 후 각 모델을 Inpainting에 활용하는 2-Track으로 프로젝트를 진행했습니다.

## References

> **Stable Diffusion** [[repo]](https://github.com/CompVis/latent-diffusion)
>
> _Proposed in [“High-Resolution Image Synthesis with Latent Diffusion Models”](https://arxiv.org/abs/2112.10752),
> CVPR 2022

> **RePaint** [[repo]](https://github.com/andreas128/RePaint)
>
> _Proposed in [“RePaint: Inpainting using Denoising Diffusion Probabilistic Models”](https://arxiv.org/abs/2201.09865),
> CVPR 2022

> **ControlNet** [[repo]](https://github.com/lllyasviel/ControlNet)
>
> _Proposed in [“Adding Conditional Control to Text-to-Image Diffusion Models"](https://arxiv.org/abs/2302.05543),
> CVPR 2023

## Method 1: ControlNet with Pose Editing

Stable Diffusion 모델을 활용하여 text condition을 주고, 1차적으로 잘린 이미지를 context에 맞게 생성합니다. 그러나 text prompt만으로는 Stable Diffusion이 복잡한 pose에 대한 semantic를 정확히 이해하기 어렵습니다. 이 문제를 해결하기 위해, Openpose를 사용하여 이미지에서 pose를 추출하고 이를 수정합니다. 이후, contextualize가 충분히 이루어지지 않은 부분에 대한 mask와 함께 ControlNet의 condition으로 제공하여 inpainting 작업을 수행합니다.

### Architecture
<p align="center">
    <img src = "./image/architecture.png"
        style = "width: 70%">
</p>

#### 1. Stable Diffusion (Outpainting)

BLIP encoder 을 통해 text embedding을 생성하고, Stable Diffusion 기반 RealisticVision model의 condition으로 제공합니다. 
RealisticVision은

#### 2. ControlNet (Openpose Editing via Human Interaction)

Stable Diffusion pose limitation -> Openpose editing
ControlNet explanation

## Method 2: Mask based RePaint (Ongoing)

Diffusion의 수학적 증명을 많이 해소한 score쪽의 논문들, 특히 NCSN 논문에서는 이상한(부자연스러운) 샘플들은 Real Image로 나타나질 않으니 모델이 학습할 수 없고, Random Noise로부터 역과정을 진행하는 Diffusion의 특성상 (todo)

### Architecture

<p align="center">
    <img src = "./image/repaint_architecture.png"
        style = "width: 70%">
</p>

#### 1. Stable Diffusion

#### 2. RePaint (DDIM)

## Demo



## Team

- [전민경 (Leader)](https://github.com/mingming2000): RePaint implementation (Stable Diffusion), Outpainting & ControlNet
- [김정우](https://github.com/kmjnwn): RePaint implementation (Stable Diffusion, DDIM)
- [김민재](https://github.com/kwjames98): Paper research, Demo
