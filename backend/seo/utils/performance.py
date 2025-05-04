import os
from typing import Union
from fastapi import logger
import httpx
from models.analysis import ErrorResult, Performance, PerformanceMetrics


async def fetch_performance_data(
    url: str, client: httpx.AsyncClient, strategy: str
) -> Union[PerformanceMetrics, ErrorResult]:
    api_key = os.getenv("GOOGLE_API_KEY")
    api_url = (
        f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        f"?url={url}&key={api_key}&strategy={strategy}&category=performance"
    )

    try:
        response = await client.get(api_url)
        data = response.json()

        if response.status_code == 200:
            try:
                return PerformanceMetrics(
                    performance_score=int(
                        data["lighthouseResult"]["categories"]["performance"]["score"]
                        * 100
                    ),
                    first_contentful_paint=data["lighthouseResult"]["audits"][
                        "first-contentful-paint"
                    ]["displayValue"],
                    largest_contentful_paint=data["lighthouseResult"]["audits"][
                        "largest-contentful-paint"
                    ]["displayValue"],
                    cumulative_layout_shift=data["lighthouseResult"]["audits"][
                        "cumulative-layout-shift"
                    ]["displayValue"],
                    total_blocking_time=data["lighthouseResult"]["audits"][
                        "total-blocking-time"
                    ]["displayValue"],
                    speed_index=data["lighthouseResult"]["audits"]["speed-index"][
                        "displayValue"
                    ],
                )
            except (KeyError, TypeError) as parse_error:
                logger.error(
                    f"Failed to parse {strategy} performance data: {parse_error}"
                )
                return ErrorResult(
                    error=f"Failed to parse {strategy} performance data: {parse_error}"
                )
        else:
            logger.error(
                f"{strategy.capitalize()} - Non-200 status: {response.status_code}"
            )
            return ErrorResult(
                error=f"{strategy.capitalize()} status code is not 200: {response.status_code}"
            )
    except httpx.RequestError as e:
        logger.error(
            f"{strategy.capitalize()} request failed: {type(e).__name__} - {e}"
        )
        return ErrorResult(
            error=f"{strategy.capitalize()} request error: {type(e).__name__}: {e}"
        )


async def check_performance_metrics(
    url: str, client: httpx.AsyncClient
) -> Union[Performance, ErrorResult]:
    mobile_result = await fetch_performance_data(url, client, "mobile")
    desktop_result = await fetch_performance_data(url, client, "desktop")

    if isinstance(mobile_result, ErrorResult):
        return mobile_result
    if isinstance(desktop_result, ErrorResult):
        return desktop_result

    return Performance(mobile=mobile_result, desktop=desktop_result)
