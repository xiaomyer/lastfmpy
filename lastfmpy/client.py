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

from . import request
from . import objects


class LastFMClient:
    def __init__(self, api: str):
        self.api = api
        self.album = self.albums = Album(api)
        self.artist = self.artists = Artist(api)
        self.chart = self.charts = Chart(api)
        self.track = self.tracks = Track(api)


async def LastFM(api: str) -> LastFMClient:
    return LastFMClient(api)


class Album:
    def __init__(self, api):
        self.api = api

    async def get_info(self, artist: str, album: str, *, autocorrect: bool = False,
                       username: str = None) -> objects.Album:
        json = await request.get(self.api, "album.getinfo", artist=artist, album=album, autocorrect=autocorrect,
                                 username=username)
        return objects.Album(json["album"])

    async def get_top_tags(self, artist: str, album: str, *, autocorrect: bool = False, username: str = None) -> list:
        json = await request.get(self.api, "album.gettoptags", artist=artist, album=album, autocorrect=autocorrect,
                                 username=username)
        return [objects.Tag(tag) for tag in json["toptags"]["tag"]]

    async def search(self, album: str, *, limit: int = 0, page: int = 0) -> objects.SearchPage:
        json = await request.get(self.api, "album.search", album=album, limit=limit, page=page)
        return objects.SearchPage(json["results"], objects.Album, "albummatches")


class Artist:
    def __init__(self, api):
        self.api = api

    async def get_info(self, artist: str, *, autocorrect: bool = False, username: str = None) -> objects.Artist:
        json = await request.get(self.api, "artist.getinfo", artist=artist, autocorrect=autocorrect,
                                 username=username)
        return objects.Artist(json["artist"])

    async def get_correction(self, artist: str) -> objects.Artist:
        json = await request.get(self.api, "artist.getcorrection", artist=artist)
        return objects.Artist(json["artist"])

    async def get_similar(self, artist: str, *, autocorrect: bool = False, limit: int = 0) -> list:
        json = await request.get(self.api, "artist.getsimilar", artist=artist, limit=limit, autocorrect=autocorrect)
        return [objects.Track(track) for track in json["similarartists"]["artist"]]

    async def get_top_albums(self, artist: str, *, autocorrect: bool = False, limit: int = 0, page: int = 0) -> list:
        json = await request.get(self.api, "artist.gettopalbums", artist=artist, limit=limit, page=page,
                                 autocorrect=autocorrect)
        return [objects.Track(track) for track in json["topalbums"]["album"]]

    async def get_top_tags(self, artist: str, *, autocorrect: bool = False) -> list:
        json = await request.get(self.api, "artist.gettoptags", artist=artist, autocorrect=autocorrect)
        return [objects.Tag(tag) for tag in json["toptags"]["tag"]]

    async def get_top_tracks(self, artist: str, *, autocorrect: bool = False, limit: int = 0, page: int = 0) -> list:
        json = await request.get(self.api, "artist.gettoptracks", artist=artist, limit=limit, page=page,
                                 autocorrect=autocorrect)
        return [objects.Track(track) for track in json["toptracks"]["track"]]

    async def search(self, artist: str, *, limit: int = 0, page: int = 0) -> objects.SearchPage:
        json = await request.get(self.api, "artist.search", artist=artist, limit=limit, page=page)
        return objects.SearchPage(json["results"], objects.Artist, "artist")


class Chart:
    def __init__(self, api):
        self.api = api

    async def get_top_artists(self, *, page: int = 0, limit: int = 0):
        json = await request.get(self.api, "chart.gettopartists", limit=limit, page=page)
        return objects.TopObjectPage(json["artists"], objects.Artist, "artist")

    async def get_top_tags(self, *, page: int = 0, limit: int = 0):
        json = await request.get(self.api, "chart.gettoptags", limit=limit, page=page)
        return objects.TopObjectPage(json["tags"], objects.Tag, "tag")

    async def get_top_tracks(self, *, page: int = 0, limit: int = 0):
        json = await request.get(self.api, "chart.gettoptracks", limit=limit, page=page)
        return objects.TopObjectPage(json["tracks"], objects.Tag, "track")


class Track:
    def __init__(self, api):
        self.api = api

    async def get_info(self, track: str, *, autocorrect: bool = False, username: str = None) -> objects.Track:
        json = await request.get(self.api, "track.getinfo", track=track, autocorrect=autocorrect,
                                 username=username)
        return objects.Track(json["track"])

    async def get_correction(self, track: str) -> objects.Track:
        json = await request.get(self.api, "track.getcorrection", track=track)
        return objects.Track(json["track"])

    async def get_similar(self, track: str, *, autocorrect: bool = False, limit: int = 0) -> list:
        json = await request.get(self.api, "track.getsimilar", track=track, limit=limit, autocorrect=autocorrect)
        return [objects.Track(track) for track in json["similartracks"]["track"]]

    async def get_top_tags(self, track: str, *, autocorrect: bool = False) -> list:
        json = await request.get(self.api, "track.gettoptags", track=track, autocorrect=autocorrect)
        return [objects.Tag(tag) for tag in json["toptags"]["tag"]]

    async def search(self, track: str, *, limit: int = 0, page: int = 0) -> objects.SearchPage:
        json = await request.get(self.api, "track.search", track=track, limit=limit, page=page)
        return objects.SearchPage(json["results"], objects.Track, "track")
