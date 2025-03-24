from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# openai_key from env
openai_key = os.getenv("API_KEY")


client = OpenAI(
    api_key=openai_key,
    base_url="https://api.vsegpt.ru/v1",

)

class Image(BaseModel):
    name: str
    base64_string: str


@app.get("/")
def read_root():
    return {"Hello": "Ping"}


@app.post("/llm/analyze")
def analyze_code():
    return {"message": "LLM analysis is not implemented yet"}


@app.post("/vlm/analyze")
def analyze_images(image: Image):

    messages = [
    {"role": "system", "content": "You are a designer of websites. You will be provided with an image of a website. Your goal will be to evaluate a website photo according following criteria: color scheme, typography, spacing & alignment. For each attribute provide the output and give a final grade from 0 to 100"},
    {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image.base64_string}",
                    },
                ],
            } 
    ]
    
        
    response =  client.chat.completions.create(  
        model="vis-openai/gpt-4o-2024-08-06",
        messages=messages,
        n=1,
        max_tokens=500,
        response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "visual_analysis",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "criteria": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "attribute": {"type": "string"},
                                        "output": {"type": "string"}
                                    },
                                    "required": ["attribute", "output"],
                                    "additionalProperties": False
                                }
                            },
                            "final_grade": {"type": "string"}
                        },
                        "required": ["criteria", "final_grade"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
    )

    print("Response:", response)
    print(response.choices[0].message.content)

    

    return {"name": image.name, "message": response.choices[0].message.content}