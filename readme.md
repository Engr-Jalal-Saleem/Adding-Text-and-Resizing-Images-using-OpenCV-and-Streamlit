# Image Resizer & Text Adder

This application allows users to resize an image and add custom text to it using Streamlit for the frontend and OpenCV for image processing.

## Features

- Upload an image (JPEG, PNG)
- Resize the uploaded image
- Add customizable text to the original or resized image

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Streamlit
- OpenCV
- NumPy
- Pillow

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/image-resizer-text-adder.git
   cd image-resizer-text-adder
   ```
2. Install the required packages:

   ```bash
   pip install streamlit opencv-python-headless numpy pillow
   ```

### Running the Application

Run the following command in the terminal:

```bash
streamlit run app.py
```

### Code Explanation

```python
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
```

### Explanation

1. **Importing Required Libraries**

   ```python
   import cv2 as cv
   import streamlit as st
   import numpy as np
   from PIL import Image
   ```

   - `cv2`: OpenCV library for image processing.
   - `streamlit`: Streamlit library for creating interactive web apps.
   - `numpy`: Library for handling arrays and numerical operations.
   - `PIL.Image`: Module for opening and manipulating images.
2. **Defining the App Function**

   ```python
   def app():
       st.title('Image Resizer & Text Adder')
       st.write('This app is used to resize the image and add text to it.')
   ```

   - Defines the main function `app` for the application.
   - `st.title()` and `st.write()` display the title and description of the app.
3. **Uploading an Image**

   ```python
       img_file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'], key=1)
   ```

   - `st.file_uploader()`: Widget for uploading image files.
4. **Checking and Processing the Uploaded Image**

   ```python
       if img_file is not None:
           file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
           img = cv.imdecode(file_bytes, 1)
           st.image(cv.cvtColor(img, cv.COLOR_BGR2RGB), channels='RGB', caption='Uploaded Image')
   ```

   - Checks if an image is uploaded.
   - Converts the uploaded image to an OpenCV format.
   - Displays the uploaded image.
5. **Input Fields for Resizing**

   ```python
           height = st.number_input('Enter Height', value=img.shape[0])
           width = st.number_input('Enter Width', value=img.shape[1])
   ```

   - Creates input fields for entering the new dimensions of the image.
6. **Resizing the Image**

   ```python
           if 'resized_image' not in st.session_state:
               st.session_state.resized_image = None

           if st.button('Resize Image'):
               if height > 0 and width > 0:
                   st.session_state.resized_image = cv.resize(img, (width, height))
                   st.image(cv.cvtColor(st.session_state.resized_image, cv.COLOR_BGR2RGB), channels='RGB', caption='Resized Image')
   ```

   - Stores the resized image in `st.session_state` to retain it across runs.
   - Resizes the image and displays it.
7. **Input Fields for Adding Text**

   ```python
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
   ```

   - Provides various input fields for customizing the text (content, font type, size, color, thickness, and position).
8. **Adding Text to the Image**

   ```python
           if st.button('Add Text'):
               if text:
                   if target_image == 'Original':
                       image_to_edit = img.copy()
                   elif target_image == 'Resized' and st.session_state.resized_image is not None:
                       image_to_edit = st.session_state.resized_image.copy()
                   else:
                       st.error("Please resize the image first.")
                       return

                   tex_img = cv.putText(image_to_edit, text, (x_pos, y_pos), font_options[font_type], font_size, color, font_thickness, cv.LINE_AA)
                   st.image(cv.cvtColor(tex_img, cv.COLOR_BGR2RGB), channels='RGB', caption='Image with Text')
               else:
                   st.error("Please enter some text.")
   ```

   - Adds the customized text to the selected image (

original or resized) and displays it.

9. **Running the App**

   ```python
   app()
   ```

   - Calls the `app` function to run the application.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Connect with me

- **Portfolio:** [Engr. Jalal Saleem Portfolio](https://engrjalalsaleem.me)
- **LinkedIn:** [Engr. Jalal Saleem](https://www.linkedin.com/in/engr-jalal-saleem)
- **Instagram:** [@jalalbinsaleem](https://www.instagram.com/jalalbinsaleem/)
- **Facebook:** [Jalal Saleem](https://www.facebook.com/jalalsaleem786)
- **GitHub:** [Engr-Jalal-Saleem](https://github.com/Engr-Jalal-Saleem)
- **NPM:** [engr_jalal_saleem](https://www.npmjs.com/~engr_jalal_saleem)
- **Twitter:** [@JSaleem786](https://twitter.com/JSaleem786)
