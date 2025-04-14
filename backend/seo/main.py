from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import logging

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

@app.post("/seo/analyze")
def analyze_code():
    return {"message": "LLM analysis is not implemented yet"}


