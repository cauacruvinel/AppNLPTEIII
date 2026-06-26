import re
from typing import Iterable, List
from functools import lru_cache
from bs4 import BeautifulSoup

@lru_cache(maxsize=128)
def validate_text(text: str, field_name: str = "texto") -> str:
	if text is None:
		raise ValueError(f"O campo '{field_name}' é obrigatório.")
	normalized = text.strip()
	if not normalized:
		raise ValueError(f"O campo '{field_name}' não pode estar vazio.")
	return normalized

def normalize_words(words: Iterable[str]) -> List[str]:
	return [w.lower() for w in words if re.search(r"\w", w)]

def safe_int(value: str, default: int, minimum: int = 1) -> int:
	try:
		parsed = int(str(value).strip())
		return parsed if parsed >= minimum else default
	except (TypeError, ValueError):
		return default

def extract_text_from_html(html_content: str, remove_scripts: bool = True) -> str:
	soup = BeautifulSoup(html_content, "html.parser")
	for tag in soup(["script", "style"]):
		tag.decompose()

	return " ".join(soup.get_text(separator=" ").split())
