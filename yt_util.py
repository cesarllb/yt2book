import os
from tqdm import tqdm
from pytube import Playlist, YouTube
from yt2text import Youtube2Text

class YoutubeVideo:
    def __init__(self, url, path_for_caption: str):
        video = YouTube(url)
        # video.check_availability()
        self.path_for_caption = path_for_caption
        self.title = video.title
        self.thumbnail_url = video.thumbnail_url
        self.id = video.video_id
        self.duration = video.length
        
    def save_video_transcript(self, lang: str, translate = True, generated_transcript = False) -> str:
        lang = lang if len(lang) == 2 else lang[:2]
        yt2text = Youtube2Text(self.id)
        transcript = yt2text.get_transcript(lang, generated_transcript)
        if transcript:
            self._save(transcript)
        elif not transcript and translate:
            translated = yt2text.translate_transcript(lang)
            if translated:
                self._save(translated)
        return os.path.join(self.path_for_caption, self.title)

    def _save(self, transcript: list[str]) -> None:
        text = ''; timer: float = 0.0
        os.makedirs(self.path_for_caption, exist_ok=True)
        for t in transcript:
            if t['start'] - timer > 5.0: #basically checks if there is a gap of 5 seconds or more between subtitles and break the line.
                text += t['text'] + ' \n'
            else:
                text += t['text'] + ' '
            timer = t['start']
        with open(os.path.join(self.path_for_caption, self.title), 'w') as f:
            f.write(text)

class YoutubePlaylist:
    def __init__(self, list_url: str) -> None:
        self.url = list_url
        self.playlist = Playlist(url= self.url)
        self.name = self.playlist.title
        self.list_videos = self._get_videos()
        
    def _get_videos(self) -> list[YoutubeVideo]:
        return [ YoutubeVideo(video.watch_url, os.path.join(os.path.curdir, self.name)) for video in self.playlist.videos ]
    
    def save_all_transcript(self, lang: str, translate = True, generated_transcript = False):
        for v in tqdm(self.list_videos):
            v.save_video_transcript(lang, translate, generated_transcript)
        
playlist = YoutubePlaylist('https://youtube.com/playlist?list=PL8dPuuaLjXtNM_Y-bUAhblSAdWRnmBUcr&si=RT9JpUwzMFgEWQYd')
playlist.save_all_transcript('es', translate= True)