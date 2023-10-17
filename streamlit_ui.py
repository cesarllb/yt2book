import streamlit as st
from backend import yt_util
from backend.converter import text2speach #save_as_audiobook
from ui_core import process_video, extract_transcripts, to_document, to_audiobook

st.title('Process YouTube list')
col1, col2 = st.columns(2)
col2.markdown("<br>"*1, unsafe_allow_html=True)

st.session_state.url = col1.text_input('Insert the YouTube playlist URL here')
lang = col1.selectbox('Select the language to extract the transcript', ('es', 'en', 'it', 'fr', 'hi', 'zh', 'ru', 'de'))
if col2.button('Process'):
    st.session_state.playlist = process_video(st.session_state.url)
    st.session_state.texts, st.session_state.chap_titles = \
                    extract_transcripts(st.session_state.playlist, lang_code= lang)
    st.session_state.processed = True
    
if 'processed' in st.session_state:
    if col2.button('Save scripts in an audiobook'):
        to_audiobook(st.session_state.texts, 
                    st.session_state.playlist.name + ' ' + st.session_state.playlist.channel_name, 
                    lang)
    format = col1.selectbox('Select the document format', ('PDF', 'EPUB'))
    if col2.button('Convert playlist to document'):
        to_document(st.session_state.texts, st.session_state.chap_titles, 
                st.session_state.playlist.channel_name, st.session_state.playlist.name, 
                st.session_state.playlist.list_videos[0].thumbnail_url, format)
