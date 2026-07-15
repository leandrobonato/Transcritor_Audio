"""Interface de linha de comando do Transcritor de Áudio."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from . import __version__
from .audio import FormatoNaoSuportadoError
from .resumo import ChaveApiAusenteError, resumir
from .transcricao import MODELO_PADRAO, MODELOS_DISPONIVEIS, transcrever

logger = logging.getLogger("transcritor")


def _montar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="transcritor",
        description=(
            "Transcreve áudios MP3/WAV para texto com Whisper e gera um "
            "resumo inteligente do conteúdo com IA."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "audio",
        help="Caminho do arquivo de áudio (.mp3 ou .wav)",
    )
    parser.add_argument(
        "-m", "--modelo",
        choices=MODELOS_DISPONIVEIS,
        default=MODELO_PADRAO,
        help="Modelo Whisper a utilizar (maior = mais preciso e mais lento)",
    )
    parser.add_argument(
        "-i", "--idioma",
        default=None,
        help="Código do idioma do áudio (ex.: pt, en). Padrão: detecção automática",
    )
    parser.add_argument(
        "-o", "--saida",
        default="saida",
        help="Pasta onde salvar a transcrição e o resumo",
    )
    parser.add_argument(
        "--sem-resumo",
        action="store_true",
        help="Apenas transcreve, sem gerar o resumo com IA",
    )
    parser.add_argument(
        "--com-tempos",
        action="store_true",
        help="Inclui marcações de tempo na transcrição salva",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _salvar(pasta: Path, nome: str, conteudo: str) -> Path:
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / nome
    destino.write_text(conteudo, encoding="utf-8")
    return destino


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )

    args = _montar_parser().parse_args(argv)
    entrada = Path(args.audio)
    pasta_saida = Path(args.saida)

    try:
        resultado = transcrever(entrada, modelo=args.modelo, idioma=args.idioma)
    except (FileNotFoundError, FormatoNaoSuportadoError, ValueError) as erro:
        logger.error("%s", erro)
        return 1

    conteudo = (
        resultado.texto_com_tempos if args.com_tempos else resultado.texto
    )
    arquivo_transcricao = _salvar(
        pasta_saida, f"{entrada.stem}_transcricao.txt", conteudo
    )
    logger.info("Transcrição salva em: %s", arquivo_transcricao)

    print("\n" + "=" * 60)
    print("TRANSCRIÇÃO")
    print("=" * 60)
    print(resultado.texto)

    if not args.sem_resumo:
        try:
            resumo = resumir(resultado.texto)
        except ChaveApiAusenteError as erro:
            logger.warning("%s", erro)
            logger.warning("Resumo ignorado. Use --sem-resumo para ocultar este aviso.")
        else:
            arquivo_resumo = _salvar(
                pasta_saida, f"{entrada.stem}_resumo.md", resumo
            )
            logger.info("Resumo salvo em: %s", arquivo_resumo)

            print("\n" + "=" * 60)
            print("RESUMO")
            print("=" * 60)
            print(resumo)

    return 0


if __name__ == "__main__":
    sys.exit(main())
