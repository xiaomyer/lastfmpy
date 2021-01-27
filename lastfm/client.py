import requests
import objects


class LastFMClient:
    def __init__(self, api: str):
        self.api = api
        self.album = Album(api)
        self.artist = Artist(api)


async def LastFM(api: str) -> LastFMClient:
    return LastFMClient(api)


class Album:
    def __init__(self, api):
        self.api = api

    async def get_info(self, artist: str, album: str, *, autocorrect: bool = False,
                       username: str = None) -> objects.Album:
        json = await requests.get(self.api, "album.getinfo", artist=artist, album=album, autocorrect=autocorrect,
                                  username=username)
        return objects.Album(json["album"])

    async def get_top_tags(self, artist: str, album: str, *, autocorrect: bool = False, username: str = None) -> list:
        json = await requests.get(self.api, "album.gettoptags", artist=artist, album=album, autocorrect=autocorrect,
                                  username=username)
        return [objects.Tag(tag) for tag in json["toptags"]["tag"]]

    async def search(self, album: str, *, limit: int = 0, page: int = 0) -> objects.Search:
        json = await requests.get(self.api, "album.search", album=album, limit=limit, page=page)
        return objects.Search(json["results"], objects.Album, "albummatches")


class Artist:
    def __init__(self, api):
        self.api = api

    async def get_info(self, artist: str, *, autocorrect: bool = False, username: str = None) -> objects.Artist:
        json = await requests.get(self.api, "artist.getinfo", artist=artist, autocorrect=autocorrect,
                                  username=username)
        return objects.Artist(json["artist"])

    async def get_correction(self, artist: str) -> objects.Artist:
        json = await requests.get(self.api, "artist.getcorrection", artist=artist)
        return objects.Artist(json["artist"])

    async def get_similar(self, artist: str, *, autocorrect: bool = False, limit: int = 0):
        json = await requests.get(self.api, "artist.getsimilar", artist=artist, limit=limit, autocorrect=autocorrect)
        return [objects.Track(track) for track in json["similarartists"]["artist"]]

    async def get_top_albums(self, artist: str, *, autocorrect: bool = False, limit: int = 0, page: int = 0):
        json = await requests.get(self.api, "artist.gettopalbums", artist=artist, limit=limit, page=page,
                                  autocorrect=autocorrect)
        return [objects.Track(track) for track in json["topalbums"]["album"]]

    async def get_top_tags(self, artist: str, *, autocorrect: bool = False):
        json = await requests.get(self.api, "artist.gettoptags", artist=artist, autocorrect=autocorrect)
        return [objects.Tag(track) for track in json["toptags"]["tag"]]

    async def get_top_tracks(self, artist: str, *, autocorrect: bool = False, limit: int = 0, page: int = 0):
        json = await requests.get(self.api, "artist.gettoptracks", artist=artist, limit=limit, page=page,
                                  autocorrect=autocorrect)
        return [objects.Track(track) for track in json["toptracks"]["track"]]

    async def search(self, artist: str, *, limit: int = 0, page: int = 0) -> objects.Search:
        json = await requests.get(self.api, "artist.search", artist=artist, limit=limit, page=page)
        return objects.Search(json["results"], objects.Artist, "artistmatches")
