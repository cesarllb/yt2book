from pytube import Playlist, YouTube, Channel

def get_video_ids_from_list(playlist_url) -> list[str]:
    playlist = Playlist(playlist_url)
    return [video.video_id for video in playlist.videos]


def get_num_list_videos(playlist_url):
    playlist = Playlist(playlist_url)
    return len(playlist.videos)

def get_thumbnail_from_id(video_id):
    video = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    return video.thumbnail_url

def get_thumbail_list_from_ids(ids: list) -> list[str]:
    return [get_thumbnail_from_id(id) for id in ids]
    
def get_video_id(video_url):
    yt = YouTube(video_url)
    return yt.video_id

def get_video_ids_from_channel(channel_url):
    channel = Channel(channel_url)
    return [video.video_id for video in channel.videos]
    
def get_num_channel_videos(channel_url):
    channel = Channel(channel_url)
    return len(channel.videos)