import os
import asyncio
from tqdm import tqdm
from pytube import Playlist, YouTube, Channel
from yt2text import Youtube2Text

class YoutubeVideo:
    def __init__(self, url, path_for_caption: str, channel_name: str):
        self.channel_name = channel_name
        self.path_for_caption = path_for_caption
        self.video = YouTube(url)
        self.title = self.video.title
        self.transcript_path = os.path.join(self.path_for_caption + ' ' + self.channel_name , self.title)
        self.thumbnail_url = self.video.thumbnail_url
        self.id = self.video.video_id
        self.duration = self.video.length
        
    def save_video_transcript(self, lang: str, translate = True, generated_transcript = False) -> str:
        if not os.path.isfile(self.transcript_path):
            if lang:
                lang = lang if len(lang) == 2 else lang[:2]
            yt2text = Youtube2Text(self.id)
            transcript = yt2text.get_transcript(lang, generated_transcript)
            if transcript:
                self._save(transcript)
            elif not transcript and translate and lang:
                translated = yt2text.translate_transcript(lang)
                if translated:
                    self._save(translated)
        return self.transcript_path

    def _save(self, transcript: dict) -> None:
        text = ''; timer: float = 0.0
        os.makedirs( self.path_for_caption + ' ' + self.channel_name , exist_ok=True)
        for t in transcript:
            text += t['text'] + ' \n' if t['start'] - timer > 10.0 else t['text'] + ' ' #basically checks if there is a gap of 5 seconds or more between subtitles and break the line.
            timer = t['start']
        with open(self.transcript_path, 'w') as f:
            f.write(text)

class YoutubePlaylist:
    def __init__(self, playlist_url: str) -> None:
        self.url = playlist_url
        
        self.playlist = Playlist(url= self.url)
        self.channel_name = Channel(self.playlist.videos[0].channel_url).channel_name
        
        self.name = self.playlist.title
        self.list_videos = self._get_videos()
        self.cover_paths = [video.thumbnail_url for video in self.list_videos]
        
    def _get_videos(self) -> list[YoutubeVideo]:
        path_for_caption = os.path.join(os.path.curdir, self.name)
        return [YoutubeVideo(video.watch_url, path_for_caption, self.channel_name) for video in self.playlist.videos ]
    
    def save_all_transcript(self, lang: str, translate = True, generated_transcript = False) -> list[str]:
        self.list_paths = []
        for v in tqdm(self.list_videos):
            self.list_paths.append(v.save_video_transcript(lang, translate, generated_transcript))
        return self.list_paths