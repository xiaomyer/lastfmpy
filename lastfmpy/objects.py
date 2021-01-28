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

from datetime import datetime


class Album:
    def __init__(self, json: dict):
        self.name = json.get("name") or json.get("#text")
        self.artist = Artist(json.get("artist")) if isinstance(json.get("artist"), dict) else json.get("artist")
        self.releasedate = json.get("releasedate")  # TODO: figure out the format of this and make it a datetime object
        self.image = [Image(image) for image in json.get("image", {})]
        self.stats = Stats(json)
        self.toptags = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.tracks = [Track(track) for track in json.get("tracks", {}).get("track", {})]
        self.wiki = Info(json.get("wiki", {}))
        self.url = json.get("url")

    def __str__(self):
        return self.name


class Track:
    def __init__(self, json: dict):
        self.name: str = json.get("name")
        self.artist = Artist(json.get("artist")) if isinstance(json.get("artist"), dict) else json.get("artist")
        self.album = Album(json.get("album", {}))
        self.duration: int = json.get("duration")
        self.releasedate: str = json.get("release_date")  # see above
        self.image: list = [Image(image) for image in json.get("image", {})]
        self.stats: Stats = Stats(json)
        self.toptags: list = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.playing = self.now_playing = True if json.get("@attr", {}).get("nowplaying") == "true" else False
        self.played = datetime.utcfromtimestamp(int(json.get("date", {}).get("uts", 0)))
        self.url: str = json.get("url")

    def __str__(self):
        return self.name


class Artist:
    def __init__(self, json: dict):
        self.name: str = json.get("name") or json.get("#text")
        self.image: list = [Image(image) for image in json.get("image", {})]
        self.stats: Stats = Stats(json)
        self.tags: list = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.similar: list = [Artist(artist) for artist in json.get("similar", {}).get("artists", {})]
        self.bio: Info = Info(json.get("bio", {}))
        self.url: str = json.get("url")

    def __str__(self):
        return self.name


class Stats:
    def __init__(self, json: dict):
        self.listeners: int = json.get("stats", {}).get("listeners") or json.get("listeners")
        self.playcount: int = json.get("stats", {}).get("playcount") or json.get("playcount")
        self.userplaycount: int = json.get("stats", {}).get("userplaycount") or json.get("userplaycount") or json.get("playcount")
        # inconsistent api!


class Image:
    def __init__(self, json: dict):
        self.url: str = json.get("#text")
        self.size: str = json.get("size")


class Tag:
    def __init__(self, json: dict):
        self.name: str = json.get("name")
        self.url: str = json.get("url")
        self.count: int = json.get("count")

    def __str__(self):
        return self.name


class Info:
    def __init__(self, json: dict):
        self.summary: str = json.get("summary")
        self.content: str = json.get("content")
        self.published: str = json.get("published")


class SearchPage:
    def __init__(self, json: dict, object_, string: str):
        self.results: int = json.get("opensearch:totalResults")
        self.matches = self.items = [object_(item) for item in json.get(string + "matches", {}).get(string)]
        # lastfm api weird


class ObjectPage:
    def __init__(self, json: dict, object_, string: str):
        self.results = self.items = self.matches = [object_(item) for item in json.get(string)]
        self.page: int = json.get("@attr").get("page")
        self.per_page: int = json.get("@attr").get("perPage")
        self.pages: int = json.get("@attr").get("totalPages")
        self.total: int = json.get("@attr").get("total")
        self.from_ = datetime.utcfromtimestamp(int(json.get("@attr", {}).get("from", 0)))
        self.to = datetime.utcfromtimestamp(int(json.get("@attr", {}).get("to", 0)))


class User:
    def __init__(self, json: dict):
        self.name = self.username = json.get("name")
        self.real_name: str = json.get("realname")
        self.url: str = json.get("url")
        self.image: list = [Image(image) for image in json.get("image", {})]
        self.country = json.get("country") if json.get("country") != "None" else None
        # yes for our json api was should make none be expressed as a string and not as null
        self.age: int = json.get("age")
        self.playcount = self.scrobbles = json.get("playcount")
        self.playlists: int = json.get("playlists")
        self.bootstrap: int = json.get("bootstrap")  # no clue what this is
        self.registered = self.created_at = datetime.utcfromtimestamp(int(json.get("registered", {}).get("unixtime", 0)))
