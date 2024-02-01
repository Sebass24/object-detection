from fastapi import FastAPI, File, Response, HTTPException, templates
from fastapi.responses import HTMLResponse
import os
from subprocess import Popen
import time
import torch
import cv2
from subprocess import Popen

app = FastAPI()

@app.get('/')
def index():
    return 'Hello Word!'

def get_frame():
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    filename = predict_img.imgpath    
    image_path = folder_path+'/'+latest_subfolder+'/'+filename    
    video = cv2.VideoCapture(image_path)  # detected video path
    #video = cv2.VideoCapture("video.mp4")
    while True:
        success, image = video.read()
        if not success:
            break
        ret, jpeg = cv2.imencode('.jpg', image)   
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')   
        time.sleep(0.1)  #control the frame rate to display one frame every 100 milliseconds: 

# function to display the detected objects video on html page
@app.get("/video_feed")
def video_feed():
    return Response(get_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.post("/predict")
async def predict_img(file: bytes = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No se recibió ningún archivo")

    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'uploads', file.filename)
    print("Carpeta de carga es ", filepath)

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    file_extension = file.filename.rsplit('.', 1)[1].lower()

    if file_extension == 'jpg':
        process = Popen(["python", "detect.py", '--source', filepath, "--weights", "best.pt"], shell=True)
        process.wait()
    elif file_extension == 'mp4':
        process = Popen(["python", "detect.py", '--source', filepath, "--weights", "best.pt"], shell=True)
        process.communicate()
        process.wait()

    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    image_path = folder_path + '/' + latest_subfolder + '/' + file.filename
    return templates.TemplateResponse("index.html", {"request": file, "image_path": image_path})
