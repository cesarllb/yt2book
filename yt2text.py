from enum import Enum
from youtube_transcript_api import NoTranscriptFound
from youtube_transcript_api import YouTubeTranscriptApi

class Language(Enum):
        MANDARIN = 'zh'
        SPANISH = 'es'
        ENGLISH = 'en'
        HINDI = 'hi'
        BENGALI = 'bn'
        PORTUGUESE = 'pt'
        RUSSIAN = 'ru'
        JAPANESE = 'ja'
        ITALIAN = 'it'
        GERMAN = 'de'
        
class Youtube2Text:
    
    def __init__(self, video_id) -> None:
        self.id = video_id
        self.transcript_list = YouTubeTranscriptApi.list_transcripts(self.id)

    def get_transcript(self, lang: Language, generated_transcript = False) -> dict:
        if not lang in Language:
            raise ValueError(f'Unsupported language: {lang}')
        try:
            transcript = self.transcript_list.find_manually_created_transcript([lang])
            return transcript.fetch()
        except NoTranscriptFound:
            if not generated_transcript:
                return None
            elif generated_transcript:
                try:
                    return self.transcript_list.find_generated_transcript([lang]).fetch()
                except NoTranscriptFound:
                    return None
    
    def translate_transcript(self, target_lang: str) -> dict:
        try:
            english_transcript = self.transcript_list.find_manually_created_transcript(['en'])
            return english_transcript.translate(target_lang).fetch()
        except NoTranscriptFound:
            return None