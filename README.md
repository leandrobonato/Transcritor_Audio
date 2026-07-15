# 🎙️ Transcritor de Áudio com IA

> Transforme reuniões, entrevistas, aulas e podcasts em **texto pesquisável** e **resumos executivos** — em um único comando.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?logo=openai&logoColor=white)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

---

## 💡 O problema que este projeto resolve

Horas de áudio gravado viram conhecimento perdido: ninguém reouve uma reunião de 1 hora para achar uma decisão de 30 segundos. Este sistema automatiza o ciclo completo:

**Áudio (MP3/WAV) → Texto → Resumo estruturado com pontos principais e ações**

Casos de uso reais:

- 📋 **Atas de reunião** geradas automaticamente, com decisões e tarefas destacadas
- 🎤 **Entrevistas e pesquisas** transcritas para análise qualitativa
- 🎓 **Aulas e palestras** convertidas em material de estudo
- 🎧 **Podcasts** transformados em show notes e conteúdo para blog

## ⚙️ Como funciona

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  MP3 / WAV  │ →  │  pydub           │ →  │  Whisper        │ →  │  IA (OpenAI)     │
│  (entrada)  │    │  normalização e  │    │  fala → texto   │    │  resumo, pontos  │
│             │    │  conversão 16kHz │    │  (100% local)   │    │  e ações         │
└─────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘
```

1. **Preparação (pydub):** o áudio é convertido para WAV mono 16 kHz e tem o volume normalizado — o formato ideal para o Whisper, melhorando a precisão em gravações de baixa qualidade.
2. **Transcrição (openai-whisper):** o modelo Whisper roda **localmente na sua máquina** — nenhum áudio sai do seu computador nesta etapa. Detecta o idioma automaticamente e gera segmentos com marcação de tempo.
3. **Resumo (IA):** a transcrição é enviada à API da OpenAI, que devolve um resumo estruturado: ideia central, pontos principais e ações/decisões identificadas.

## 🚀 Instalação

**Pré-requisitos:** Python 3.10+ e [FFmpeg](https://ffmpeg.org/download.html) (usado pelo pydub e pelo Whisper).

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/Transcritor_Audio.git
cd Transcritor_Audio

# 2. Crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. (Opcional — apenas para o resumo com IA)
# Copie .env.example para .env e adicione sua chave da OpenAI
copy .env.example .env
```

> 💡 **Sem chave da OpenAI?** O sistema funciona normalmente como transcritor: use a flag `--sem-resumo`.

## 📖 Uso

```bash
# Transcrever e resumir
python main.py reuniao.mp3

# Apenas transcrever (sem custo de API, 100% offline)
python main.py entrevista.wav --sem-resumo

# Mais precisão: modelo maior + idioma fixo
python main.py aula.mp3 --modelo small --idioma pt

# Transcrição com marcações de tempo
python main.py podcast.mp3 --com-tempos
```

Os resultados são salvos na pasta `saida/`:

| Arquivo | Conteúdo |
|---|---|
| `<nome>_transcricao.txt` | Transcrição completa do áudio |
| `<nome>_resumo.md` | Resumo em Markdown: ideia central, pontos principais, ações e decisões |

### Opções disponíveis

| Opção | Descrição | Padrão |
|---|---|---|
| `-m, --modelo` | Modelo Whisper: `tiny`, `base`, `small`, `medium`, `large` | `base` |
| `-i, --idioma` | Código do idioma (`pt`, `en`, ...) | detecção automática |
| `-o, --saida` | Pasta de destino dos arquivos gerados | `saida` |
| `--sem-resumo` | Pula a etapa de resumo com IA | — |
| `--com-tempos` | Salva a transcrição com marcações `[MM:SS → MM:SS]` | — |

### Qual modelo escolher?

| Modelo | Velocidade | Precisão | Indicado para |
|---|---|---|---|
| `tiny` / `base` | ⚡ rápido | boa | testes e áudios com fala clara |
| `small` / `medium` | 🚶 moderado | muito boa | reuniões e entrevistas |
| `large` | 🐢 lento | excelente | áudios com ruído ou múltiplas vozes |

## 🧩 Exemplo de saída do resumo

```markdown
## Resumo
Reunião de alinhamento do projeto X, com foco no cronograma de entrega
e na divisão de responsabilidades entre as equipes de design e backend.

## Pontos principais
- O prazo da entrega final foi mantido para o dia 30.
- A equipe de design entregará os protótipos até sexta-feira.
- Foi identificado um risco de atraso na integração com o gateway de pagamento.

## Ações e decisões
- João ficará responsável pela homologação do gateway até o dia 22.
- Decidido: a demo para o cliente será na quinta-feira, às 14h.
```

## 🏗️ Arquitetura do projeto

```
Transcritor_Audio/
├── main.py                     # Ponto de entrada
├── requirements.txt
├── .env.example                # Modelo de configuração da API
└── src/transcritor/
    ├── cli.py                  # Interface de linha de comando
    ├── audio.py                # Preparação do áudio (pydub)
    ├── transcricao.py          # Fala → texto (openai-whisper)
    └── resumo.py               # Resumo inteligente (API OpenAI)
```

O código segue separação de responsabilidades: cada módulo tem uma única função no pipeline e pode ser usado de forma independente — por exemplo, importar `transcritor.transcricao.transcrever()` em outro projeto ou numa API web.

## 🛠️ Tecnologias

| Tecnologia | Papel |
|---|---|
| [openai-whisper](https://github.com/openai/whisper) | Reconhecimento de fala estado-da-arte, executado localmente |
| [pydub](https://github.com/jiaaro/pydub) | Conversão, normalização e manipulação de áudio |
| [OpenAI API](https://platform.openai.com/) | Geração do resumo estruturado com IA |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Gestão segura de credenciais via `.env` |

## 🗺️ Possíveis evoluções

- [ ] Interface web (Streamlit/Gradio) com upload de arquivos
- [ ] Suporte a mais formatos (M4A, OGG, FLAC) e a vídeos
- [ ] Identificação de falantes (diarização)
- [ ] Processamento em lote de múltiplos arquivos
- [ ] Exportação para SRT/VTT (legendas)

## 📄 Licença

Distribuído sob a licença MIT. Sinta-se à vontade para usar e adaptar.

---

*Desenvolvido por **Leandro Miozzo Bonato** — projeto de portfólio demonstrando integração de processamento de áudio, reconhecimento de fala e IA generativa em Python.*
