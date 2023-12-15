import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBgBfjlWEoaMdXS8GbYLOWEUaGFz0XQmag")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

prompt_parts = [
    "You're a researcher writing an article, using all of your knowledge about design patterns and LaTeX best practices. Format the citations to BibTeX style, removing the abstracts if has any, and make it more efficient: ",
]

# Get user input
users_input = input('Enter the citation details: ')

# Construct BibTeX entry with user input
bibtex_entry = f"""
@incollection{{CUSTOM_ENTRY,
  {users_input}
}}
"""

# Concatenate BibTeX entry with prompt_parts
prompt_parts.append(bibtex_entry)

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

response = model.generate_content(prompt_parts)
print(response.text)
