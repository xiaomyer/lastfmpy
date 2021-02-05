# lastfmpy - Last.FM API wrapper written in Python

[![widget](https://inv.wtf/widget/myerfire)](https://myer.wtf/discord)

Maintained by [Myer (also known as myerfire, MyerFire)](https://github.com/myerfire)

- [YouTube](https://myer.wtf/youtube)
- [Twitter](https://myer.wtf/twitter)
- myer#0001 on Discord

This library is an async wrapper for the [last.fm API](https://last.fm/api).

## Features

- Currently, any API methods that do not require the authentication process are supported.

## Installation

`lastfmpy` is available from the official pYpI package index.

`python -m pip install -U lastfmpy`

## Documentation

- There are relevant docstrings on the functions of the main wrapper class.
- Object attribute documentation may (?) be worked on but the code
  in [objects.py](https://github.com/MyerFire/lastfmpy/blob/master/lastfmpy/objects.py) is easily readable.
- There is no API method for a user's currently playing song. The way to get the currently playing song of a user is
  to request recent tracks and check whether the first index of the list has the attribute `playing` set to true.
    - **UPDATE** - There is now a utility function in the `User` object of the `Client` that does this for you: `get_now_playing(user)`

## Quick Start

```python
from lastfmpy import LastFM
import asyncio

API_KEY = "hahagetbaited"
# if it isn't obvious enough, replace this string 
# with your API key obtained by going to https://last.fm/api/applications and creating an application

async def main():
    lastfm = await LastFM(API_KEY)
    recent = await lastfm.user.get_recent_tracks(user="myerfire")
    print(f"{recent.items[0].name}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
```