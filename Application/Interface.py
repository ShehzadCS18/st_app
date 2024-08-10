import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("Image Segmentation App")

st.header("Greet Me")
name = st.text_input("Enter your name:")
if st.button("Greet"):
    response = requests.post("http://127.0.0.1:8000/api/greet/", json={"name": name})
    if response.status_code == 200:
        st.write(response.json().get("message"))
    else:
        st.write("Error:", response.json().get("error"))
st.header("Image Segmentation")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    if st.button("Process"):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = buffered.getvalue()
        response = requests.post("http://127.0.0.1:8000/api/segment/", files={"image": img_str})

        if response.status_code == 200:
            segmented_image_data = response.json().get("segmented_image")
            area = response.json().get("area")
            segmented_image = Image.open(BytesIO(segmented_image_data.encode('latin-1')))
            st.image(segmented_image, caption='Segmented Image.', use_column_width=True)
            st.write(f"Segmented Area: {area} pixels")
        else:
            st.write("Error:", response.status_code)
