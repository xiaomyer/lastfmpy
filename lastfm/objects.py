from datetime import datetime


class Album:
    def __init__(self, json: dict):
        self.name = json.get("name")
        self.artist = json.get("artist")
        self.releasedate = json.get("releasedate")  # TODO: figure out the format of this and make it a datetime object
        self.image = [Image(image) for image in json.get("image", {})]
        self.stats = Stats(json)
        self.toptags = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.tracks = [Track(track) for track in json.get("tracks", {}).get("track", {})]
        self.wiki = Info(json.get("wiki"))
        self.url = json.get("url")

    def __str__(self):
        return self.name


class Track:
    def __init__(self, json: dict):
        self.name: str = json.get("name")
        self.artist: str = json.get("artist")
        self.duration: int = json.get("duration")
        self.releasedate: str = json.get("release_date")  # see above
        self.image: list = [Image(image) for image in json.get("image", {})]
        self.stats: Stats = Stats(json)
        self.toptags: list = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.url: str = json.get("url")

    def __str__(self):
        return self.name


class Artist:
    def __init__(self, json: dict):
        self.name: str = json.get("name")
        self.image: list = [Image(image) for image in json.get("image", {})]
        self.stats: Stats = Stats(json.get("stats"))
        self.tags: list = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.similar: list = [Artist(artist) for artist in json.get("similar", {}).get("artists", {})]
        self.bio: Info = Info(json.get("bio"))
        self.url: str = json.get("url")

    def __str__(self):
        return self.name


class Stats:
    def __init__(self, json: dict):
        self.listeners: int = json.get("listeners")
        self.playcount: int = json.get("playcount")


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


class Search:
    def __init__(self, json: dict, object_, string: str):
        self.results: int = json.get("opensearch:totalResults")
        self.matches = [object_(item) for item in json.get(string)]
