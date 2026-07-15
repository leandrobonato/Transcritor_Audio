"""Motor de respostas para dúvidas frequentes (FAQ).

Combina busca por palavras-chave com similaridade de texto (difflib),
tolerando acentuação e pequenos erros de digitação.
"""

import json
import unicodedata
from difflib import SequenceMatcher

from bot.config import CAMINHO_FAQS

LIMIAR_SIMILARIDADE = 0.72


def normalizar(texto: str) -> str:
    """Remove acentos, pontuação básica e converte para minúsculas."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.split())


def _carregar_faqs() -> list[dict]:
    with open(CAMINHO_FAQS, encoding="utf-8") as arquivo:
        return json.load(arquivo)


FAQS = _carregar_faqs()


def buscar_resposta(mensagem: str) -> str | None:
    """Retorna a resposta do FAQ mais compatível com a mensagem, ou None."""
    texto = normalizar(mensagem)
    if not texto:
        return None

    melhor_resposta = None
    melhor_pontuacao = 0.0

    for faq in FAQS:
        pontuacao = _pontuar(texto, faq)
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_resposta = faq["resposta"]

    if melhor_pontuacao >= LIMIAR_SIMILARIDADE:
        return melhor_resposta
    return None


def _pontuar(texto: str, faq: dict) -> float:
    """Calcula o quão bem a mensagem casa com um item do FAQ (0.0 a 1.0)."""
    # Palavra-chave contida na mensagem é o sinal mais forte.
    for chave in faq["palavras_chave"]:
        chave_normalizada = normalizar(chave)
        if chave_normalizada in texto:
            return 1.0

    # Sem palavra-chave exata, compara a similaridade com a pergunta cadastrada
    # e com cada palavra-chave individualmente.
    candidatos = [normalizar(faq["pergunta"])] + [normalizar(c) for c in faq["palavras_chave"]]
    pontuacoes = [SequenceMatcher(None, texto, candidato).ratio() for candidato in candidatos]

    palavras_mensagem = texto.split()
    for chave in faq["palavras_chave"]:
        for palavra in palavras_mensagem:
            pontuacoes.append(SequenceMatcher(None, palavra, normalizar(chave)).ratio())

    return max(pontuacoes)


def listar_perguntas() -> str:
    """Monta a lista numerada de perguntas disponíveis no FAQ."""
    linhas = [f"  {i}. {faq['pergunta']}" for i, faq in enumerate(FAQS, start=1)]
    return "\n".join(linhas)
