from typing import TypedDict, Dict, List, TypeAlias
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from services.moodservice import MoodService
from os import getenv


class MoodHistory(TypedDict):
    Liked: Dict[str, bool]
    Disliked: Dict[str, bool]
    Favorite: Dict[str, bool]
    Skipped: Dict[str, int]
    Finished: Dict[str, int]
    Previous: List[str]


History: TypeAlias = Dict[str, MoodHistory]


class HistoryService:
    client: AsyncIOMotorClient = AsyncIOMotorClient(getenv("CONNECTION_STRING"))
    db: AsyncIOMotorDatabase = client["songhistory"]
    collection = db["users"]
    
    @staticmethod
    async def get_history(user_id: str) -> History:
        user_data = await HistoryService.collection.find_one({"user_id": user_id})
        if user_data:
            return user_data["history"]
        else:
            history = HistoryService.create()
            await HistoryService.save(user_id, history)
            return history

    @staticmethod
    async def reset(user_id: str):
        history = HistoryService.create()
        await HistoryService.save(user_id, history)
        return history

    @staticmethod
    async def load(user_id: str) -> History:
        user_data = await HistoryService.collection.find_one({"user_id": user_id})
        if user_data:
            return user_data["history"]
        return HistoryService.create()

    @staticmethod
    async def save(user_id: str, history: History) -> None:
        await HistoryService.collection.update_one(
            {"user_id": user_id},
            {"$set": {"history": history}},
            upsert=True
        )

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
            } for mood in MoodService.get_moods()
        }

    @staticmethod
    def add_to_previously_played(history: History, mood: str, song_id: str):
        history[mood]["Previous"].insert(0, song_id)
        if len(history[mood]["Previous"]) > 3:
            history[mood]["Previous"].pop()

    @staticmethod
    async def skip_song(user_id: str, song_id: str, mood: str):
        history: History = await HistoryService.get_history(user_id)
        if song_id not in history[mood]["Skipped"]:
            history[mood]["Skipped"][song_id] = 0
        history[mood]["Skipped"][song_id] += 1
        HistoryService.add_to_previously_played(history, mood, song_id)
        await HistoryService.save(user_id, history)

    @staticmethod
    async def finish_song(user_id: str, song_id: str, mood: str):
        history: History = await HistoryService.get_history(user_id)
        if song_id not in history[mood]["Finished"]:
            history[mood]["Finished"][song_id] = 0
        history[mood]["Finished"][song_id] += 1
        HistoryService.add_to_previously_played(history, mood, song_id)
        await HistoryService.save(user_id, history)

    @staticmethod
    async def like_song(user_id: str, song_id: str, mood: str, like: bool):
        history: History = await HistoryService.get_history(user_id)
        history[mood]["Liked"][song_id] = like
        await HistoryService.save(user_id, history)

    @staticmethod
    async def dislike_song(user_id: str, song_id: str, mood: str, dislike: bool):
        history: History = await HistoryService.get_history(user_id)
        history[mood]["Disliked"][song_id] = dislike
        await HistoryService.save(user_id, history)

    @staticmethod
    async def favorite_song(user_id: str, song_id: str, mood: str, favorite: bool):
        history: History = await HistoryService.get_history(user_id)
        history[mood]["Favorite"][song_id] = favorite
        await HistoryService.save(user_id, history)
