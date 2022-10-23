from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from img_classification import fruit_classification
from PIL import Image
import cv2
# from skimage import io
# from skimage.metrics import structural_similarity as compare_ssim
import tempfile
import numpy as np
from collections import deque
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.title("Fruit Classification")

def classify_and_label(image):
    label, score = fruit_classification(image, 'keras_model.h5')
    if label == 0:
        st.write("Đây là quả Táo")
    elif label == 1:
        st.write("Đây là quả Bơ")
    elif label == 2:
        st.write("Đây là quả Chuối")
    elif label == 3:
        st.write("Đây là quả Nho")
    elif label == 4:
        st.write("Đây là quả Ổi")
    elif label == 5:
        st.write("Đây là quả Chanh")
    elif label == 6:
        st.write("Đây là quả Kiwi")
    elif label == 7:
        st.write("Đây là quả Cam")
    elif label == 8:
        st.write("Đây là quả Đào")
    elif label == 9:
        st.write("Đây là quả Thơm")
    elif label == 10:
        st.write("Đây là quả Dâu tây")
    elif label == 11:
        st.write("Đây là quả Cà chua")
    elif label == 12:
        st.write("Đây là quả Dưa hấu")
    elif label == 13:
        st.write("Đây là quả Chanh dây")
    elif label == 14:
        st.write("Đây là quả Lựu")
    
    else:
        st.write("Không rõ")
    st.write("Với tỷ lệ: ",score)

uploaded_file = st.file_uploader("Tải lên hình ảnh", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đã upload', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    classify_and_label(image)


upload_file2=st.file_uploader("Choose a video file", type="mp4")


if upload_file2 is not None:
    st.video(upload_file2)

    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(upload_file2.read())

    vf = cv2.VideoCapture(tfile.name)
    frames_queue = deque(maxlen = 20)
    stframe = st.empty()
    sec = 0
    count=0
    while vf.isOpened():
        vf.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
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


            classify_and_label(Image.fromarray(resized_frame))
            #here iwant to upload te images