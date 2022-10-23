from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from img_classification import fruit_classification
from PIL import Image, ImageFont, ImageDraw
import cv2
# from skimage import io
# from skimage.metrics import structural_similarity as compare_ssim
import tempfile
import numpy as np
from collections import deque
import subprocess
from ffmpy import FFmpeg
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.title("Fruit Classification")

CLASS_LIST = ['Táo','Bơ','Chuối','Nho','Ổi','Chanh','Kiwi','Cam','Đào','Thơm','Dâu tây','Cà chua','Dưa hấu','Chanh dây','Lựu']
def classify_and_label(image):
    label, score = fruit_classification(image, 'keras_model.h5')
    st.write('Đây là quả',CLASS_LIST[label], ", độ chính xác là ", score)
    return label, score


def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

uploaded_file = st.file_uploader("Tải lên hình ảnh", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đã upload', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    classify_and_label(image)


upload_file2=st.file_uploader("Choose a video file", type="mp4")
fontpath = "./Baloo-Regular.ttf" 
font = ImageFont.truetype(fontpath, 42)


if upload_file2 is not None:
    st.video(upload_file2)
    
    temp_file_to_save = './temp_file_1.mp4'
    temp_file_result  = './temp_file_2.mp4'
    # tfile = tempfile.NamedTemporaryFile(delete=False) 
    # tfile.write(upload_file2.read())
    write_bytesio_to_file(temp_file_to_save, upload_file2)

    # vf = cv2.VideoCapture(tfile.name)
    vf = cv2.VideoCapture(temp_file_to_save)

    # Get the width and height of the video.
    original_video_width = int(vf.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(vf.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = vf.get(cv2.CAP_PROP_FPS)

    # # Initialize the VideoWriter Object to store the output video in the disk.
    # video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),vf.get(cv2.CAP_PROP_FPS), (original_video_width, original_video_height))
    
    # specify a writer to write a processed video to a disk frame by frame
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
    out_mp4 = cv2.VideoWriter(temp_file_result, fourcc_mp4, frame_fps, (original_video_width, original_video_height),isColor = True)
    frames_queue = deque(maxlen = 20)
    stframe = st.empty()
    sec = 0
    count=0
    imageLocation = st.empty()
    while vf.isOpened():
        vf.set(cv2.CAP_PROP_POS_MSEC, sec*200)
        ret, frame = vf.read()
        
        sec = sec + ret
        sec = round(sec, 2)
        # if frame is read correctly ret is True
        if not ret:
            st.write("Can't receive frame (stream end?). Exiting ...")
            break
        else:
            
            
            
            resized_frame = cv2.resize(frame, (224, 224))
            
            resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            frames_queue.append(resized_frame)
            

            label, score = classify_and_label(Image.fromarray(resized_frame))



            # Write predicted class name on top of the frame.
            # cv2.putText(frame, CLASS_LIST[label], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Write The frame into the disk using the VideoWriter Object.
            # out_mp4.write(frame)

            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            text = CLASS_LIST[label] + ", score: "+ str(score) 
            draw.text((30, 30),text , font = font, fill = (0,255,0,0))
            img_pil = np.array(img_pil) 
            img_pil = cv2.cvtColor(img_pil, cv2.COLOR_BGR2RGB)
            # img_pil = Image.toarray(img_pil)
            imageLocation.image(img_pil, caption='Ảnh đã upload', use_column_width=True)

    # out_mp4.release()
    vf.release()
    
    # convertedVideo = "./testh264.mp4"
    # subprocess.call(args=f"ffmpeg -y -i {temp_file_result} -c:v libx264 {convertedVideo}".split(" "))

    # st.video(convertedVideo)
