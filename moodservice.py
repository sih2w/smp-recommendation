class MoodService:
    moods = [
        "HAPPY",
        "SAD",
        "CHILL",
        "ENERGETIC",
        "ROMANTIC",
        "ANGRY",
        "PEACEFUL",
        "PARTY",
        "MOTIVATIONAL",
        "NOSTALGIC"
    ]

    @staticmethod
    def get_mood(mood: str) -> str:
        if mood in MoodService.moods:
            return mood
        return MoodService.moods[-1]