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
        async with aiofiles.open(filepath, mode="r", encoding="utf-8") as f:
            content = await f.read()
            words = content.split()
            stopwords.update(word.strip().lower() for word in words if word.strip())
    return stopwords


# https://github.com/stopwords-iso/stopwords-ru/blob/master/stopwords-ru.txt
# https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt
async def create_word_cloud(
    url: str, client: httpx.AsyncClient
) -> Union[WordCloudResult, ErrorResult]:
    try:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

            words = re.findall(r"\b\w+\b", text.lower())
            word_counts = Counter(words)

            stopwords = await load_stopwords(["stopwords-en.txt", "stopwords-ru.txt"])
            filtered_counts = {
                word: count
                for word, count in word_counts.items()
                if word not in stopwords and len(word) > 2
            }

            word_cloud_data = [
                {"text": word, "value": count}
                for word, count in filtered_counts.items()
            ]

            return WordCloudResult(data=word_cloud_data)
        else:
            return ErrorResult(error="Status code is not 200")
    except httpx.RequestError as e:
        return ErrorResult(error=str(e))


async def get_distribution_of_keywords(
    url: str, client: httpx.AsyncClient, top_n: int = 10
) -> Union[dict, ErrorResult]:
    try:
        response = await client.get(url)
        if response.status_code != 200:
            return ErrorResult(error="Failed to fetch page content.")

        soup = BeautifulSoup(response.content, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        full_text = soup.get_text(separator=" ", strip=True).lower()
        words = re.findall(r"\b\w+\b", full_text)

        stopwords = await load_stopwords(["stopwords-en.txt", "stopwords-ru.txt"])
        filtered_words = [
            word for word in words if word not in stopwords and len(word) > 2
        ]
        top_keywords = [word for word, _ in Counter(filtered_words).most_common(top_n)]

        headings_text = " ".join(
            tag.get_text() for tag in soup.find_all(["h1", "h2", "h3"])
        )

        important_tags = {
            "title": soup.title.string if soup.title else "",
            "description": soup.find("meta", attrs={"name": "description"}),
            "headings": headings_text,
        }

        if important_tags["description"]:
            important_tags["description"] = important_tags["description"].get(
                "content", ""
            )
        else:
            important_tags["description"] = ""

        distribution = {}

        for tag, content in important_tags.items():
            content_words = re.findall(r"\b\w+\b", content.lower())
            keyword_matches = {
                keyword: content_words.count(keyword)
                for keyword in top_keywords
                if keyword in content_words
            }
            distribution[tag] = keyword_matches

        total_counts = {
            keyword: filtered_words.count(keyword) for keyword in top_keywords
        }
        distribution["total"] = total_counts

        return distribution

    except Exception as e:
        return ErrorResult(error=str(e))
