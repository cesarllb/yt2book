from backend import yt_util
from backend.yt_util import YoutubePlaylist
from backend.converter import text2document #create_epub, create_pdf
from backend.converter import text2speach #save_as_audiobook


def process_video(url) -> YoutubePlaylist:
    return YoutubePlaylist(url)

def extract_transcripts(playlist: yt_util.YoutubePlaylist, lang_code: str = None) -> tuple[list, list]:
    if lang_code:
        text_paths: list[str] = playlist.save_all_transcript(lang_code, translate= True)
    elif not lang_code:
        text_paths: list[str] = playlist.save_all_transcript(lang_code, translate= False)
    return yt_util.get_texts_and_chapters_titles(text_paths) 

def to_document(texts: list[str], chapters_name: list[str], 
                author: str, title: str, cover_url: str, format: str):
    if format == 'PDF':
        text2document.create_pdf(texts, chapters_name, 
                author, title, cover_url)
    if format == 'EPUB':
        text2document.create_epub(texts, chapters_name, 
                author, title, cover_url)
def to_audiobook(texts: list[str], title: str, lang_code: str):
    text2speach.save_as_audiobook(texts, title, lang_code)