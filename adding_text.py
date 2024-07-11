import cv2 as cv
import streamlit as st
import numpy as np
from PIL import Image

def app():
    st.title('Image Resizer & Text Adder')
    st.write('This app is used to resize the image and add text to it.')

    img_file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'], key=1)

    if img_file is not None:
        # Convert the uploaded file to an OpenCV image
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv.imdecode(file_bytes, 1)

        # Show the uploaded image
        st.image(cv.cvtColor(img, cv.COLOR_BGR2RGB), channels='RGB', caption='Uploaded Image')

        height = st.number_input('Enter Height', value=img.shape[0])
        width = st.number_input('Enter Width', value=img.shape[1])

        if 'resized_image' not in st.session_state:
            st.session_state.resized_image = None

        if st.button('Resize Image'):
            if height > 0 and width > 0:
                # Resize the image
                st.session_state.resized_image = cv.resize(img, (width, height))
                st.image(cv.cvtColor(st.session_state.resized_image, cv.COLOR_BGR2RGB), channels='RGB', caption='Resized Image')

        text = st.text_input('Enter Text to Add', '')

        font_options = {
            'FONT_HERSHEY_SIMPLEX': cv.FONT_HERSHEY_SIMPLEX,
            'FONT_HERSHEY_PLAIN': cv.FONT_HERSHEY_PLAIN,
            'FONT_HERSHEY_DUPLEX': cv.FONT_HERSHEY_DUPLEX,
            'FONT_HERSHEY_COMPLEX': cv.FONT_HERSHEY_COMPLEX,
            'FONT_HERSHEY_TRIPLEX': cv.FONT_HERSHEY_TRIPLEX,
            'FONT_HERSHEY_COMPLEX_SMALL': cv.FONT_HERSHEY_COMPLEX_SMALL,
            'FONT_HERSHEY_SCRIPT_SIMPLEX': cv.FONT_HERSHEY_SCRIPT_SIMPLEX,
            'FONT_HERSHEY_SCRIPT_COMPLEX': cv.FONT_HERSHEY_SCRIPT_COMPLEX,
        }

        font_type = st.selectbox('Select Font Type', list(font_options.keys()))
        font_size = st.number_input('Enter Font Size', value=1.3)
        font_color = st.color_picker('Pick Font Color', '#000000')
        color = tuple(int(font_color[i:i+2], 16) for i in (1, 3, 5))
        font_thickness = st.number_input('Enter Font Thickness', value=2)
        x_pos = st.number_input('Enter X Position', value=50)
        y_pos = st.number_input('Enter Y Position', value=50)
        target_image = st.selectbox('Choose Image for Text', ['Original', 'Resized'])

        if st.button('Add Text'):
            if text:
                if target_image == 'Original':
                    image_to_edit = img.copy()
                elif target_image == 'Resized' and st.session_state.resized_image is not None:
                    image_to_edit = st.session_state.resized_image.copy()
                else:
                    st.error("Please resize the image first.")
                    return

                # Add text to the selected image
                tex_img = cv.putText(image_to_edit, text, (x_pos, y_pos), font_options[font_type], font_size, color, font_thickness, cv.LINE_AA)
                st.image(cv.cvtColor(tex_img, cv.COLOR_BGR2RGB), channels='RGB', caption='Image with Text')
            else:
                st.error("Please enter some text.")

app()
