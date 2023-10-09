import streamlit as st
from yt_util import YoutubePlaylist
from text2document import create_epub, create_pdf
from text2speach import save_as_audiobook

def process_video(url):
    st.session_state.playlist = YoutubePlaylist(url)

def extraer_scripts(lang_code: str = None):
    if lang_code:
        st.session_state.text_paths: list[str] = st.session_state.playlist.save_all_transcript(lang_code, translate= True)
    elif not lang_code:
        st.session_state.text_paths: list[str] = st.session_state.playlist.save_all_transcript(lang_code, translate= False)
    st.session_state.lang_code = lang_code
    
    texts, chap_titles = [], []
    for path in st.session_state.text_paths:
        chap_titles.append( path.split('/')[-1] )
        with open(path) as f:
            texts.append(f.read())
    st.session_state.texts = texts
    st.session_state.chap_titles = chap_titles

def to_audiobook():
    save_as_audiobook(st.session_state.texts, 
                    st.session_state.playlist.name + ' ' + st.session_state.playlist.channel_name, st.session_state.lang_code)

def to_document(format: str):
    if format == 'PDF':
        create_pdf(st.session_state.texts, st.session_state.chap_titles, 
                st.session_state.playlist.channel_name, st.session_state.playlist.name, 
                st.session_state.playlist.list_videos[0].thumbnail_url)
    if format == 'EPUB':
        create_epub(st.session_state.texts, st.session_state.chap_titles, 
                st.session_state.playlist.channel_name, st.session_state.playlist.name, 
                st.session_state.playlist.list_videos[0].thumbnail_url, lang= st.session_state.lang_code)

st.title('Procesador de Playlist de YouTube')
st.session_state.url = st.text_input('Introduce la URL de la playlist de YouTube')


format = st.selectbox('Select the language to extract the transcript', ('es', 'en', 'it', 'fr', 'hi', 'zh', 'ru', 'de'))
if st.button('Procesar videos'):
    process_video(st.session_state.url)
    extraer_scripts(lang_code='es')

if st.button('Guardar scripts extraídos como un audiolibro'):
    to_audiobook()

format = st.selectbox('Selecciona el formato del documento', ('PDF', 'EPUB'))
if st.button('Convertir playlist a documento'):
    to_document(format)
