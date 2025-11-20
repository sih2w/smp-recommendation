from typing import List
from services.historyservice import History
from services.randomservice import WeightedKeys, RandomService


class RecommendationService:
    @staticmethod
    def get_song_chance(history: History, mood: str, song_id: str):
        chance = 0.50

        if song_id in history[mood]["Disliked"]:
            chance = 0.10
        else:
            if song_id in history[mood]["Previous"]:
                chance -= 0.20

            if song_id in history[mood]["Liked"]:
                chance += 0.10

            if song_id in history[mood]["Favorite"]:
                chance += 0.20

            if song_id in history[mood]["Skipped"] and song_id in history[mood]["Finished"]:
                finished_count = history[mood]["Finished"][song_id]
                skipped_count = history[mood]["Skipped"][song_id]
                percent_finished = finished_count / (finished_count + skipped_count)
                chance += (0.10 * percent_finished)

        chance = max(0.00, min(chance, 1.00))

        return chance

    @staticmethod
    def get_song_chances(history: History, mood: str, song_ids: List[str]):
        song_chances: WeightedKeys = {
            "Keys": [],
            "Chances": [],
        }

        for song_id in song_ids:
            chance = RecommendationService.get_song_chance(history, mood, song_id)
            song_chances["Keys"].append(song_id)
            song_chances["Chances"].append(chance)
        song_chances["Chances"] = RandomService.normalize(song_chances["Chances"])

        return song_chances