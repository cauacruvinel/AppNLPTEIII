try:
    from nltk.stem import PorterStemmer, WordNetLemmatizer
except ImportError:  # pragma: no cover
    PorterStemmer = None
    WordNetLemmatizer = None

try:
    from textblob import TextBlob, Word
except ImportError:  # pragma: no cover
    TextBlob = None
    Word = None


class WordManipulationAnalyzer:
    """Manipulação e normalização de palavras."""

    def _pluralize(self, word: str) -> str:
        if Word is not None:
            return str(Word(word).pluralize())
        return f"{word}s" if not word.endswith("s") else word

    def _singularize(self, word: str) -> str:
        if Word is not None:
            return str(Word(word).singularize())
        return word[:-1] if word.endswith("s") else word

    def pluralize_words(self, words):
        """Retorna flexão para plural."""
        return {w: self._pluralize(w) for w in words}

    def singularize_words(self, words):
        """Retorna flexão para singular."""
        return {w: self._singularize(w) for w in words}

    def spellcheck_and_correct(self, text: str):
        """Sugere correções ortográficas e texto corrigido."""
        if TextBlob is None:
            return {"corrections": {}, "corrected_text": text}
        blob = TextBlob(text)
        corrections = {}
        for token in blob.words:
            suggestion = str(token.correct())
            if suggestion.lower() != str(token).lower():
                corrections[str(token)] = suggestion
        return {"corrections": corrections, "corrected_text": str(blob.correct())}

    def stemming_and_lemmatization(self, words):
        """Compara stemming e lematização."""
        stemmer = PorterStemmer() if PorterStemmer else None
        lemmatizer = WordNetLemmatizer() if WordNetLemmatizer else None
        result = []
        for word in words:
            stem = stemmer.stem(word) if stemmer else word
            if lemmatizer:
                try:
                    lemma = lemmatizer.lemmatize(word)
                except LookupError:
                    lemma = word
            else:
                lemma = word
            result.append({"word": word, "stem": stem, "lemma": lemma})
        return result
