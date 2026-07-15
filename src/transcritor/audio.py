"""Preparação de áudio com pydub.

Converte arquivos MP3/WAV para o formato ideal de entrada do Whisper:
WAV PCM, mono, 16 kHz. Também aplica normalização de volume, o que
melhora a qualidade da transcrição em gravações com volume baixo.
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from pydub import AudioSegment
from pydub.effects import normalize

logger = logging.getLogger(__name__)

FORMATOS_SUPORTADOS = {".mp3", ".wav"}

# Whisper trabalha internamente com 16 kHz mono
TAXA_AMOSTRAGEM_WHISPER = 16_000


class FormatoNaoSuportadoError(ValueError):
    """Lançada quando o arquivo de entrada não é MP3 nem WAV."""


def validar_arquivo(caminho: str | Path) -> Path:
    """Valida se o arquivo existe e possui um formato suportado."""
    arquivo = Path(caminho)

    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

    if arquivo.suffix.lower() not in FORMATOS_SUPORTADOS:
        raise FormatoNaoSuportadoError(
            f"Formato '{arquivo.suffix}' não suportado. "
            f"Use um dos formatos: {', '.join(sorted(FORMATOS_SUPORTADOS))}"
        )

    return arquivo


def carregar_audio(caminho: str | Path) -> AudioSegment:
    """Carrega um arquivo MP3 ou WAV como AudioSegment."""
    arquivo = validar_arquivo(caminho)
    formato = arquivo.suffix.lower().lstrip(".")

    logger.info("Carregando áudio: %s", arquivo.name)
    return AudioSegment.from_file(arquivo, format=formato)


def preparar_para_whisper(caminho: str | Path) -> Path:
    """Converte o áudio para WAV mono 16 kHz normalizado.

    Retorna o caminho de um arquivo temporário pronto para o Whisper.
    O chamador é responsável por remover o arquivo após o uso.
    """
    audio = carregar_audio(caminho)

    duracao_s = len(audio) / 1000
    logger.info("Duração: %.1fs | Canais: %d | Taxa: %d Hz",
                duracao_s, audio.channels, audio.frame_rate)

    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(TAXA_AMOSTRAGEM_WHISPER)
    audio = normalize(audio)

    destino = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    destino.close()

    audio.export(destino.name, format="wav")
    logger.info("Áudio preparado (WAV mono 16 kHz): %s", destino.name)

    return Path(destino.name)


def duracao_segundos(caminho: str | Path) -> float:
    """Retorna a duração do áudio em segundos."""
    return len(carregar_audio(caminho)) / 1000
