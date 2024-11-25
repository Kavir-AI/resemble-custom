import gradio as gr
import torch
import torchaudio

print("Loading Resemble Enhance")
from resemble_enhance.enhancer.inference import denoise, enhance

print("Checking CUDA availability")
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


def _fn(path, solver, nfe, tau, denoising):
    if path is None:
        return None, None

    solver = solver.lower()
    nfe = int(nfe)
    lambd = 0.9 if denoising else 0.1

    dwav, sr = torchaudio.load(path)
    dwav = dwav.mean(dim=0)

    wav1, new_sr = denoise(dwav, sr, device)
    wav2, new_sr = enhance(dwav, sr, device, nfe=nfe, solver=solver, lambd=lambd, tau=tau)

    wav1 = wav1.cpu().numpy()
    wav2 = wav2.cpu().numpy()

    return (new_sr, wav1), (new_sr, wav2)


def main():
    print("Starting main function")
    inputs: list = [
        gr.Audio(type="filepath", label="Input Audio"),
        gr.Dropdown(choices=["Midpoint", "RK4", "Euler"], value="Midpoint", label="CFM ODE Solver"),
        gr.Slider(minimum=1, maximum=128, value=64, step=1, label="CFM Number of Function Evaluations"),
        gr.Slider(minimum=0, maximum=1, value=0.5, step=0.01, label="CFM Prior Temperature"),
        gr.Checkbox(value=False, label="Denoise Before Enhancement"),
    ]
    print("Inputs created")

    outputs: list = [
        gr.Audio(label="Output Denoised Audio"),
        gr.Audio(label="Output Enhanced Audio"),
    ]

    print("Creating Gradio Interface")
    interface = gr.Interface(
        fn=_fn,
        title="Resemble Enhance",
        description="AI-driven audio enhancement for your audio files, powered by Resemble AI.",
        inputs=inputs,
        outputs=outputs,
    )
    print("Launching Gradio Interface")
    interface.launch()
    print("Gradio Interface Launched")


if __name__ == "__main__":
    main()
