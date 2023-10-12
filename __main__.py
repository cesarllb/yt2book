from backend.yt_util import YoutubePlaylist
from backend.converter import text2document #create_epub, create_pdf
from backend.converter import text2speach #save_as_audiobook

def test():
    playlist = YoutubePlaylist('https://youtube.com/playlist?list=PL8dPuuaLjXtNM_Y-bUAhblSAdWRnmBUcr&si=RT9JpUwzMFgEWQYd')
    text_paths: list[str] = playlist.save_all_transcript('es', translate= True)
    texts, chap_titles = [], []
    for path in text_paths:
        chap_titles.append( path.split('/')[-1] )
        with open(path) as f:
            texts.append(f.read())
    text2document.create_pdf(texts, chap_titles, playlist.channel_name, playlist.name, playlist.list_videos[0].thumbnail_url)
    # save_as_audiobook(texts, playlist.name + ' ' + playlist.channel_name, 'es')

if __name__ == '__main__':
    test()