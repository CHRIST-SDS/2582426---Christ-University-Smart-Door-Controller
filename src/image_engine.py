import torch
from diffusers import AutoPipelineForText2Image

_pipe = None

def get_image_pipeline():
    global _pipe
    if _pipe is None:
        # Check GPU availability (CUDA for NVIDIA, MPS for Mac Apple Silicon, CPU as fallback)
        device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        dtype = torch.float16 if device in ["cuda", "mps"] else torch.float32
        
        # SDXL-Turbo is optimized to render high-quality images in just 1-2 steps
        _pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", 
            torch_dtype=dtype
        )
        _pipe.to(device)
    return _pipe

def generate_status_badge(status_text: str, output_path: str = "outputs/badge.png") -> str:
    """
    Generates a visual digital pass/badge based on the gate decision status.
    """
    pipe = get_image_pipeline()
    prompt = f"Futuristic digital security UI access badge, campus gate pass, text state: {status_text}, 3d render, high tech interface, highly detailed"
    
    # 2 inference steps for fast local generation
    image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
    image.save(output_path)
    return output_path