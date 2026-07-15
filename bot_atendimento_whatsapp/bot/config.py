"""Configurações centralizadas do bot, carregadas do arquivo .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

NOME_EMPRESA = os.getenv("NOME_EMPRESA", "Minha Empresa")
HORARIO_INICIO = os.getenv("HORARIO_INICIO", "08:00")
HORARIO_FIM = os.getenv("HORARIO_FIM", "18:00")

FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

CAMINHO_BANCO = BASE_DIR / "agendamentos.db"
CAMINHO_FAQS = BASE_DIR / "bot" / "faqs.json"
