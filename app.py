# import streamlit as st
# from google import genai
# from google.genai import types
# import os
# from dotenv import load_dotenv
# from PIL import Image

# #backend
# load_dotenv()
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input,image, prompt):#function to generate response
#     model=genai.GenerativeModel('gemini-pro-vision')#generative ai model, generate content based on the input
#     response=model.generate_content([input,image[0],prompt])#genrate content using model
#     return response.text #return the response in text format
           
# def input_image_setup(uploaded_file):#function to process image
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()#Converts the uploaded file into a byte format (binary data). This is necessary for passing the image to the generative model

#         image_parts=[
#             {
#                 "mime_type":uploaded_file.type,
#                 "data":bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No File uploaded")


# #frontend
# #streamlit app

# st.set_page_config(page_title="CalorieScan")

# st.header("CalorieScan")
# input=st.text_input("Input Prompt: ", key="input")
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
# image=""
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)

# submit = st.button("Tell me the total calories")

# input_prompt="""
# You are an expert in nutritionist where you need to see the food items from the image
#                and calculate the total calories, also provide the details of every food items with calories intake
#                is below format

#                1. Item 1 - no of calories
#                2. Item 2 - no of calories
#                ----
#                ----


# """

# ## If submit button is clicked

# if submit:
#     image_data=input_image_setup(uploaded_file)
#     response=get_gemini_response(input_prompt, image_data,input)
#     st.subheader("Response")
#     st.write(response)


import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from PIL import Image
import base64

# Load environment variables
load_dotenv()

# Configure API
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="CalorieScan", page_icon="🍎")
st.title("🍎 CalorieScan")

uploaded_file = st.file_uploader("Upload food image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Analyze Calories"):
        with st.spinner("Analyzing..."):
            try:
                # Read image bytes
                image_bytes = uploaded_file.getvalue()
                
                # Create the prompt
                prompt = """Analyze this food image and list:
                1. Each food item with calories
                2. Total calories
                3. Brief nutritional breakdown"""
                
                # Generate response
                response = client.models.generate_content(
                    model='gemini-2.0-flash-exp',
                    contents=[
                        prompt,
                        {"mime_type": uploaded_file.type, "data": image_bytes}
                    ]
                )
                
                st.subheader("Analysis")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

