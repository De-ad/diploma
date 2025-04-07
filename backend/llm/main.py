from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from typing import List
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

app = FastAPI()
load_dotenv()
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

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
    payload = []
    payload.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{1}",
                    },
                ],
            } )
    payload.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{2}",
                    },
                ],
            } )
    logger.debug(payload)
    return {"Hello": "Ping"}

@app.post("/llm/analyze")
def analyze_code():
    return {"message": "LLM analysis is not implemented yet"}


@app.post("/vlm/analyze")
async def analyze_images(websiteURL: str = Form(...), image: List[UploadFile] = File(default=[])):

    results = {
        "websiteURL": websiteURL,
        "images": []
    }
    
    payload = []

    for img in image:
        content = await img.read()
        base64_image = base64.b64encode(content).decode("utf-8")
        results["images"].append({
            "filename": img.filename,
            "content_type": img.content_type,
            "base64": base64_image
        })
        payload.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            } )
        

    
    messages = [
    {"role": "system", "content": "You are a designer of websites. You will be provided with an image of a website. Your goal will be to evaluate a website photo according following criteria: color scheme, typography, spacing & alignment. For each attribute provide the output and give a final grade from 0 to 100"}
    ]
    

    messages = messages + payload
    logger.debug(messages)
        
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

    

    return {"message": response.choices[0].message.content}
