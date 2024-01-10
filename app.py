import os
import io
import base64
import json
import requests
import streamlit as st


auth_key = os.environ["AUTH_KEY"]
url = os.environ["ENDPOINT_URL"]

headers = {
  'Authorization': auth_key,
  'Content-Type': 'application/json'
}

st.set_page_config(initial_sidebar_state="collapsed")

st.title("Image to text frontend app")

prompt = st.text_input("Provide prompt", value="An android toy near the Eiffel Tower")

temperature = st.sidebar.slider(label='temperature', min_value=0.1, max_value=5.0, value=1.0, step=0.1)
guidance_scale = st.sidebar.slider(label='guidance scale', min_value=0.1, max_value=15.0, value=7.5, step=0.1)
num_inference_steps = st.sidebar.slider(label='number of inference steps', min_value=1, max_value=100, value=50, step=1)
seed = st.sidebar.slider(label='seed', min_value=1, max_value=100, value=42, step=1)

press_button = st.button('Generate image')
if press_button:
    if prompt:
        with st.spinner(text="This may take a moment..."):
            payload = json.dumps({
                "prompt": prompt, 
                "guidance_scale": guidance_scale, 
                "num_inference_steps": num_inference_steps, 
                "seed": seed, 
                "temperature": temperature
                })
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                response_data = response.json()
                generated_image = response_data["result"]["generated_image"]
                st.write("Result:")
                st.write(generated_image)
            except:
                st.error("There is no response, try again later")
    else:
        st.text("Please, specify a prompt")