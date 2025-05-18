from dotenv import load_dotenv
import os   

load_dotenv()

import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#Function to load gemini pro vision 

model = genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt]
    )
    return response.text

def input_image_details(uploaded_file):
    # Check if the uploaded file is a valid image
    if uploaded_file is not None:
        byte_data = uploaded_file.getvalue()
        
        image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": byte_data,
                }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image file uploaded.")

# initialize our streamlit app

st.set_page_config(page_title="Multilingual Image Generation", page_icon=":guardsman:", layout="wide")
st.header("Multilingual Invoice Extraction")
input = st.text_input("Enter your question about the invoice",key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

submit_button = st.button("Tell about invoice")
input_prompt = """
You are invoice excutor extpert You are a multilingual invoice extraction expert. You are given an image of an invoice and a question about the invoice. You need to extract the answer from the image and return it in the same language as the question.
The question is in English and the answer should be in English. The image is an invoice. The question is: {input}. The image is: {image}. The answer is:
"""

# If submit button is pressed
if submit_button :
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)                                              
    st.subheader("Gemini Pro Vision Response")
    st.write(response)                            