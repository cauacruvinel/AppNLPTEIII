import requests
import nltk
from TextBlobAnalyser import TextBlobAnalyzer
from SentimentAnalyser import SentimentAnalyzer
from spaCyAnalyser import *
from StatisticsLexiconAnalyzer import (
	StatisticsLexiconAnalyzer, wordnet_details,
	word_frequency, generate_ngrams, text_statistics
)
from utils import *

class NLPAnalyser:
	def __init__(self):

		resources = [
			("corpora/stopwords", "stopwords"),
			("corpora/wordnet", "wordnet"),
			("tokenizers/punkt", "punkt"),
			("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger"),
		]
		for path, name in resources:
			try:
				nltk.data.find(path)
			except LookupError:
				nltk.download(name, quiet=True)

		self.textblob = TextBlobAnalyzer()
		self.sentiment = SentimentAnalyzer()
		self.spacy = SpacyAnalyzer()
		self.lexicon = StatisticsLexiconAnalyzer()

	def analyse_block_a(self, text: str) -> dict:
		text = validate_text(text)
		blob = self.textblob.create_blob(text)

		return {
			"sentences": self.textblob.tokenize_sentences(blob),
			"words": self.textblob.tokenize_words(blob),
			"pos_tags": self.textblob.pos_tagging(blob),
			"noun_phrases": self.textblob.noun_phrases(blob),
		}

	def analyse_block_b(self, text: str) -> dict:
		text = validate_text(text)
		blob = self.textblob.create_blob(text)
		return self.sentiment.get_sentiment_details(blob)

	def analyse_block_c(self, text: str) -> dict:
		text = validate_text(text)
		blob = self.textblob.create_blob(text)
		words = normalize_words(self.textblob.tokenize_words(blob))
		filtered = self.lexicon.remove_stop_words(words)

		return {
			"statistics": text_statistics(text, words),
			"filtered_words": filtered,
			"word_frequency": word_frequency(filtered),
		}

	def analyse_block_d(self, text: str,
	                    word_for_wordnet="", n_value="2",
	                    top_n="10") -> dict:
		text = validate_text(text)
		blob = self.textblob.create_blob(text)
		words = normalize_words(self.textblob.tokenize_words(blob))

		return {
			"ngrams": generate_ngrams(words, safe_int(n_value, default=2)),
			"top_words": word_frequency(words, safe_int(top_n, default=10)),
			"wordnet": wordnet_details(word_for_wordnet) if word_for_wordnet else {},
		}

	def analyse_block_e(self, text: str, compare_text: str) -> dict:
		text = validate_text(text)

		return {
			"entities": self.spacy.named_entities(text),
			"tokens": self.spacy.extract_tokens(text),
			"dependencies": self.spacy.dependency_parsing(text),
			"similarity": self.spacy.text_similarity(text, compare_text) if compare_text.strip() else None,
		}

	def analyse_text(self, text: str, comparison_text="", word_for_wordnet="") -> dict:
		return {
			"block_a": self.analyse_block_a(text),
			"block_b": self.analyse_block_b(text),
			"block_c": self.analyse_block_c(text),
			"block_d": self.analyse_block_d(text, word_for_wordnet=word_for_wordnet),
			"block_e": self.analyse_block_e(text, comparison_text),
		}

	def search_url(self, url: str) -> str:
		resp = requests.get(url, timeout=10)
		resp.raise_for_status()
		return extract_text_from_html(resp.text)



