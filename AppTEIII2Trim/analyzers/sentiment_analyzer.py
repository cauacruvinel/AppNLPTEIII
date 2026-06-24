class SentimentAnalyzer:
    """Análise de sentimento com TextBlob."""

    def sentiment_scores(self, blob):
        """Obtém polaridade e subjetividade."""
        s = blob.sentiment
        return {"polarity": s.polarity, "subjectivity": s.subjectivity}

    def sentiment_interpretation(self, polarity: float) -> str:
        """Interpreta textual da polaridade."""
        if polarity > 0.1:
            return "Texto predominantemente positivo."
        if polarity < -0.1:
            return "Texto predominantemente negativo."
        return "Texto predominantemente neutro."
