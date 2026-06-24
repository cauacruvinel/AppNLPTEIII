try:
    import spacy
except ImportError:  # pragma: no cover
    spacy = None


class SpacyAnalyzer:
    """Análises avançadas com spaCy."""

    def __init__(self):
        self.nlp = self._load_nlp_model()

    def _load_nlp_model(self):
        """Carrega modelo spaCy com fallback seguro."""
        if spacy is None:
            return None
        for model in ("pt_core_news_sm", "en_core_web_sm"):
            try:
                return spacy.load(model)
            except OSError:
                continue
        return spacy.blank("pt")

    def named_entities(self, text: str):
        """Extrai entidades nomeadas."""
        if self.nlp is None:
            return []
        doc = self.nlp(text)
        return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    def text_similarity(self, text_a: str, text_b: str):
        """Calcula similaridade semântica entre dois textos."""
        if self.nlp is None:
            return 0.0
        doc_a = self.nlp(text_a)
        doc_b = self.nlp(text_b)
        return float(doc_a.similarity(doc_b))
