from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from ui_core import process_video, extract_transcripts, to_document, to_audiobook


class YoutubeTranscriptUI(App):
        
    def build(self):
        Window.size = (600, 300)
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        title = Label(text='Process YouTube list', size_hint=(1, 0.25), font_size=30)
        main_layout.add_widget(title)

        self.input = TextInput(multiline=False, size_hint=(1, None), height=50)
        main_layout.add_widget(self.input)
        
        row = BoxLayout(orientation='horizontal')
        col1 = BoxLayout(orientation='vertical', size_hint=(0.5, None))
        col2 = BoxLayout(orientation='vertical', size_hint=(0.5, None))
        row.add_widget(col1); row.add_widget(col2)
        main_layout.add_widget(row)
        
        self.select_box_doc_format = Spinner(
            text='Select the document format',
            values=('PDF', 'EPUB'),
            size_hint=(1, 0.3)
        )
        col1.add_widget(self.select_box_doc_format)

        self.select_box_lang = Spinner(
            text='Select the language to extract the transcript',
            values=('es', 'en', 'it', 'fr', 'hi', 'zh', 'ru', 'de'),
            size_hint=(1, 0.3)
        )
        col1.add_widget(self.select_box_lang)

        # Buttons
        button_2 = Button(text='Save scripts in an audiobook')
        button_2.bind(on_press=self.save_audiobook)
        col2.add_widget(button_2)
        button_3 = Button(text='Convert playlist to document')
        button_3.bind(on_press=self.save_as_document)
        col2.add_widget(button_3)
        
        button_1 = Button(text='Process',size_hint=(1, 0.3))
        button_1.bind(on_press=self.procces_url)
        main_layout.add_widget(button_1)

        return main_layout
    
    def procces_url(self, instance):
        if self.input.text:
            self.playlist = process_video(str(self.input.text))
            self.texts, self.chap_titles = extract_transcripts(self.playlist, 
                                            lang_code= self.select_box_lang.text if self.select_box_lang.text else 'en')
        
    def save_audiobook(self, instance):
        to_audiobook(self.texts, self.title, self.select_box_lang.text)
        
    def save_as_document(self, instance):
        to_document(self.texts, self.chap_titles, self.playlist.channel_name, self.playlist.name, 
                    self.playlist.list_videos[0].thumbnail_url, self.select_box_doc_format.text)
        
if __name__ == '__main__':
    YoutubeTranscriptUI().run()
