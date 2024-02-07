import argparse
import io
from PIL import Image
import datetime

import torch
import cv2
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import re
import requests
import shutil
import time

app = Flask("__main__")


@app.route("/")
def hello_world():
    return render_template('index.html')


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
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    directory = folder_path+'/'+latest_subfolder
    print("printing directory: ",directory)  
    filename = predict_img.imgpath
    file_extension = filename.rsplit('.', 1)[1].lower()
    #print("printing file extension from display function : ",file_extension)
    environ = request.environ
    if file_extension == 'jpg':      
        return send_from_directory(directory,filename,environ)

    elif file_extension == 'mp4':
        return render_template('index.html')

    else:
        return "Invalid file format"

   
""" @app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST":
        print("entering to POTS -> predict_img")
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(os.environ.get("FLASK_APP", __file__))
            print("Basepath: ", basepath)
            filepath = os.path.join(".." + basepath,'uploads',f.filename)
            print("Filepath: ", filepath)
            print("upload folder is ", filepath)
            f.save(filepath)
            
            predict_img.imgpath = f.filename
            print("printing predict_img :::::: ", predict_img)

            file_extension = f.filename.rsplit('.', 1)[1].lower()    
            if file_extension == 'jpg':
                process = Popen(["python", "detect.py", '--source', filepath, "--weights","best.pt"], shell=True)
                process.wait()
                
                
            elif file_extension == 'mp4':
                process = Popen(["python", "detect.py", '--source', filepath, "--weights","best.pt"], shell=True)
                process.communicate()
                process.wait()

            
    folder_path = '../code/src/runs/detect'
    if hasattr(predict_img, 'imgpath'):
        filename = predict_img.imgpath
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
        latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
        image_path = os.path.join(folder_path, latest_subfolder, filename)
        return render_template('index.html', image_path=image_path)
    else:
    # Manejar el caso en que predict_img.imgpath no esté definido
    # Esto puede ocurrir si no se ha enviado una solicitud POST previamente
    # o si ha habido un error en la lógica del código
        return "No se ha cargado ningún archivo aún."
    
    #subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    #latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    #image_path = folder_path+'/'+latest_subfolder+'/'+f.filename 
    #return render_template('index.html', image_path=image_path)
    #return "done"  """

@app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST":
        print("Entering POST -> upload_image")
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(os.environ.get("FLASK_APP", __file__))
            print("Basepath: ", basepath)
            filepath = os.path.join(".." + basepath, 'uploads', f.filename)
            print("Filepath: ", filepath)
            print("Upload folder is ", filepath)
            f.save(filepath)
            
            predict_img.imgpath = f.filename
            print("Printing predict_img: ", predict_img)

            file_extension = f.filename.rsplit('.', 1)[1].lower()    
            if file_extension == 'jpg':
                process = Popen(["python", basepath + "/detect.py", '--source', filepath, "--project", basepath + "/runs/detect"  ,"--weights", "best.pt"])
                process.wait()
                
            elif file_extension == 'mp4':
                process = Popen(["python", basepath + "/detect.py", '--source', filepath, "--project", basepath + "/runs/detect" , "--weights", "best.pt"])
                process.communicate()
                process.wait()
    
    folder_path = '../code/src/runs/detect'
    if hasattr(predict_img, 'imgpath'):
        filename = predict_img.imgpath
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
        latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
        image_path = os.path.join(folder_path, latest_subfolder, filename)
        return render_template('index.html', image_path=image_path)
    else:
    # Manejar el caso en que predict_img.imgpath no esté definido
    # Esto puede ocurrir si no se ha enviado una solicitud POST previamente
    # o si ha habido un error en la lógica del código
        return "No se ha cargado ningún archivo aún."

""" @app.route("/detected_image")
def get_detected_image():
    folder_path = '../code/src/runs/detect'
    if hasattr(get_detected_image, 'imgpath'):
        filename = get_detected_image.imgpath
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
        latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
        image_path = os.path.join(folder_path, latest_subfolder, filename)
        return render_template('index.html', image_path=image_path)
    else:
        return "No se ha cargado ningún archivo aún."
 """

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8080, type=int, help="port number")
    args = parser.parse_args()
    model = torch.hub.load('../code/src', 'custom','best.pt', source='local')
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat

