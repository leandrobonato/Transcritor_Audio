"""Ponto de entrada do Transcritor de Áudio.

Uso:
    python main.py caminho/do/audio.mp3
    python main.py reuniao.wav --modelo small --idioma pt
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from transcritor.cli import main

if __name__ == "__main__":
    sys.exit(main())
