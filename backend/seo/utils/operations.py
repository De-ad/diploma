import httpx

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

def check_ssl_certificate():
    return

def check_mobile_performance_metrics():
    return

def check_desktop_performace_metrics():
    return

# inline css, metadata, deprecated, headers structure, title, description, favicon, image seo, 
def check_http_code(url):
    return