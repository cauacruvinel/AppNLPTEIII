from textblob import TextBlob

class SentimentAnalyzer:

	POSITIVE_THRESHOLD = 0.1
	NEGATIVE_THRESHOLD = -0.1

	def sentiment_scores(self, blob: TextBlob) -> dict:
		s = blob.sentiment
		return {
			"polarity": round(s.polarity, 3),
			"subjectivity": round(s.subjectivity, 3)
		}

	def sentiment_interpretation(self, polarity: float) -> str:
		if polarity > self.POSITIVE_THRESHOLD:
			return "Texto predominantemente positivo."
		elif polarity < self.NEGATIVE_THRESHOLD:
			return "Texto predominantemente negativo."
		else:
			return "Texto predominantemente neutro."

	def get_sentiment_details(self, blob: TextBlob) -> dict:
		scores = self.sentiment_scores(blob)
		polarity = scores["polarity"]

		return {
			**scores,
			"interpretation": self.sentiment_interpretation(polarity),
			"strength": abs(polarity),
			"objectivity": 1 - scores["subjectivity"]
		}
