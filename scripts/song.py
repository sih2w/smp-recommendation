from typing import List, TypedDict


class Song(TypedDict):
    Mood: str
    Title: str
    Artist: List[str]


class SongFunctions:
    @staticmethod
    def GetSongId(song: Song):
        return str.replace(song["Title"] + " " + song["Artist"][0], " ", "_")