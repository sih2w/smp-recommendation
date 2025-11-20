class MoodService:
    mapping = {
        "happy": "HAPPY UPBEAT POP",
        "sad": "SAD EMOTIONAL HEARTACHE",
        "chill": "LOFI CHILL RELAXING",
        "energetic": "ENERGETIC WORKOUT POP",
        "romantic": "ROMANTIC LOVE HEART",
        "angry": "ANGER METAL ROCK SHOUTING",
        "peaceful": "PEACE RELAX CALM",
        "party": "PARTY DANCE EDM",
        "motivational": "INSPIRE CINEMATIC MOTIVATIONAL",
        "nostalgic": "NOSTALGIC THROWBACK RETRO"
    }

    @staticmethod
    def get_moods():
        return list(MoodService.mapping.keys())

    @staticmethod
    def get_keywords(mood: str):
        return MoodService.mapping.get(mood, MoodService.mapping["happy"])

    @staticmethod
    def get_mood(mood: str) -> str:
        if mood in MoodService.mapping:
            return mood
        return MoodService.get_moods()[0]