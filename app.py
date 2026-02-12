import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from PIL import Image

#backend
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

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




def get_gemini_response(input_text, image_data, prompt):
    """Generate response from Gemini model"""
    try:
        # Prepare the content parts
        contents = [prompt]
        
        if input_text:
            contents.append(input_text)
        
        # Add image
        contents.append(types.Part.from_bytes(
            data=image_data['data'],
            mime_type=image_data['mime_type']
        ))
        
        # Generate content using the new API
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',  # Using latest model
            contents=contents
        )
        
        return response.text
    
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

def input_image_setup(uploaded_file):
    """Process uploaded image"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_data = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_data
    else:
        raise FileNotFoundError("No file uploaded")

# Frontend - Streamlit app
st.set_page_config(page_title="CalorieScan", page_icon="🍎")

st.title("🍎 CalorieScan")
st.write("Upload a food image to analyze its nutritional content")

# Input section
input_text = st.text_input("Additional instructions (optional):", 
                           placeholder="e.g., Focus on protein content")

uploaded_file = st.file_uploader("Choose an image...", 
                                 type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit = st.button("🔍 Analyze Calories", type="primary")

# Nutrition analysis prompt
input_prompt = """
You are an expert nutritionist. Analyze the food items in the image
and calculate the total calories. Provide details of every food item with calorie intake
in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
3. Item 3 - number of calories
----
----
Total Calories: X kcal

Also provide a brief nutritional assessment (protein, carbs, fats, vitamins).
"""

# Process when submit button is clicked
if submit:
    if uploaded_file is not None:
        with st.spinner("🔄 Analyzing your food image..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_text, image_data, input_prompt)
                
                if response:
                    st.subheader("📊 Nutritional Analysis")
                    st.write(response)
                    
                    # Add download option
                    st.download_button(
                        label="📥 Download Analysis",
                        data=response,
                        file_name="calorie_analysis.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("❌ Failed to get response from the model.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please upload an image first!")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini AI")

