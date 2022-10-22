from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from img_classification import fruit_classification
from PIL import Image

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.title("Fruit Classification")


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))


uploaded_file = st.file_uploader("Tải lên hình ảnh", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đã upload', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    label, score = fruit_classification(image, 'keras_model.h5')
    if label == 0:
        st.write("Táo")
    elif label == 1:
        st.write("Bơ")
    elif label == 2:
        st.write("Chuối")
    elif label == 3:
        st.write("Nho")
    elif label == 4:
        st.write("Ổi")
    elif label == 5:
        st.write("Bơ")
    elif label == 5:
        st.write("Chanh")
    elif label == 5:
        st.write("Kiwi")
    elif label == 5:
        st.write("Cam")
    elif label == 5:
        st.write("Thơm")
    elif label == 5:
        st.write("Dâu tây")
    elif label == 5:
        st.write("Cà chua")
    elif label == 5:
        st.write("Dưa hấu")
    elif label == 5:
        st.write("Chanh dây")
    elif label == 5:
        st.write("Lựu")
    
    else:
        st.write("Không rõ")
    st.write(score)