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

from . import objects
from . import request


class LastFMClient:
    """Main class that contains features for all the endpoints of the last.fm API that do not require authentication"""

    def __init__(self, api: str):
        self.api = api
        self.album = self.albums = Album(api)
        self.artist = self.artists = Artist(api)
        self.chart = self.charts = Chart(api)
        self.track = self.tracks = Track(api)
        self.user = self.users = User(api)


async def LastFM(api: str) -> LastFMClient:
    """Class factory for LastFMClient objects
    TODO: Implement an API key check as a method of the client class and invoke it in this function"""
    return LastFMClient(api)


class Album:
    """The features of the API in the album method"""

    def __init__(self, api):
        self.api = api

    async def get_info(self, artist: str = None, album: str = None, mbid: str = None, *, autocorrect: bool = False,
                       username: str = None) -> objects.Album:
        """
        Gets relevant information of an album from an artist and album name
        :param artist: Artist name
        :param album: Album name
        :param mbid:
        :param autocorrect: Whether the request should autocorrect errors in name
        :param username: The username to fetch relevant information about the album for (amount of plays, etc)
        :return: lastfmpy.Album
        """
        json = await request.get(self.api, "album.getinfo", artist=artist, album=album, mbid=mbid,
                                 autocorrect=autocorrect,
                                 username=username)
        return objects.Album(json["album"])

    async def get_top_tags(self, artist: str, album: str, *, autocorrect: bool = False, username: str = None) -> list:
        """
        Get top overall tags of an album from an artist and album name
        :param artist: Artist name
        :param album: Album name
        :param autocorrect: Whether the request should autocorrect errors in name
        :param username: The username to fetch relevant information about the album for (amount of plays, etc)
        :return: list of lastfmpy.Tag
        """
        json = await request.get(self.api, "album.gettoptags", artist=artist, album=album, autocorrect=autocorrect,
                                 username=username)
        return [objects.Tag(tag) for tag in json["toptags"]["tag"]]

    async def search(self, album: str, *, limit: int = 0, page: int = 0) -> objects.SearchPage:
        """
        Searches for an album based on a string
        :param album: Album to search for
        :param limit: Amount of search results to retrieve
        :param page: Page of search results
        :return: lastfmpy.SearchPage
        """
        json = await request.get(self.api, "album.search", album=album, limit=limit, page=page)
        return objects.SearchPage(json["results"], objects.Album, "albummatches")


class Artist:
    def __init__(self, api):
        """
        Wrapper on the artist endpoint of the last.fm API
        :param api:
        """
        self.api = api

    async def get_info(self, artist: str, *, autocorrect: bool = False, username: str = None) -> objects.Artist:
        """
        Gets relevant information of an artist from an artist name
        :param artist: Artist name
        :param autocorrect: Whether to autocorrect the artist name
        :param username: The username to fetch relevant information about the album for (amount of plays, etc)
        :return: lastfmpy.Artist
        """
        json = await request.get(self.api, "artist.getinfo", artist=artist, autocorrect=autocorrect,
                                 username=username)
        return objects.Artist(json["artist"])

    async def get_correction(self, artist: str) -> objects.Artist:
        """
        Gets the correction of an artist name
        :param artist: Artist name
        :return: objects.Artist
        """
        json = await request.get(self.api, "artist.getcorrection", artist=artist)
        return objects.Artist(json["artist"])

    async def get_similar(self, artist: str, *, autocorrect: bool = False, limit: int = 0) -> list:
        """
        Gets similar artists
        :param artist: Artist name
        :param autocorrect: Whether to autocorrect the artist name
        :param limit: Amount of similar artists to get
        :return: list of objects.Artist
        """
        json = await request.get(self.api, "artist.getsimilar", artist=artist, limit=limit, autocorrect=autocorrect)
        return [objects.Artist(artist) for artist in json["similarartists"]["artist"]]

    async def get_top_albums(self, artist: str, *, autocorrect: bool = False, limit: int = 0,
                             page: int = 0) -> objects.ObjectPage:
        """
        Gets the artist's top albums
        :param artist: Artist name
        :param autocorrect: Whether to autocorrect the artist name
        :param limit: Amount of albums to get
        :param page: Page of the search
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "artist.gettopalbums", artist=artist, limit=limit, page=page,
                                 autocorrect=autocorrect)
        return objects.ObjectPage(json["topalbums"], objects.Album, "album")

    async def get_top_tags(self, artist: str, *, autocorrect: bool = False) -> objects.ObjectPage:
        """
        Gets the artist's top tags
        :param artist: Artist name
        :param autocorrect: Whether to autocorrect the artist name
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "artist.gettoptags", artist=artist, autocorrect=autocorrect)
        return objects.ObjectPage(json["toptags"], objects.Tag, "tag")

    async def get_top_tracks(self, artist: str, *, autocorrect: bool = False, limit: int = 0,
                             page: int = 0) -> objects.ObjectPage:
        """
        Gets the artist's top tracks
        :param artist: Artist name
        :param autocorrect: Whether to autocorrect the artist name
        :param limit: Amount of tracks to get
        :param page: Page of the search
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "artist.gettoptracks", artist=artist, limit=limit, page=page,
                                 autocorrect=autocorrect)
        return objects.ObjectPage(json["toptracks"], objects.Track, "track")

    async def search(self, artist: str, *, limit: int = 0, page: int = 0) -> objects.SearchPage:
        """
        Searches for an artist based off a string
        :param artist: Artist name
        :param limit: Amount of artists to get
        :param page:
        :return: objects.SearchPage
        """
        json = await request.get(self.api, "artist.search", artist=artist, limit=limit, page=page)
        return objects.SearchPage(json["results"], objects.Artist, "artist")


class Chart:
    def __init__(self, api):
        self.api = api

    async def get_top_artists(self, *, page: int = 0, limit: int = 0):
        """
        Gets the overall top artists
        :param page: Page of the chart
        :param limit: Amount of artists to get
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "chart.gettopartists", limit=limit, page=page)
        return objects.ObjectPage(json["artists"], objects.Artist, "artist")

    async def get_top_tags(self, *, page: int = 0, limit: int = 0):
        """
        Gets the overall top tags
        :param page: Page of the chart
        :param limit: Amount of tags to get
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "chart.gettoptags", limit=limit, page=page)
        return objects.ObjectPage(json["tags"], objects.Tag, "tag")

    async def get_top_tracks(self, *, page: int = 0, limit: int = 0):
        """
        Gets the overall top tracks
        :param page: Page of the chart
        :param limit: Amount of tracks to get
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "chart.gettoptracks", limit=limit, page=page)
        return objects.ObjectPage(json["tracks"], objects.Track, "track")


class Track:
    def __init__(self, api):
        self.api = api

    async def get_info(self, track: str, artist: str, *, autocorrect: bool = False,
                       username: str = None) -> objects.Track:
        """
        Gets relevant information about a track from a track name
        :param track: Track name
        :param artist: Artist name
        :param autocorrect: Whether the request should autocorrect errors in name
        :param username: The username to fetch relevant information about the album for (amount of plays, etc)
        :return: objects.Track
        """
        json = await request.get(self.api, "track.getinfo", track=track, artist=artist, autocorrect=autocorrect,
                                 username=username)
        return objects.Track(json["track"])

    async def get_correction(self, track: str, artist: str) -> objects.Track:
        """
        Gets the correction of an artist name
        :param track: Track name
        :param artist: Artist name
        :return: objects.Track
        """
        json = await request.get(self.api, "track.getcorrection", track=track, artist=artist)
        return objects.Track(json["track"])

    async def get_similar(self, track: str, artist: str, *, autocorrect: bool = False, limit: int = 0) -> list:
        """
        Gets similar tracks from a track name
        :param track: Track name
        :param artist: Artist name
        :param autocorrect: Whether the request should autocorrect errors in name
        :param limit: The amount of similar tracks to get
        :return: list of objects.Track
        """
        json = await request.get(self.api, "track.getsimilar", track=track, artist=artist, limit=limit,
                                 autocorrect=autocorrect)
        return [objects.Track(track) for track in json["similartracks"]["track"]]

    async def get_top_tags(self, track: str, artist: str, *, autocorrect: bool = False) -> list:
        """
        Gets top tags of a track
        :param track: Track name
        :param artist: Artist name
        :param autocorrect: Whether the request should autocorrect errors in name
        :return: list of objects.Tag
        """
        json = await request.get(self.api, "track.gettoptags", track=track, autocorrect=autocorrect)
        return [objects.Tag(tag) for tag in json["toptags"]["tag"]]

    async def search(self, track: str, *, limit: int = 0, page: int = 0) -> objects.SearchPage:
        """
        Searches for a track based on a string
        :param track: Track to search for
        :param limit: Amount of tracks to get
        :param page: Page of the search
        :return: objects.SearchPage
        """
        json = await request.get(self.api, "track.search", track=track, limit=limit, page=page)
        return objects.SearchPage(json["results"], objects.Track, "track")


class User:
    def __init__(self, api):
        self.api = api

    async def get_info(self, user: str) -> objects.User:
        """
        Gets relevant information about a user based on a username
        :param user: Username of a user
        :return: objects.User
        """
        json = await request.get(self.api, "user.getinfo", user=user)
        return objects.User(json["user"])

    async def get_friends(self, user: str, *, recenttracks: bool = False, limit: int = 0,
                          page: int = 0) -> objects.ObjectPage:
        """
        Gets friends of a user
        :param user: Username of a user
        :param recenttracks: Whether to get the recent tracks of the user's friends
        :param limit: The amount of friends to get
        :param page: The page of friends
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "user.getfriends", user=user, recenttracks=recenttracks, limit=limit,
                                 page=page)
        return objects.ObjectPage(json["friends"], objects.User, "user")

    async def get_loved_tracks(self, user: str, *, limit: int = 0, page: int = 0) -> objects.ObjectPage:
        """
        Gets the loved tracks of a user
        :param user: Username of a user
        :param limit: The amount of loved tracks to get
        :param page: The page of loved tracks
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "user.getlovedtracks", user=user, limit=limit, page=page)
        return objects.ObjectPage(json["lovedtracks"], objects.Track, "track")

    async def get_recent_tracks(self, user: str, *, limit: int = 0, page: int = 0, from_: int = 0,
                                extended: bool = False, to: int = 0) -> objects.ObjectPage:
        """
        Get recent tracks of a user
        :param user: Username of a user
        :param limit: Amount of recent tracks to get
        :param page: Page of recent tracks to get
        :param from_: UNIX timestamp of beginning of timespan
        :param extended: Whether to get extended track information
        :param to: UNIX timestamp of end of timespan
        :return: objects.ObjectPage
        """
        json = await request.get(self.api, "user.getrecenttracks", user=user, limit=limit, page=page, from_=from_,
                                 extended=extended, to=to)
        return objects.ObjectPage(json["recenttracks"], objects.Track, "track")

    async def get_top_albums(self, user: str, *, period: str = None, limit: int = 0, page: int = 0):
        json = await request.get(self.api, "user.gettopalbums", user=user, limit=limit, page=page, period=period)
        return objects.ObjectPage(json["topalbums"], objects.Album, "album")

    async def get_top_artists(self, user: str, *, period: str = None, limit: int = 0, page: int = 0):
        json = await request.get(self.api, "user.gettopartists", user=user, limit=limit, page=page, period=period)
        return objects.ObjectPage(json["topartists"], objects.Artist, "artist")

    async def get_top_tags(self, user: str, *, limit: int = 0):
        json = await request.get(self.api, "user.gettoptags", user=user, limit=limit)
        return objects.ObjectPage(json["toptags"], objects.Tag, "tag")

    async def get_top_tracks(self, user: str, *, period: str = None, limit: int = 0, page: int = 0):
        json = await request.get(self.api, "user.gettoptracks", user=user, limit=limit, page=page, period=period)
        return objects.ObjectPage(json["toptracks"], objects.Track, "track")

    async def get_weekly_album_chart(self, user: str, *, from_: str = None, to: str = None):
        json = await request.get(self.api, "user.getweeklyalbumchart", user=user, from_=from_, to=to)
        return objects.ObjectPage(json["weeklyalbumchart"], objects.Album, "album")

    async def get_weekly_artist_chart(self, user: str, *, from_: str = None, to: str = None):
        json = await request.get(self.api, "user.getweeklyartistchart", user=user, from_=from_, to=to)
        return objects.ObjectPage(json["weeklyartistchart"], objects.Artist, "artist")

    async def get_weekly_track_chart(self, user: str, *, from_: str = None, to: str = None):
        json = await request.get(self.api, "user.getweeklytrackchart", user=user, from_=from_, to=to)
        return objects.ObjectPage(json["weeklytrackchart"], objects.Track, "track")
