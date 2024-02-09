import argparse
import io
from PIL import Image
import datetime

import torch
import cv2
from re import DEBUG, sub
from flask import Flask, render_template, request, send_from_directory, redirect, send_file, url_for, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import re
import requests
import shutil
import time

app = Flask("__main__")
CORS(app)

# function for accessing rtsp stream
# @app.route("/rtsp_feed")
# def rtsp_feed():
    # cap = cv2.VideoCapture('rtsp://admin:hello123@192.168.29.126:554/cam/realmonitor?channel=1&subtype=0')
    # return render_template('index.html')


# Function to start webcam and detect objects

# @app.route("/webcam_feed")
# def webcam_feed():
    # #source = 0
    # cap = cv2.VideoCapture(0)
    # return render_template('index.html')

# function to get the frames from video (output video)

def get_frame():
    folder_path = '../code/src/runs/detect'
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

def get_files_names(directorio):
    nombres_de_archivos = []
    for root, dirs, files in os.walk(directorio):
        nombres_de_archivos.extend([f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))])
    return nombres_de_archivos

@app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST":
        print("Entering POST -> upload_image")
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(os.environ.get("FLASK_APP", __file__))
            filepath = os.path.join(".." + basepath, 'uploads', f.filename)
            f.save(filepath)
            
            predict_img.imgpath = f.filename
            print("Printing predict_img: ", predict_img)

            conf = "0.75"
            imgsize = "640"

            file_extension = f.filename.rsplit('.', 1)[1].lower()    
            if file_extension == 'jpg':
                process = Popen(["python", basepath + "/detect.py", '--source', filepath, '--conf', conf, '--img-size', imgsize, "--project", basepath + "/runs/detect"  ,"--weights", "best.pt"])
                process.wait()
            elif file_extension == 'mp4':
                process = Popen(["python", basepath + "/detect.py", '--source', filepath, '--conf', conf, '--img-size', imgsize, "--project", basepath + "/runs/detect" , "--weights", "best.pt"])
                process.communicate()
                process.wait()
    
    if hasattr(predict_img, 'imgpath'):
        return "Archivo procesado"
    else:
        return "No se ha cargado ningún archivo aún."

# function to display the detected objects video on html page
@app.route("/video_feed")
def video_feed():
    return Response(get_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#The display function is used to serve the image or video from the folder_path directory.
@app.route('/<path:filename>')
def display(filename):
    folder_path = '../code/src/runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    for subfolder in subfolders:
        directory = os.path.join(folder_path, subfolder)
        print("Buscando en el directorio:", directory)
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            return send_from_directory(directory, filename, request.environ)
    
    return "Archivo no encontrado"

@app.route('/getimagenames')
def get_images_names():
    basepath = os.path.dirname(os.environ.get("FLASK_APP", __file__))
    dirpath = os.path.join(".." + basepath, 'runs', 'detect')
    return get_files_names(dirpath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8080, type=int, help="port number")
    args = parser.parse_args()
    model = torch.hub.load('../code/src', 'custom','best.pt', source='local')
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat

