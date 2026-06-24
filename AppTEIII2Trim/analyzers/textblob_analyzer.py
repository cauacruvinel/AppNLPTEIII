import re

try:
    from textblob import TextBlob
except ImportError:  # pragma: no cover
    TextBlob = None


class _FallbackBlob:
    def __init__(self, text: str):
        self._text = text

    @property
    def sentences(self):
        return [s.strip() for s in re.split(r"(?<=[.!?])\\s+", self._text) if s.strip()]

    @property
    def words(self):
        return re.findall(r"\\b\\w+\\b", self._text)

    @property
    def tags(self):
        return []

    @property
    def noun_phrases(self):
        return []

    @property
    def sentiment(self):
        return type("Sentiment", (), {"polarity": 0.0, "subjectivity": 0.0})()

    def correct(self):
        return self._text

    def __str__(self):
        return self._text


class TextBlobAnalyzer:
    """Análises fundamentais com TextBlob."""

    def create_blob(self, text: str):
        """Cria o objeto TextBlob base para as análises."""
        if TextBlob is None:
            return _FallbackBlob(text)
        return TextBlob(text)

    def tokenize_sentences(self, blob):
        """Tokeniza o texto em sentenças."""
        try:
            return [str(s) for s in blob.sentences]
        except Exception:
            return [str(blob)]

    def tokenize_words(self, blob):
        """Tokeniza o texto em palavras."""
        try:
            return [str(w) for w in blob.words]
        except Exception:
            return str(blob).split()

    def pos_tagging(self, blob):
        """Executa POS tagging."""
        try:
            return [(word, tag) for word, tag in blob.tags]
        except Exception:
            return []

    def noun_phrases(self, blob):
        """Extrai sintagmas nominais."""
        try:
            return [str(np) for np in blob.noun_phrases]
        except Exception:
            return []
