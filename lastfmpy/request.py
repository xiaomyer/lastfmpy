"""
MIT License

Copyright (c) 2020 Myer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import aiohttp
from . import exceptions


URL = "http://ws.audioscrobbler.com/2.0"


async def get(api: str, method: str, **kwargs) -> dict:
    """
    Sends a get request to the last.fm API
    :param api: API key
    :param method: last.fm API method
    :param kwargs: Will be converted to HTTP attributes (&key=value)
    :return: dict (JSON) of the API response
    """
    parameters = "".join([f"&{key}={value}" for key, value in kwargs.items() if bool(value)])
    if kwargs.get("from_"):  # keywords go brr
        parameters += f"&from={kwargs.get('from_')}"
    async with aiohttp.request("GET", f"{URL}?method={method}{parameters}&api_key={api}&format=json") as response:
        json = await response.json()
    if bool(json.get("error")):
        if json["error"] == 6:
            raise exceptions.InvalidInputError(json["message"])
        elif json["error"] == 11:
            raise exceptions.ServiceOfflineError(json["message"])
        elif json["error"] == 29:
            raise exceptions.RatelimitExceededError(json["message"])
    return json
