from urllib.request import urlopen

import spacy
from textblob import TextBlob
from nltk import *
import requests
from bs4 import BeautifulSoup
import Interface

class AnalisadorNLP(Interface):
    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("pt_core_news_sm")

    def search_url(self):
        url = self._widgets["text_url"].get()
        if not url.strip():
            self._widgets["status"].configure(text="⚠ Insira uma URL válida.")
            return
        self._widgets["status"].configure(text=f"🔄 Buscando: {url}")
        answer = requests.get(url)

        if answer.status_code == 200:
            html_content = BeautifulSoup(answer.content, "html.parser")
            text = html_content.get_text()
            self._widgets["textbox"].insert("end", text)
            self.analyse_text()

    def analyse_text(self):
        text = self._widgets["textbox"].get("1.0", "end").strip()
        if not text:
            self._widgets["status"].configure(text="⚠ Nenhum texto para analisar.")
            return
        self._widgets["status"].configure(text="🔍 Analisando...")

        blob = TextBlob(text)
        phrases = sent_tokenize(text)
        blob.nons = [word.lemma_ for word in blob.words]
