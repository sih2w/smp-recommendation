from quart import Quart, jsonify, request
from moodservice import MoodService
from randomservice import RandomService
from historyservice import HistoryService, History
from spotifyservice import SpotifyService
from recommendationservice import RecommendationService
from numpy.random import Generator, PCG64


app = Quart(__name__)


def add_to_previously_played(history: History, mood: str, song_id: str):
    history[mood]["Previous"].insert(0, song_id)
    if len(history[mood]["Previous"]) > 3:
        history[mood]["Previous"].pop()


@app.route("/skip-song", methods=["GET"])
def skip_song():
    try:
        user_id = request.args.get("UserId")
        song_id = request.args.get("SongId")
        mood = MoodService.get_mood(request.args.get("Mood"))

        history: History = HistoryService.get_history(user_id)
        if not song_id in history[mood]["Skipped"]:
            history[mood]["Skipped"][song_id] = 0
        history[mood]["Skipped"][song_id] += 1

        add_to_previously_played(history, mood, song_id)

        return jsonify({
            "Success": True,
        })
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e),
        })


@app.route("/finish-song", methods=["GET"])
def finish_song():
    try:
        user_id = request.args.get("UserId")
        song_id = request.args.get("SongId")
        mood = MoodService.get_mood(request.args.get("Mood"))

        history: History = HistoryService.get_history(user_id)
        if not song_id in history[mood]["Finished"]:
            history[mood]["Finished"][song_id] = 0
        history[mood]["Finished"][song_id] += 1

        add_to_previously_played(history, mood, song_id)

        return jsonify({
            "Success": True,
        })
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e),
        })


@app.route("/like", methods=["GET"])
def like_song():
    try:
        user_id = request.args.get("UserId")
        song_id = request.args.get("SongId")
        mood = MoodService.get_mood(request.args.get("Mood"))
        like = request.args.get("Like", default=True)

        history: History = HistoryService.get_history(user_id)
        history[mood]["Liked"][song_id] = like
        return jsonify({
            "Success": True,
        })
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e),
        })


@app.route("/dislike", methods=["GET"])
def dislike_song():
    try:
        user_id = request.args.get("UserId")
        song_id = request.args.get("SongId")
        mood = MoodService.get_mood(request.args.get("Mood"))
        disliked = request.args.get("Dislike", default=True)

        history: History = HistoryService.get_history(user_id)
        history[mood]["Disliked"][song_id] = disliked
        return jsonify({
            "Success": True,
        })
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e),
        })


@app.route("/favorite", methods=["GET"])
async def favorite_song():
    try:
        user_id = request.args.get("UserId")
        song_id = request.args.get("SongId")
        mood = MoodService.get_mood(request.args.get("Mood"))
        favorite = request.args.get("Favorite", default=True)

        history: History = HistoryService.get_history(user_id)
        history[mood]["Favorite"][song_id] = favorite
        return jsonify({
            "Success": True,
        })
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e),
        })


@app.route("/get-playlist", methods=["GET"])
async def get_playlist():
    try:
        mood = MoodService.get_mood(request.args.get("Mood"))
        limit = int(request.args.get("Limit", default=0))

        playlist, message = await SpotifyService.get_playlist(mood, limit)

        if message == "":
            return jsonify({
                "Success": True,
                "Playlist": playlist,
            })
        else:
            raise Exception(message)
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e),
        })


@app.route("/next-song", methods=["GET"])
def next_song():
    try:
        user_id = request.args.get("UserId")
        mood = MoodService.get_mood(request.args.get("Mood"))
        song_ids = request.args.get("SongsIds", [])
        history: History = HistoryService.get_history(user_id)

        song_chances = RecommendationService.get_song_chances(history, mood, song_ids)
        song_id = RandomService.get_key(song_chances, Generator(PCG64()))

        return jsonify({
            "SongId": song_id,
            "Success": True,
        })
    except Exception as e:
        return jsonify({
            "Success": False,
            "Error": str(e),
        })


@app.route("/", methods=["GET"])
async def index():
    return jsonify({
        "Success": True,
    })


@app.teardown_appcontext
def cleanup(exception=None):
    for user_id, history in HistoryService.cache.items():
        HistoryService.save(user_id, history)
        print(f"Saved {user_id}'s history.")


if __name__ == "__main__":
    app.run()