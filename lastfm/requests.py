import aiohttp
import exceptions


URL = "http://ws.audioscrobbler.com/2.0"


async def get(api: str, method: str, **kwargs) -> dict:
    parameters = "".join([f"&{key}={value}" for key, value in kwargs.items() if bool(value)])
    async with aiohttp.ClientSession() as session:
        json = await (
            await session.get(f"{URL}?method={method}{parameters}&api_key={api}&format=json")).json()
    if bool(json.get("error")):
        if json["error"] == 6:
            raise exceptions.InvalidInput
    return json
