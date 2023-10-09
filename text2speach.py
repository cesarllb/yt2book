from text_to_speech import save

def save_as_audiobook(texts: list[str], title: str, lang_code: str, output_folder = ''):
    text = ''.join(texts)
    output_file = f"{title}.mp3"  # Specify the output file (only accepts .mp3)
    lang_code = lang_code.lower() if len(lang_code) == 2 else lang_code[:2]
    save(text, lang_code, file=output_file)