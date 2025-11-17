from typing import List
from scripts.recommend import Song
import pandas as pd


class PlaylistFunctions:
    @staticmethod
    def Generate(mood: str = "Happy"):
        df = pd.read_csv(filepath_or_buffer="../data/songs/songs.csv", delimiter="\t")
        result = df[df["Mood"] == mood]
        songs: List[Song] = []

        for row in result.iterrows():
            songs.append({
                "Mood": mood,
                "Title": row[1]["Title"],
                "Artist": row[1]["Artist"].split(","),
            })

        return songs