from typing import List
from scripts.history import History
from scripts.choices import WeightedKeys, ChoiceFunctions
from scripts.song import Song, SongFunctions


class RecommendationFunctions:
    @staticmethod
    def GetSongChance(history: History, song: Song):
        chance = 0.50
        song_id = SongFunctions.GetSongId(song)

        if song_id in history["Disliked"]:
            chance = 0.10
        else:
            if song_id in history["Previous"]:
                chance -= 0.20

            if song_id in history["Liked"]:
                chance += 0.10

            if song_id in history["Favorite"]:
                chance += 0.20

            if song_id in history["Skipped"] and song_id in history["Finished"]:
                finished_count = history["Finished"][song_id]
                skipped_count = history["Skipped"][song_id]
                percent_finished = finished_count / (finished_count + skipped_count)
                chance += (0.10 * percent_finished)

        chance = max(0.00, min(chance, 1.00))

        return chance

    @staticmethod
    def GetSongChances(history: History, songs: List[Song]):
        song_chances: WeightedKeys = {
            "Keys": [],
            "Chances": [],
        }

        for song in songs:
            chance = RecommendationFunctions.GetSongChance(history, song)
            song_chances["Keys"].append(song)
            song_chances["Chances"].append(chance)
        song_chances["Chances"] = ChoiceFunctions.Normalize(song_chances["Chances"])

        return song_chances