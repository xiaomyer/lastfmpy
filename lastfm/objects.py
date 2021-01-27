from datetime import datetime


class Album:
    def __init__(self, json):
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
    def __init__(self, json):
        self.name = json.get("name")
        self.artist = json.get("artist")
        self.duration = json.get("duration")
        self.releasedate = json.get("release_date")  # see above
        self.image = [Image(image) for image in json.get("image", {})]
        self.stats = Stats(json)
        self.toptags = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.url = json.get("url")

    def __str__(self):
        return self.name


class Artist:
    def __init__(self, json):
        self.name = json.get("name")
        self.image = [Image(image) for image in json.get("image", {})]
        self.stats = Stats(json)
        self.tags = [Tag(tag) for tag in json.get("tags", {}).get("tag", {})]
        self.similar = [Artist(artist) for artist in json.get("similar", {}).get("artists", {})]
        self.bio = Info(json.get("bio"))
        self.url = json.get("url")

    def __str__(self):
        return self.name


class Stats:
    def __init__(self, json):
        self.listeners = json.get("listeners")
        self.playcount = json.get("playcount")


class Image:
    def __init__(self, json):
        self.url = json.get("#text")
        self.size = json.get("size")


class Tag:
    def __init__(self, json):
        self.name = json.get("name")
        self.url = json.get("url")
        self.count = json.get("count")

    def __str__(self):
        return self.name


class Info:
    def __init__(self, json):
        self.summary = json.get("summary")
        self.content = json.get("content")
        self.published = json.get("published")


class Search:
    def __init__(self, json, object_, string):
        self.results = json.get("opensearch:totalResults")
        self.matches = [object_(item) for item in json.get(string)]
