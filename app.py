from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

load_dotenv()

key=os.getenv("GOOGLE_API_KEY")

# configure
genai.configure(api_key=key)

def get_gemini_response(prompt_text,user_question,image_parts):
    model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
    response= model.generate_content([prompt_text, user_question, image_parts[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        byte_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": byte_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")
    
# Initialize Streamlit App

st.set_page_config(page_title="Invoice Extractor")

input = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image..",type=['.jpg','.png','.jpeg'])
image=""

if uploaded_file is not None:
   image = Image.open(uploaded_file)
   st.image(image,caption="Uploaded Image.",use_column_width=True)

submit=st.button("Tell me about the invoices")

# if submit button is clicked
input_prompt= """
You are an expert in understanding invoices.
recieve the input image as invoice and you 
need to answer the questions based on the 
input image.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response= get_gemini_response(input_prompt,input,image_data)
    
    st.subheader("The Response is")
    st.write(response)