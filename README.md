# Meme Annotation App
A mini-project for image annotation, as part of Meme Harmful Classification. This app uses Gradio as the backend and FastAPI as the frontend.
## Quick Start
Requirements: Install all importance libs for this app:
```bash
pip install -r requirements.txt
```
Environment: Open 2 different command prompts and activate the Anaconda environment (in my OS, it's named `base`)
```bash
conda activate base
```
### Run app
we start with backend, which based on FastAPI:
```bash
cd backend
uvicorn main:app
```

Next, we start the frontend and deploy app by Gradio:
```bash
cd frontend
python app.py
```  
### Data Storage 

All annotated data is stored under the `storage/` directory (created automatically next to `main.py`):

```text
storage/
│── submit/
│   ├── images/   # approved images
│   └── jsons/    # JSON metadata for approved images
│
└── reject/
    ├── images/   # rejected images
    └── jsons/    # JSON metadata for rejected images
