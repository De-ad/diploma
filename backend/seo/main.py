from urllib.parse import urlparse
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import logging
from utils import operations

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

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


class Website(BaseModel):
    url: str


def strip_url(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return f"{parsed_url.scheme}://{parsed_url.netloc}"
    else:
        raise ValueError("URL is invalid or missing scheme")


@app.post("/seo/analyze")
async def analyze_code(website: Website):
    return await operations.analyze(strip_url(website.url))
