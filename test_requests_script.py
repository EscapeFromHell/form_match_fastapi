import json
import logging
import os
import asyncio

import httpx

from src.utils import get_logger

URL = "http://127.0.0.1:8000/api_v1/forms/get_form"

logger = get_logger(log_level=logging.DEBUG)


async def get_test_data() -> dict:
    """
    Load test request data from the "test_requests_data.json" file.

    Returns:
        dict: Test request data.
    """
    path = os.path.dirname(__file__)
    file_path = os.path.join(path, "test_requests_data.json")
    try:
        with open(file_path, "r") as file:
            test_data = json.load(file)
            return test_data
    except FileNotFoundError:
        logger.error("Error: test_requests_data.json not found!")
    except Exception as e:
        logger.error(f"Error during opening file! Detail: {e}")


async def async_request(method: str = "POST", url: str = URL, params: dict | None = None) -> dict:
    """
    Make an asynchronous HTTP request.

    Args:
        method (str): HTTP method.
        url (str): Request URL.
        params (dict): Request parameters.

    Returns:
        dict: JSON response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, params=params)
        return response.json()


async def execute(request_type: str, test_data: dict) -> None:
    """
    Execute asynchronous HTTP requests based on the specified request type.

    Args:
        request_type (str): Type of requests ("success", "not_found", or "validation_error").
        test_data (dict): Test request data.

    Returns:
        None
    """
    print(f"{request_type.capitalize()} requests:")
    tasks = [async_request(params=params) for params in test_data[request_type]]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


async def main() -> None:
    """
    Main asynchronous function to execute test requests.

    Returns:
        None
    """
    test_data = await get_test_data()
    await execute(request_type="success", test_data=test_data)
    await execute(request_type="not_found", test_data=test_data)
    await execute(request_type="validation_error", test_data=test_data)


if __name__ == "__main__":
    asyncio.run(main())
