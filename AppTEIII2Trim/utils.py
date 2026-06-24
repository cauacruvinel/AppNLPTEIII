import re
from typing import Iterable, List


def validate_text(text: str, field_name: str = "texto") -> str:
    """Valida entrada textual e retorna conteúdo limpo."""
    if text is None:
        raise ValueError(f"O campo '{field_name}' é obrigatório.")
    normalized = text.strip()
    if not normalized:
        raise ValueError(f"O campo '{field_name}' não pode estar vazio.")
    return normalized


def normalize_words(words: Iterable[str]) -> List[str]:
    """Normaliza tokens removendo ruído e convertendo para minúsculas."""
    return [w.lower() for w in words if re.search(r"\\w", w)]


def safe_int(value: str, default: int, minimum: int = 1) -> int:
    """Converte texto para inteiro com fallback seguro."""
    try:
        parsed = int(str(value).strip())
        return parsed if parsed >= minimum else default
    except (TypeError, ValueError):
        return default
