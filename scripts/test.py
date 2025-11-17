from typing import List
from scripts.choices import ChoiceFunctions, WeightedKeys
from scripts.history import HistoryFunctions, History
from scripts.playlist import PlaylistFunctions
from scripts.recommend import RecommendationFunctions
from scripts.song import Song, SongFunctions
from scripts.user import UserFunctions
from numpy.random import Generator, PCG64


class TestFunctions:
    @staticmethod
    def OutputHistory(history: History):
        print("")
        for key, value in history.items():
            print(f"{key}: {value}")
        print("")

    @staticmethod
    def OutputCurrentSongChances(song_chances: WeightedKeys):
        print("")
        for index in range(len(song_chances["Keys"])):
            key = song_chances["Keys"][index]
            chance = song_chances["Chances"][index]
            print(f"{SongFunctions.GetSongId(key)}: {f"%.2f" % chance}")
        print("")

    @staticmethod
    def Step(history: History, songs: List[Song], generator: Generator):
        song_chances = RecommendationFunctions.GetSongChances(history, songs)
        action_chances = UserFunctions.GetActionChances()

        song = ChoiceFunctions.GetKey(song_chances, generator)
        action = ChoiceFunctions.GetKey(action_chances, generator)
        song_id = SongFunctions.GetSongId(song)

        HistoryFunctions.UpdatePrevious(history, song)

        if action == "Skip":
            HistoryFunctions.Increment(history, "Skipped", song)
        else:
            HistoryFunctions.Increment(history, "Finished", song)

            if action == "Like":
                history["Liked"][song_id] = True
                history["Disliked"][song_id] = False
            elif action == "Dislike":
                history["Liked"][song_id] = False
                history["Disliked"][song_id] = True
            elif action == "Favorite":
                history["Favorite"][song_id] = True

        return song_id

if __name__ == "__main__":
    user_id = "test"
    history = HistoryFunctions.Load(user_id)
    songs = PlaylistFunctions.Generate("Happy")
    generator = Generator(PCG64(0))

    for episode in range(3):
        song_id = TestFunctions.Step(history, songs, generator)
        TestFunctions.OutputHistory(history)
        TestFunctions.OutputCurrentSongChances(
            RecommendationFunctions.GetSongChances(history, songs)
        )

        print("Playing song: " + song_id)

    HistoryFunctions.Save(user_id, history)
