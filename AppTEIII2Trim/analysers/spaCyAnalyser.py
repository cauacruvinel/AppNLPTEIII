import warnings
import spacy
from typing import Optional, List

class SpacyAnalyzer:
	_model_cache = {}

	def __init__(self):
		self.nlp = self._load_nlp_model()

	@classmethod
	def _load_nlp_model(cls) -> Optional[object]:
		models_to_try = [
			"pt_core_news_sm",
			"en_core_web_sm"
		]

		for model_name in models_to_try:
			if model_name in cls._model_cache:
				return cls._model_cache[model_name]

			try:
				model = spacy.load(model_name)
				cls._model_cache[model_name] = model
				return model
			except (OSError, ImportError):
				continue

		try:
			blank_model = spacy.blank("pt")
			cls._model_cache["pt_blank"] = blank_model
			return blank_model
		except Exception:
			return None

	def named_entities(self, text: str) -> List[dict]:
		if self.nlp is None:
			return []

		try:
			doc = self.nlp(text)
			return [
				{
					"text": ent.text,
					"label": ent.label_,
					"start": ent.start_char,
					"end": ent.end_char
				}
				for ent in doc.ents
			]
		except Exception:
			return []

	def text_similarity(self, text_a: str, text_b: str) -> float:
		if self.nlp is None:
			return 0.0

		try:
			doc_a = self.nlp(text_a)
			doc_b = self.nlp(text_b)
			with warnings.catch_warnings():
				warnings.simplefilter("ignore")
				return round(float(doc_a.similarity(doc_b)), 3)
		except Exception:
			return 0.0

	def extract_tokens(self, text: str) -> List[dict]:
		if self.nlp is None:
			return []

		try:
			doc = self.nlp(text)
			return [
				{
					"text": token.text,
					"lemma": token.lemma_,
					"pos": token.pos_,
					"tag": token.tag_,
					"dep": token.dep_,
					"is_stop": token.is_stop
				}
				for token in doc
			]
		except Exception:
			return []

	def dependency_parsing(self, text: str) -> dict:
		if self.nlp is None:
			return {"dependencies": [], "root": None}

		try:
			doc = self.nlp(text)
			dependencies = []
			root = None

			for token in doc:
				if token.dep_ == "ROOT":
					root = token.text

				dependencies.append({
					"child": token.text,
					"relation": token.dep_,
					"head": token.head.text
				})

			return {"dependencies": dependencies, "root": root}
		except Exception:
			return {"dependencies": [], "root": None}

	@classmethod
	def clear_model_cache(cls):
		cls._model_cache.clear()
