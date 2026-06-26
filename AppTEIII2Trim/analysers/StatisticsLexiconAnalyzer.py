import re
from collections import Counter
from nltk.corpus import stopwords, wordnet
from nltk.util import ngrams

def wordnet_details(word: str) -> dict:
	try:
		synsets = wordnet.synsets(word)
	except LookupError:
		return {"definitions": [], "synonyms": [], "antonyms": [], "examples": []}

	definitions = []
	synonyms = set()
	antonyms = set()
	examples = []

	for synset in synsets:
		definitions.append(synset.definition())
		examples.extend(synset.examples())

		for lemma in synset.lemmas():
			synonyms.add(lemma.name())
			for ant in lemma.antonyms():
				antonyms.add(ant.name())

	return {
		"definitions": list(set(definitions)),
		"synonyms": sorted(synonyms),
		"antonyms": sorted(antonyms),
		"examples": list(set(examples))[:3]
	}

def calculate_lexical_diversity(words) -> dict:
	if not words:
		return {"type_token_ratio": 0.0, "hapax_legomena": 0, "unique_words": 0}

	word_freq = Counter(words)
	unique_words = len(word_freq)
	total_words = len(words)

	hapax = sum(1 for count in word_freq.values() if count == 1)

	return {
		"type_token_ratio": round(unique_words / total_words, 3) if total_words > 0 else 0,
		"hapax_legomena": hapax,
		"unique_words": unique_words,
		"total_words": total_words,
		"lexical_diversity": round(unique_words / total_words, 3) if total_words > 0 else 0
	}


def word_frequency(words, top_n: int = 10) -> list:
	return [
		{"word": w, "count": c}
		for w, c in Counter(words).most_common(top_n)
	]

def generate_ngrams(words, n_value: int) -> list:
	cleaned = [w for w in words if re.search(r"\w", w)]

	if n_value <= 0 or len(cleaned) < n_value:
		return []

	try:
		return [" ".join(g) for g in ngrams(cleaned, n_value)]
	except Exception:
		return [
			" ".join(cleaned[i: i + n_value])
			for i in range(len(cleaned) - n_value + 1)
		]


def text_statistics(text: str, words: list) -> dict:
	sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

	return {
		"word_count": len(words),
		"sentence_count": len(sentences),
		"character_count": len(text),
		"avg_word_length": round(sum(len(w) for w in words) / len(words), 2) if words else 0,
		"avg_sentence_length": round(len(words) / len(sentences), 2) if sentences else 0,
		"unique_words": len(set(words)),
		"lexical_diversity": calculate_lexical_diversity(words)
	}


class StatisticsLexiconAnalyzer:
	def __init__(self):
		self._stopwords_cache = {}

	def remove_stop_words(self, words, language: str = "portuguese") -> list:
		if language not in self._stopwords_cache:
			try:
				self._stopwords_cache[language] = set(stopwords.words(language))
			except LookupError:
				self._stopwords_cache[language] = set()

		stops = self._stopwords_cache[language]
		return [w for w in words if w.lower() not in stops]

	def clear_cache(self):
		self._stopwords_cache.clear()
