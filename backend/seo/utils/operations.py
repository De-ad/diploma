from bs4 import BeautifulSoup
import httpx
import socket
import ssl
import re
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

async def check_if_robots_file_is_present(url: str):
    url = f"{url.rstrip('/')}/robots.txt"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return {
                    "found": True,
                    "status_code": response.status_code,
                    "message": "robots.txt is found"
                }
            else:
                return {
                    "found": False,
                    "status_code": response.status_code,
                    "message": "robots.txt not found"
                }
        except httpx.RequestError as e:
            return {"error": str(e)}


async def check_if_sitemap_file_is_present(url: str):
    url = f"{url.rstrip('/')}/sitemap.xml"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return {
                    "found": True,
                    "status_code": response.status_code,
                    "message": "sitemap.xml is found"
                }
            else:
                return {
                    "found": False,
                    "status_code": response.status_code,
                    "message": "sitemap.xml not found"
                }
        except httpx.RequestError as e:
            return {"error": str(e)}

def check_ssl_certificate(url: str):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=url) as s:
            s.connect((url, 443))

        return {
                    "result": "has valid cert"
                }

    except Exception as e:
         return {
                    "result": "has invalid cert" +str(e)
                }

async def check_performance_metrics(url: str):
    api_key = os.getenv("API_KEY")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    return {"error": "Invalid JSON response", "raw": response.text}

                if 'error' in data:
                    return {"error": data["error"]["message"], "details": data["error"]}

                try:
                    performance_score = data['lighthouseResult']['categories']['performance']['score'] * 100
                    fcp = data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
                    lcp = data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
                    cls = data['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
                    tbt = data['lighthouseResult']['audits']['total-blocking-time']['displayValue']

                    return {
                        "performanceScore": performance_score,
                        "firstContentfulPaint": fcp,
                        "largestContentfulPaint": lcp,
                        "cumulativeLayoutShift": cls,
                        "totalBlockingTime": tbt
                    }
                except KeyError as e:
                    return {"error": f"Missing expected data in response: {e}", "data": data}

            else:
                return {
                    "status_code": response.status_code,
                    "message": "Non-200 response",
                    "body": response.text
                }
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}

async def create_word_cloud(url: str):
     async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                for tag in soup(['script', 'style', 'noscript']):
                    tag.decompose()

                text = soup.get_text(separator=' ', strip=True)
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

                img_io = io.BytesIO()
                wordcloud.to_image().save(img_io, format='PNG')
                img_io.seek(0)

                img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
                return {'image': f"data:image/png;base64,{img_base64}"}
                
            else:
                return {
                    "message": "error"
                }
        except httpx.RequestError as e:
            return {"error": str(e)}

  

   

# inline css, metadata, deprecated, headers structure, title, description, favicon, image seo, 
def check_http_code(url):
    return