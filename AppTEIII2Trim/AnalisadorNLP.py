import re
from pathlib import Path
from urllib.request import urlopen

from analyzers import (
    SentimentAnalyzer,
    SpacyAnalyzer,
    StatisticsLexiconAnalyzer,
    TextBlobAnalyzer,
    WordManipulationAnalyzer,
)
from utils import normalize_words, safe_int, validate_text


class AnalisadorNLP:
    """Orquestra funcionalidades NLP dos blocos A-E."""

    def __init__(self):
        self.textblob_analyzer = TextBlobAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.word_analyzer = WordManipulationAnalyzer()
        self.stats_analyzer = StatisticsLexiconAnalyzer()
        self.spacy_analyzer = SpacyAnalyzer()

    def open_file(self, file_path: str) -> str:
        """Lê conteúdo textual de arquivo."""
        valid_path = Path(validate_text(file_path, "arquivo"))
        return valid_path.read_text(encoding="utf-8", errors="ignore")

    def search_url(self, url: str) -> str:
        """Baixa texto simples a partir de uma URL."""
        valid_url = validate_text(url, "URL")
        with urlopen(valid_url, timeout=15) as response:
            content = response.read().decode("utf-8", errors="ignore")
        return re.sub(r"<[^>]+>", " ", content).strip()

    def analyze_block_a(self, text: str):
        """Bloco A: TextBlob fundamentos."""
        valid_text = validate_text(text)
        blob = self.textblob_analyzer.create_blob(valid_text)
        sentences = self.textblob_analyzer.tokenize_sentences(blob)
        words = self.textblob_analyzer.tokenize_words(blob)
        return {
            "sentence_count": len(sentences),
            "word_count": len(words),
            "sentences": sentences,
            "words": words,
            "pos_tags": self.textblob_analyzer.pos_tagging(blob),
            "noun_phrases": self.textblob_analyzer.noun_phrases(blob),
        }

    def analyze_block_b(self, text: str):
        """Bloco B: análise de sentimento."""
        valid_text = validate_text(text)
        blob = self.textblob_analyzer.create_blob(valid_text)
        scores = self.sentiment_analyzer.sentiment_scores(blob)
        scores["interpretation"] = self.sentiment_analyzer.sentiment_interpretation(
            scores["polarity"]
        )
        return scores

    def analyze_block_c(self, text: str):
        """Bloco C: manipulação de palavras."""
        valid_text = validate_text(text)
        words = normalize_words(re.findall(r"\\b\\w+\\b", valid_text))
        return {
            "plural": self.word_analyzer.pluralize_words(words),
            "singular": self.word_analyzer.singularize_words(words),
            "spellcheck": self.word_analyzer.spellcheck_and_correct(valid_text),
            "stemm_lemma": self.word_analyzer.stemming_and_lemmatization(words),
        }

    def analyze_block_d(
        self, text: str, word_for_wordnet: str = "", n_value: str = "2", top_n: str = "10"
    ):
        """Bloco D: estatística e léxico."""
        valid_text = validate_text(text)
        words = normalize_words(re.findall(r"\\b\\w+\\b", valid_text))
        parsed_n = safe_int(n_value, default=2, minimum=1)
        parsed_top_n = safe_int(top_n, default=10, minimum=1)
        details = {"definitions": [], "synonyms": [], "antonyms": []}
        clean_word = word_for_wordnet.strip()
        if clean_word:
            details = self.stats_analyzer.wordnet_details(clean_word)

        no_stop_words = self.stats_analyzer.remove_stop_words(words)
        return {
            "frequency": self.stats_analyzer.word_frequency(words, parsed_top_n),
            "wordnet": details,
            "without_stop_words": " ".join(no_stop_words),
            "ngrams": self.stats_analyzer.generate_ngrams(words, parsed_n),
        }

    def analyze_block_e(self, text: str, comparison_text: str):
        """Bloco E: NER e similaridade com spaCy."""
        valid_text = validate_text(text)
        entities = self.spacy_analyzer.named_entities(valid_text)
        similarity = None
        if comparison_text.strip():
            similarity = self.spacy_analyzer.text_similarity(valid_text, comparison_text)
        return {"entities": entities, "similarity": similarity}

    def analyse_text(self, text: str, comparison_text: str = "", word_for_wordnet: str = ""):
        """Executa todos os blocos de análise."""
        return {
            "A": self.analyze_block_a(text),
            "B": self.analyze_block_b(text),
            "C": self.analyze_block_c(text),
            "D": self.analyze_block_d(text, word_for_wordnet=word_for_wordnet),
            "E": self.analyze_block_e(text, comparison_text),
        }
