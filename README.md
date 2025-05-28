# 🎨 Custom Avatar Generator

Welcome to **Custom Avatar Generator** — your AI-powered solution for creating stunning, ultra-detailed custom avatars effortlessly!

---

## 🚀 Project Overview

This project leverages the power of **Stable Diffusion XL**, **LoRA fine-tuning**, and **ComfyUI** to generate personalized avatar images based on user input. Upload your images, select your preferred style, and watch the AI work its magic!

### Key Features

- 🔥 **High-quality avatars**: Generate 4k, ultra-detailed portraits.
- 🎭 **Customizable styles**: Choose from various artistic styles like anime, realistic, cartoon, and more.
- ⚡ **Fast and scalable**: Powered by ComfyUI’s headless API for seamless backend generation.
- 🔄 **Extensible workflow**: Easy to modify and expand the generation pipeline.
- 🛠️ **Open source**: Fully customizable and ready for your own creative twist.

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+
- CUDA-enabled GPU (recommended for performance)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) installed
- Pretrained models (Stable Diffusion XL, VAE, LoRA checkpoints)

### Installation

1. Clone this repo:
    ```bash
    git clone https://github.com/MOhItNegi1/custom-avatar-generator.git
    cd custom-avatar-generator
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    .\venv\Scripts\activate   # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Place your models in the following folders:
    ```
    models/Stable-diffusion/
    models/VAE/
    loras/
    ```

---

## 🚀 Usage

1. Start the ComfyUI server (ensure it is running on port 8188):
    ```bash
    python main.py
    ```

2. Open the web interface:
    ```
    http://127.0.0.1:8000/
    ```

3. Upload your images and choose a style.

4. Trigger avatar generation.

5. View or download your generated avatar from the results page.

---

## 📁 Project Structure

