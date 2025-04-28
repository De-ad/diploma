from collections import Counter
import os
import re
from typing import List, Set, Union
import aiofiles
from bs4 import BeautifulSoup
import httpx
from models.analysis import ErrorResult, WordCloudResult

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
async def load_stopwords(filepaths: List[str]) -> Set[str]:
    stopwords = set()
    for filepath in filepaths:
        filepath = os.path.join(BASE_DIR, filepath)
        async with aiofiles.open(filepath, mode='r', encoding='utf-8') as f:
            content = await f.read()
            words = content.split()
            stopwords.update(word.strip().lower() for word in words if word.strip())
    return stopwords

# https://github.com/stopwords-iso/stopwords-ru/blob/master/stopwords-ru.txt
# https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt
async def create_word_cloud(url: str,  client: httpx.AsyncClient) -> Union[WordCloudResult, ErrorResult]:
    try:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            for tag in soup(['script', 'style', 'noscript']):
                tag.decompose()

            text = soup.get_text(separator=' ', strip=True)

            words = re.findall(r'\b\w+\b', text.lower())
            word_counts = Counter(words)

            stopwords = await load_stopwords(["stopwords-en.txt", "stopwords-ru.txt"])
            filtered_counts = {word: count for word, count in word_counts.items() if word not in stopwords and len(word) > 2}

            word_cloud_data = [{"text": word, "value": count} for word, count in filtered_counts.items()]

            return WordCloudResult(
                data=word_cloud_data
            )
        else:
            return ErrorResult(error="Status code is not 200")
    except httpx.RequestError as e:
        return ErrorResult(error=str(e))
