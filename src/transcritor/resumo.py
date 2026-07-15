"""Resumo inteligente da transcrição usando a API da OpenAI.

Requer a variável de ambiente OPENAI_API_KEY (pode ser definida em um
arquivo .env na raiz do projeto).
"""

from __future__ import annotations

import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

MODELO_PADRAO = "gpt-4o-mini"

PROMPT_SISTEMA = """\
Você é um assistente especializado em resumir transcrições de áudio.
Responda sempre no mesmo idioma da transcrição.

Produza um resumo com a seguinte estrutura em Markdown:

## Resumo
Um parágrafo conciso com a ideia central do áudio.

## Pontos principais
Lista com os pontos mais importantes abordados.

## Ações e decisões
Lista de tarefas, compromissos ou decisões mencionadas.
Se não houver, escreva "Nenhuma ação ou decisão identificada."
"""


class ChaveApiAusenteError(RuntimeError):
    """Lançada quando OPENAI_API_KEY não está configurada."""


def resumir(texto: str, modelo: str = MODELO_PADRAO) -> str:
    """Gera um resumo estruturado do texto transcrito.

    Args:
        texto: transcrição completa a ser resumida.
        modelo: modelo de chat da OpenAI a utilizar.

    Returns:
        Resumo em Markdown com ideia central, pontos principais e ações.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise ChaveApiAusenteError(
            "A variável OPENAI_API_KEY não está definida. "
            "Configure-a no ambiente ou em um arquivo .env para gerar resumos."
        )

    if not texto.strip():
        raise ValueError("A transcrição está vazia; não há o que resumir.")

    logger.info("Gerando resumo com o modelo '%s'...", modelo)

    cliente = OpenAI()
    resposta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": f"Transcrição:\n\n{texto}"},
        ],
        temperature=0.3,
    )

    resumo = resposta.choices[0].message.content.strip()
    logger.info("Resumo gerado com sucesso.")
    return resumo
