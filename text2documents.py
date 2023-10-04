import io
import random
import requests
from PIL import Image
from ebooklib import epub
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_epub(texts: list[str], chapters_name: list[str], author: str, title: str, cover_url: str, lang = 'en'):
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('id' + random.randint(10_000, 19_999))
    book.set_title(title)
    book.set_language(lang)
    if requests.get(cover_url).status_code == 200:
        book.set_cover('cover.jpg', requests.get(cover_url).content)
    book.add_author(author)

    chapters = []
    for i, text in enumerate(texts):
        chapter = chapters_name[i] if len(chapters_name) == len(text) else f'Chapter {i+1}'
        c = epub.EpubHtml(title= chapter, file_name=f'chap_{i+1}.xhtml', lang= lang)
        c.content = text
        book.add_item(c)
        chapters.append(c)
    # Define Table Of Contents
    book.toc = chapters
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # Add CSS file
    book.add_item(nav_css)

    # Create book spine
    book.spine = ['nav'] + chapters

    # Write EPUB file
    epub.write_epub(f'{title} - {author}.epub', book)
    
def create_pdf(texts: list[str], chapters_name: list[str], author: str, title: str, cover_url: str):
    c = canvas.Canvas(f"{title}.pdf", pagesize=letter)
    width, height = letter

    # Add cover image if the URL is valid
    if requests.get(cover_url).status_code == 200:
        image_data = requests.get(cover_url).content
        image = Image.open(io.BytesIO(image_data))
        c.drawImage(image, 0, 0, width=width, height=height)
        c.showPage()

    for i, text in enumerate(texts):
        # Add text to the page
        c.setFont("Helvetica", 10)
        chapter = chapters_name[i] if len(chapters_name) == len(text) else f'Chapter {i+1}'
        c.drawString(10, height - 50, chapter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, height - 100)
        textobject.textLines(text)
        c.drawText(textobject)
        c.showPage()

    # Save the PDF file
    c.save()
