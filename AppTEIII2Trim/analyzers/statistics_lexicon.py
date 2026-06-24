import re
from collections import Counter

try:
    from nltk import ngrams as nltk_ngrams
    from nltk.corpus import stopwords, wordnet
except ImportError:  # pragma: no cover
    nltk_ngrams = None
    stopwords = None
    wordnet = None


class StatisticsLexiconAnalyzer:
    """Análises estatísticas e léxicas."""

    def word_frequency(self, words, top_n: int = 10):
        """Retorna top N palavras por frequência."""
        return Counter(words).most_common(top_n)

    def wordnet_details(self, word: str):
        """Busca definições, sinônimos e antônimos no WordNet."""
        if wordnet is None:
            return {"definitions": [], "synonyms": [], "antonyms": []}
        try:
            synsets = wordnet.synsets(word)
        except LookupError:
            return {"definitions": [], "synonyms": [], "antonyms": []}

        definitions = []
        synonyms = set()
        antonyms = set()
        for synset in synsets:
            definitions.append(synset.definition())
            for lemma in synset.lemmas():
                synonyms.add(lemma.name())
                for ant in lemma.antonyms():
                    antonyms.add(ant.name())
        return {
            "definitions": definitions,
            "synonyms": sorted(synonyms),
            "antonyms": sorted(antonyms),
        }

    def remove_stop_words(self, words, language: str = "portuguese"):
        """Remove stop words de uma lista de palavras."""
        if stopwords is None:
            return words
        try:
            stops = set(stopwords.words(language))
        except LookupError:
            stops = set()
        return [w for w in words if w.lower() not in stops]

    def generate_ngrams(self, words, n_value: int):
        """Gera n-gramas customizados."""
        cleaned = [w for w in words if re.search(r"\\w", w)]
        if n_value <= 0:
            return []
        if nltk_ngrams is not None:
            return [" ".join(g) for g in nltk_ngrams(cleaned, n_value)]
        return [" ".join(cleaned[i : i + n_value]) for i in range(len(cleaned) - n_value + 1)]
