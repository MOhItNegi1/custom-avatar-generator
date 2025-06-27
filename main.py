

print("Script started")

from comfyui_api import modify_workflow, run_comfyui
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import os
import uuid
import shutil
import subprocess
import json

app = FastAPI()




@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Upload Images for Avatar</title>
        </head>
        <body>
            <h1>Upload Images</h1>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <label>Select style:</label>
                <input name="style" type="text" value="default" required />
                <br><br>
                <input name="images" type="file" multiple required />
                <br><br>
                <button type="submit">Upload</button>
            </form>
        </body>
    </html>
    """


UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
WORKFLOW_PATH = "workflows/avatar_generation.json"  # Prebuilt ComfyUI workflow

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_images(images: list[UploadFile] = File(...), style: str = Form(...)):
    session_id = str(uuid.uuid4())
    user_dir = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(user_dir, exist_ok=True)
    for img in images:
        with open(os.path.join(user_dir, img.filename), "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
    return {"session_id": session_id, "message": "Images uploaded successfully."}

@app.post("/generate")
async def generate_avatar(session_id: str = Form(...), style: str = Form(...)):
    user_dir = os.path.join(UPLOAD_FOLDER, session_id)
    print(f"Checking permissions for: {user_dir}")
    print(f"Exists: {os.path.exists(user_dir)}")
    print(f"Is Directory: {os.path.isdir(user_dir)}")
    print(f"Can write test file:")

    try:
        test_path = os.path.join(user_dir, "test_perm.txt")
        with open(test_path, "w") as f:
            f.write("permission test")
        os.remove(test_path)
        print("Write test: OK")
    except Exception as e:
        print("Write test failed:", e)
    if not os.path.exists(user_dir):
        return JSONResponse(status_code=404, content={"error": "Session not found."})

    try:
        new_workflow_path = modify_workflow(user_dir, style, session_id)
        run_comfyui(new_workflow_path)
        return {"message": "Generation complete.", "result_path": f"/result/{session_id}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



@app.get("/result/{session_id}")
async def get_result(session_id: str):
    output_path = os.path.join(RESULT_FOLDER, f"{session_id}.png")
    if os.path.exists(output_path):
        return FileResponse(output_path, media_type="image/png")
    return JSONResponse(status_code=404, content={"error": "Result not found."})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8188)
print("Script ended")
