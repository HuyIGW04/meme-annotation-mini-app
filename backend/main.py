from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
import json

app = FastAPI()

# storage
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
os.makedirs(f"{BASE_DIR}/submit/images", exist_ok=True)
os.makedirs(f"{BASE_DIR}/submit/jsons", exist_ok=True)
os.makedirs(f"{BASE_DIR}/reject/images", exist_ok=True)
os.makedirs(f"{BASE_DIR}/reject/jsons", exist_ok=True)


# submit API
@app.post("/annotate/submit")
async def submit_annotation(
    image: UploadFile,
    label: str = Form(...),
    target: str = Form(...),
    type_img: str = Form(...),
    topic: str = Form(...)
):
    # save image
    img_path = os.path.join(BASE_DIR, "submit/images", image.filename)
    with open(img_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # save json
    data = {
        "image": image.filename,
        "class": label,
        "target": target,
        "type": type_img,
        "topic": topic,
    }
    name_json = os.path.splitext(image.filename)[0]
    json_path = os.path.join(BASE_DIR, "submit/jsons",
                             f"{name_json}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return JSONResponse(content={"status": "success", "data": data})


# reject API
@app.post("/annotate/reject")
async def reject_annotation(
    image: UploadFile,
    reason: str = Form(...)
):
    # save image
    img_path = os.path.join(BASE_DIR, "reject/images", image.filename)
    with open(img_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # save json
    data = {
        "image": image.filename,
        "action": "Reject",
        "reason": reason,
    }
    name_json = os.path.splitext(image.filename)[0]
    json_path = os.path.join(BASE_DIR, "reject/jsons",
                             f"{name_json}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return JSONResponse(content={"status": "rejected", "data": data})
