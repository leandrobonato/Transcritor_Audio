"""Transcrição de fala em texto com openai-whisper.

O modelo roda 100% localmente — nenhum áudio é enviado para a nuvem
nesta etapa. Modelos disponíveis (do mais rápido ao mais preciso):
tiny, base, small, medium, large.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

import whisper

from .audio import preparar_para_whisper

logger = logging.getLogger(__name__)

MODELOS_DISPONIVEIS = ("tiny", "base", "small", "medium", "large")
MODELO_PADRAO = "base"


@dataclass
class ResultadoTranscricao:
    """Resultado de uma transcrição."""

    texto: str
    idioma: str
    segmentos: list[dict] = field(default_factory=list)

    @property
    def texto_com_tempos(self) -> str:
        """Transcrição formatada com marcações de tempo por trecho."""
        linhas = []
        for seg in self.segmentos:
            inicio = _formatar_tempo(seg["start"])
            fim = _formatar_tempo(seg["end"])
            linhas.append(f"[{inicio} → {fim}] {seg['text'].strip()}")
        return "\n".join(linhas)


def _formatar_tempo(segundos: float) -> str:
    """Formata segundos como MM:SS."""
    minutos, seg = divmod(int(segundos), 60)
    return f"{minutos:02d}:{seg:02d}"


def transcrever(
    caminho_audio: str | Path,
    modelo: str = MODELO_PADRAO,
    idioma: str | None = None,
) -> ResultadoTranscricao:
    """Transcreve um arquivo MP3/WAV para texto.

    Args:
        caminho_audio: caminho do arquivo de áudio (.mp3 ou .wav).
        modelo: nome do modelo Whisper (tiny, base, small, medium, large).
        idioma: código do idioma (ex.: "pt"). Se None, é detectado
            automaticamente.

    Returns:
        ResultadoTranscricao com o texto completo, idioma detectado e
        segmentos com marcações de tempo.
    """
    if modelo not in MODELOS_DISPONIVEIS:
        raise ValueError(
            f"Modelo '{modelo}' inválido. "
            f"Opções: {', '.join(MODELOS_DISPONIVEIS)}"
        )

    logger.info("Carregando modelo Whisper '%s'...", modelo)
    modelo_whisper = whisper.load_model(modelo)

    wav_temporario = preparar_para_whisper(caminho_audio)
    try:
        logger.info("Transcrevendo... (isso pode levar alguns minutos)")
        resultado = modelo_whisper.transcribe(
            str(wav_temporario),
            language=idioma,
            fp16=False,  # evita aviso em máquinas sem GPU
        )
    finally:
        os.unlink(wav_temporario)

    logger.info("Transcrição concluída (idioma: %s)", resultado["language"])

    return ResultadoTranscricao(
        texto=resultado["text"].strip(),
        idioma=resultado["language"],
        segmentos=resultado.get("segments", []),
    )
