import os
from typing import Union
from fastapi import logger
import httpx
from models.analysis import ErrorResult, Performance


async def check_performance_metrics(
    url: str, client: httpx.AsyncClient
) -> Union[Performance, ErrorResult]:
    api_key = os.getenv("GOOGLE_API_KEY")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"

    try:
        response = await client.get(api_url)
        data = response.json()
        if response.status_code == 200:
            try:
                performance_score = (
                    data["lighthouseResult"]["categories"]["performance"]["score"] * 100
                )
                fcp = data["lighthouseResult"]["audits"]["first-contentful-paint"][
                    "displayValue"
                ]
                lcp = data["lighthouseResult"]["audits"]["largest-contentful-paint"][
                    "displayValue"
                ]
                cls = data["lighthouseResult"]["audits"]["cumulative-layout-shift"][
                    "displayValue"
                ]
                tbt = data["lighthouseResult"]["audits"]["total-blocking-time"][
                    "displayValue"
                ]

                return Performance(
                    performance_score=performance_score,
                    first_contentful_paint=fcp,
                    largest_contentful_paint=lcp,
                    cumulative_layout_shift=cls,
                    total_blocking_time=tbt,
                )
            except (KeyError, TypeError) as parse_error:
                logger.error(f"Failed to parse performance data: {parse_error}")
                return ErrorResult(
                    error=f"Failed to parse performance data: {parse_error}"
                )
        else:
            logger.error(f"Non-200 status: {response.status_code}")
            return ErrorResult(error=f"Status code is not 200: {response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Request failed: {type(e).__name__} - {e}")
        return ErrorResult(error=f"{type(e).__name__}: {e}")
