import re
from textblob import TextBlob
from functools import lru_cache

class _FallbackBlob:
	def __init__(self, text: str):
		self._text = text

	@property
	def sentences(self):
		return [s.strip() for s in re.split(r"(?<=[.!?])\s+", self._text) if s.strip()]

	@property
	def words(self):
		return re.findall(r"\b\w+\b", self._text)

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
	def __init__(self):
		self._blob_cache = {}

	@lru_cache(maxsize=64)
	def _create_blob_cached(self, text: str):
		return TextBlob(text)

	def create_blob(self, text: str):
		try:
			return self._create_blob_cached(text)
		except Exception:
			return _FallbackBlob(text)

	def tokenize_sentences(self, blob):
		try:
			return [str(s).strip() for s in blob.sentences]
		except Exception:
			return [str(blob)]

	def tokenize_words(self, blob):
		try:
			return [str(w).lower() for w in blob.words]
		except Exception:
			return str(blob).lower().split()

	def pos_tagging(self, blob):
		try:
			return [(word, tag) for word, tag in blob.tags]
		except Exception:
			return []

	def noun_phrases(self, blob):
		try:
			return [str(np).strip() for np in blob.noun_phrases]
		except Exception:
			return []

	def clear_cache(self):
		self._blob_cache.clear()
