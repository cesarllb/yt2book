import streamlit as st
from backend import yt_util
from backend.yt_util import YoutubePlaylist
from backend.converter import text2speach #save_as_audiobook
from backend.converter import text2document #create_epub, create_pdf

def process_video(url):
    st.session_state.playlist = YoutubePlaylist(url)

def extract_transcripts(lang_code: str = None):
    if lang_code:
        st.session_state.text_paths: list[str] = st.session_state.playlist.save_all_transcript(lang_code, translate= True)
    elif not lang_code:
        st.session_state.text_paths: list[str] = st.session_state.playlist.save_all_transcript(lang_code, translate= False)
    st.session_state.lang_code = lang_code
    st.session_state.texts, st.session_state.chap_titles = yt_util.get_texts_and_chapters_titles(st.session_state.text_paths) 

def to_document(format: str):
    if format == 'PDF':
        text2document.create_pdf(st.session_state.texts, st.session_state.chap_titles, 
                st.session_state.playlist.channel_name, st.session_state.playlist.name, 
                st.session_state.playlist.list_videos[0].thumbnail_url)
    if format == 'EPUB':
        text2document.create_epub(st.session_state.texts, st.session_state.chap_titles, 
                st.session_state.playlist.channel_name, st.session_state.playlist.name, 
                st.session_state.playlist.list_videos[0].thumbnail_url)

st.title('Process YouTube list')
col1, col2 = st.columns(2)
col2.markdown("<br>"*1, unsafe_allow_html=True)

st.session_state.url = col1.text_input('Insert the YouTube playlist URL here')
if col2.button('Process'):
    process_video(st.session_state.url)
    extract_transcripts(lang_code= format)
    st.session_state.processed = True
    
if 'processed' in st.session_state:
    format = col1.selectbox('Select the language to extract the transcript', ('es', 'en', 'it', 'fr', 'hi', 'zh', 'ru', 'de'))
    if col2.button('Save scripts in an audiobook'):
        text2speach.save_as_audiobook(st.session_state.texts, 
                        st.session_state.playlist.name + ' ' + st.session_state.playlist.channel_name, st.session_state.lang_code)

    format = col1.selectbox('Select the document format', ('PDF', 'EPUB'))
    if col2.button('COnvert playlist to document'):
        to_document(format)
