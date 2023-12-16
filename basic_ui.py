import streamlit as st
import google.generativeai as genai
import io
import os
from PIL import Image
import pybtex as pb
import google.ai.generativelanguage as glm

class API_config():
    def __init__(self):
        self.generation_config = {"temperature": 1, "top_p": 1, "top_k": 1, "max_output_tokens": 4096}
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]

    def get_api_key(self, api_key):
        genai.configure(api_key=api_key)

    def get_response(self, message, model='gemini-pro'):
        model = genai.GenerativeModel(
            model,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        res = model.generate_content(message, stream=True)
        return res


prompt_parts = ["You're a researcher writing an article, using all of your knowledge about design patterns and LaTeX best practices. Optimize the citation format to adhere to the BibTeX style, omitting any abstracts if present. Strive for efficiency in the overall document structure and citation presentation:\n",]

with st.sidebar:
    st.title('easyTex')
    st.write("Powered by GERAIA")
    
    api_key = st.text_input("API key")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        if "api_key" in st.secrets:
            genai.configure(api_key=st.secrets["api_key"])
        else:
            st.error("Missing API key.")

tab1, tab2 = st.tabs(['BibTex format', 'Coming soon'])

with tab1:
    st.subheader("Input your citations and the magic is complete")
    col1, col2 = st.columns(2)
    
    with col1:
        input_text = st.text_area(
            'Input',
            placeholder = 'Enter your citation'
        )
        send_button = st.button('Send input')

    with col2:
        output_text = st.text_area(
            'Output'
        )
        download_button = st.download_button(label='Download', data=output_text, key='download_button')

    # st.caption(f'You used X tokens, still Y tokens remaining.')
if send_button:
  instance = API_config()
  
  prompt_parts.append(input_text)
  
  # Call the get_response method on the instance
  response_generator = instance.get_response(prompt_parts)
  
  # Iterate over the generator and update the output text area
  for content in response_generator:
      content = response_generator.generate_content
      output_text = content