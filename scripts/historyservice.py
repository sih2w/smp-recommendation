import json
from typing import TypedDict, Dict, List, TypeAlias
from scripts.moodservice import MoodService


class MoodHistory(TypedDict):
    Liked: Dict[str, bool]
    Disliked: Dict[str, bool]
    Favorite: Dict[str, bool]
    Skipped: Dict[str, int]
    Finished: Dict[str, int]
    Previous: List[str]


History: TypeAlias = Dict[str, MoodHistory]


class HistoryService:
    cache: Dict[str, History] = {}

    @staticmethod
    def get_history(user_id: str) -> History:
        if user_id not in HistoryService.cache:
            HistoryService.cache[user_id] = HistoryService.load(user_id)
        history = HistoryService.cache[user_id]
        return history

    @staticmethod
    def get_user_file_path(user_id):
        return f"../data/users/{user_id}.json"

    @staticmethod
    def reset(user_id):
        history = HistoryService.create()
        HistoryService.save(user_id, history)
        return history

    @staticmethod
    def load(user_id: str) -> History:
        try:
            with open(HistoryService.get_user_file_path(user_id), "r") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return HistoryService.create()

    @staticmethod
    def save(user_id: str, history: History) -> None:
        with open(HistoryService.get_user_file_path(user_id), "w") as f:
            f.write(json.dumps(history))

    @staticmethod
    def create():
        return {
            mood: {
                "Liked": {},
                "Disliked": {},
                "Favorite": {},
                "Skipped": {},
                "Finished": {},
                "Previous": [],
            } for mood in MoodService.moods
        }