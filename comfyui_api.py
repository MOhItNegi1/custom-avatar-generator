# comfyui_api.py
# This script modifies a workflow JSON with user input and runs ComfyUI in headless mode
import requests
import argparse
import json
import os
import subprocess
import torch

WORKFLOW_BASE_PATH = "workflows/avatar_generation.json"




def modify_workflow(input_dir, style, session_id):
    with open(WORKFLOW_BASE_PATH, 'r') as f:
        workflow = json.load(f)

    # Dynamically build LoRA path based on style
    lora_filename = f"{style.lower()}_style_lora.safetensors"
    lora_path = os.path.join("loras", lora_filename)

    # Fallback to default if LoRA file doesn't exist
    if not os.path.exists(lora_path):
        print(f"⚠️ LoRA file not found for style '{style}', falling back to default.")
        lora_path = os.path.join("loras", "default_style_lora.safetensors")

    for node in workflow['workflow']['nodes']:
        if node['type'] == 'ApplyLoRA':
            node['inputs']['lora_path'] = lora_path

        elif node['type'] == 'CLIPTextEncode' and 'positive' in node['id']:
            prompt = node['inputs']['text']
            prompt = prompt.replace("{style}", style).replace("{user_name}", session_id)
            node['inputs']['text'] = prompt

        elif node['type'] == 'SaveImage':
            node['inputs']['output_path'] = f"results/{session_id}.png"

    os.makedirs("temp_workflows", exist_ok=True)
    temp_path = f"temp_workflows/{session_id}_workflow.json"
    with open(temp_path, 'w') as f:
        json.dump(workflow, f, indent=4)

    return temp_path









def run_comfyui(workflow_path):
    with open(workflow_path, 'r') as f:
        full_workflow = json.load(f)

    # Post only the `workflow` key's value (not the full wrapper)
    workflow_json = full_workflow["workflow"]

    print("Sending workflow JSON to ComfyUI API:")
    print(json.dumps(workflow_json, indent=2))  # Debug output

    response = requests.post("http://127.0.0.1:8188/prompt", json=workflow_json)

    if response.status_code != 200:
        print(" ComfyUI API error:", response.text)
        raise RuntimeError("ComfyUI failed to accept the workflow.")

    print(" Workflow submitted successfully.")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--style", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    session_id = os.path.basename(args.output).replace(".png", "")
    new_workflow_path = modify_workflow(args.input, args.style, session_id)
    run_comfyui(new_workflow_path)

if __name__ == "__main__":
    main()
