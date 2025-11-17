import json
from scripts.song import Song, SongFunctions
from typing import TypedDict, Dict, List, Literal


class History(TypedDict):
    Liked: Dict[str, bool]
    Disliked: Dict[str, bool]
    Favorite: Dict[str, bool]
    Skipped: Dict[str, int]
    Finished: Dict[str, int]
    Previous: List[str]


class HistoryFunctions:
    @staticmethod
    def GetUserFilePath(user_id):
        return f"../data/users/{user_id}.json"

    @staticmethod
    def Reset(user_id):
        history = HistoryFunctions.Create()
        HistoryFunctions.Save(user_id, history)
        return history

    @staticmethod
    def Load(user_id: str) -> History:
        try:
            with open(HistoryFunctions.GetUserFilePath(user_id), "r") as f:
                return json.loads(f.read())
        except FileNotFoundError as e:
            return HistoryFunctions.Create()

    @staticmethod
    def Save(user_id: str, history: History) -> None:
        with open(HistoryFunctions.GetUserFilePath(user_id), "w") as f:
            f.write(json.dumps(history))

    @staticmethod
    def UpdatePrevious(history: History, song: Song):
        history["Previous"].insert(0, SongFunctions.GetSongId(song))
        if len(history["Previous"]) > 3:
            history["Previous"].pop()

    @staticmethod
    def Increment(history: History, category: Literal["Skipped", "Finished"], song: Song):
        song_id = SongFunctions.GetSongId(song)
        if not song_id in history[category]:
            history[category][song_id] = 0
        history[category][song_id] += 1

    @staticmethod
    def Create():
        return {
            "Liked": {},
            "Disliked": {},
            "Favorite": {},
            "Skipped": {},
            "Finished": {},
            "Previous": [],
        }

if __name__ == "__main__":
    history = HistoryFunctions.Load("test")
    print(history)
    HistoryFunctions.Save("test", history)