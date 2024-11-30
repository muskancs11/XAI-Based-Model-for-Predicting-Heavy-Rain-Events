import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

def main():
    st.title("Image Processing with Flask and Streamlit")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = uploaded_file.read()
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        if st.button("Process Image"):
            image_base64 = base64.b64encode(image).decode('utf-8')
            response = requests.post("https://e9ef-35-229-251-222.ngrok-free.app/process_image", json={"image": image_base64})

            if response.status_code == 200:
                result = response.json()
                coefficients = result["coefficients"]
                masked_boundaries_image = base64.b64decode(result["masked_boundaries_image"])
                perturbed_images = [base64.b64decode(img) for img in result["perturbed_images"]]
                top_features_image = base64.b64decode(result["top_features_image"])

                st.write("Coefficients: ", coefficients)

                st.write("Masked Boundaries Image:")
                st.image(masked_boundaries_image, caption='Masked Boundaries Image', use_column_width=True)
                st.write("Perturbed Images:")
                #st.image(perturbed_images, caption='Perturbed Images', use_column_width=True)
                for img in perturbed_images:
                    st.image(img, use_column_width=True)
                st.write("Top Features Image:")
                st.image(top_features_image, caption='Top Features Image', use_column_width=True)
            else:
                st.error("Error processing image")

if __name__ == "__main__":
    main()