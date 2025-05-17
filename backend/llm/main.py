import json
from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from typing import List
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
from fastapi.middleware.cors import CORSMiddleware

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
    payload.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{1}",
                },
            ],
        }
    )
    payload.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{2}",
                },
            ],
        }
    )
    return {"Hello": "Ping"}

def create_payload(role: str, label: str, filename: str, text: str):
    return {
        "role": role,
        "content": [
            {"type": "text", "text": label},
            {"type": "text", "text": text},
        ],
    }
    
@app.post("/llm/analyze")
async def analyze_code (websiteURL: str = Form(...), htmlFile: List[UploadFile] = File(default=[]), cssFiles: List[UploadFile] = File(default=[])):
    payload = []

    for file in htmlFile:
        content = (await file.read()).decode("utf-8")
        payload.append(create_payload("user", "HTML File", file.filename, content))

    for i, file in enumerate(cssFiles):
        content = (await file.read()).decode("utf-8")
        payload.append(create_payload("user", f"CSS File {i + 1}: {file.filename}", file.filename, content))


    messages = [
        {
            "role": "system",
            "content": "You are a designer of websites. You will be provided with files of a website. There's one HTML file and several CSS files. Your goal will be to evaluate design of website based on code in files according following criteria: color palette, contrast (between text and its background), whitespace/margins(balanced amount), layout/grid alignment, typography, visual hierarchy(scale/text/color emphasis), visual complexity(traditional/minimalist/busy). For each attribute provide the output and the grade from 0 to 100. Give a final grade from 0 to 100. Write everything in Russian language.",
        }
    ]

    messages = messages + payload

    response = client.chat.completions.create(
        model="openai/o4-mini",
        messages=messages,
        n=1,
        max_tokens=2000,
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
                                    "grade": {"type" : "string"},
                                    "output": {"type": "string"},
                                },
                                "required": ["attribute", "output", "grade"],
                                "additionalProperties": False,
                            },
                        },
                        "final_grade": {"type": "string"},
                    },
                    "required": ["criteria", "final_grade"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    )

    print("Response:", response)
    print(response.choices[0].message.content)
    raw_json_string = response.choices[0].message.content
    parsed_message = json.loads(raw_json_string)
    return {"message": parsed_message}



@app.post("/vlm/analyze")
async def analyze_images(
    websiteURL: str = Form(...), image: List[UploadFile] = File(default=[])
):
    payload = []

    for index, img in enumerate(image):
        content = await img.read()
        base64_image = base64.b64encode(content).decode("utf-8")
        payload.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Image {index + 1}"},
                    {
                        "type": "image_url",
                        "image_url": f"data:{img.content_type};base64,{base64_image}",
                    },
                ],
            }
        )

    messages = [
        {
            "role": "system",
            "content": "You are a designer of websites. You will be provided with images of a website. Your goal will be to evaluate website photos according following criteria: color palette, contrast (between text and its background), whitespace/margins(balanced amount), layout/grid alignment, typography, visual hierarchy(scale/text/color emphasis), visual complexity(traditional/minimalist/busy). For each attribute provide the output and the grade from 0 to 100. If the score is less than 90, in the output additionally write exactly why you have lowered the score. Give a final grade from 0 to 100. Write everything in Russian language.",
        }
    ]

    messages = messages + payload

    response = client.chat.completions.create(
        model="vis-openai/gpt-4o-2024-08-06",
        # model="vis-openai/o4-mini",
        messages=messages,
        n=1,
        max_tokens=1000,
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
                                    "grade": {"type" : "string"},
                                    "output": {"type": "string"},
                                },
                                "required": ["attribute", "output", "grade"],
                                "additionalProperties": False,
                            },
                        },
                        "final_grade": {"type": "string"},
                    },
                    "required": ["criteria", "final_grade"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    )

    print("Response:", response)
    print(response.choices[0].message.content)
    raw_json_string = response.choices[0].message.content
    parsed_message = json.loads(raw_json_string)
    
    return {"message": parsed_message}
