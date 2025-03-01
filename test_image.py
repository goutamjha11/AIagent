import os
from dotenv import load_dotenv
from openai import OpenAI
# from langchain.llms import OpenAI
# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import base64
# from openai import OpenAI

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "images/InputForm_Error_Sample 2.png"

# Getting the Base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    # model="gpt-4o-mini",   ## (gpt-4o, gpt-4-vision-preview, gpt-4-turbo
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "give me the errors in chart format?",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
    stream=True

)
streamed_text= ""
for chunk in response:
    if chunk.choices[0].delta.content:
        streamed_text += chunk.choices[0].delta.content
print(streamed_text)
pass