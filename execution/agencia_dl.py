#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================
  agencia_dl.py — Agência Digital Automatizada da DL Soluções Condominiais
==========================================================================
"""
from __future__ import annotations

import os
import io
import sys
import subprocess
import random
import logging
import datetime
import pathlib
import time
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

import requests
from dotenv import load_dotenv

# Google Drive
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Google Gemini AI (Vertex)
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google import genai

# ============================================================================
#  CONFIGURAÇÃO INICIAL
# ============================================================================

# Garante que o console do Windows imprima emojis/unicode sem crash
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_EXECUTION_DIR = pathlib.Path(__file__).resolve().parent
load_dotenv(_EXECUTION_DIR / ".env")

TMP_DIR = _PROJECT_ROOT / "tmp"
TMP_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("agencia_dl")

# Google Drive
GOOGLE_CREDENTIALS_PATH = pathlib.Path(
    os.getenv("GOOGLE_CREDENTIALS_PATH", "")
) if os.getenv("GOOGLE_CREDENTIALS_PATH") else pathlib.Path(
    r"C:\Users\Diogo\Documents\Arquivista_DL\credentials_drive.json"
)
GOOGLE_TOKEN_PATH = _PROJECT_ROOT / "token_arquivista.json"
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")

# Google Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Meta Graph API
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
# Este é o ID da sua página do Facebook
META_PAGE_ID = os.getenv("META_PAGE_ID", "")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
META_GRAPH_URL = "https://graph.facebook.com/v19.0"

# Vertex AI (Imagen)
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "spry-framework-284300")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")

if GCP_PROJECT_ID:
    try:
        vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
    except Exception as e:
        logger.error("Erro ao iniciar Vertex AI: %s", e)
# ============================================================================
#  ESTRATÉGIA DE NEGÓCIOS (GEOLOCALIZAÇÃO RJ)
# ============================================================================

ZONAS_RJ = [
    "na Zona Sul",
    "na Zona Oeste",
    "na Zona Norte",
    "na Zona Sudoeste",
    "na Barra da Tijuca",
    "no Recreio dos Bandeirantes",
    "no Jardim Oceânico",
    "em Copacabana"
]

# Ciclo de 5 dias (reinicia automaticamente)
_TEMAS_CICLO = [
    "Segurança Eletrônica (Câmeras e CFTV)",             # Dia 1
    "Elétrica e Máquinas de Automação",                  # Dia 2
    "Energia Solar Fotovoltaica Híbrida (Bateria Ongrid)",# Dia 3
    "Sistemas de Prevenção de Incêndio",                 # Dia 4
]
_DATA_REFERENCIA = datetime.date(2026, 3, 1)  # Marco zero do ciclo


def _tema_do_dia(hoje: datetime.date | None = None) -> str:
    hoje = hoje or datetime.date.today()
    dia_ciclo = (hoje - _DATA_REFERENCIA).days % len(_TEMAS_CICLO)
    return _TEMAS_CICLO[dia_ciclo]


TEMA_PARA_PASTA = {
    "Segurança Eletrônica (Câmeras e CFTV)": "cftv",
    "Elétrica e Máquinas de Automação": "automacao",
    "Energia Solar Fotovoltaica Híbrida (Bateria Ongrid)": "energia_solar",
    "Sistemas de Prevenção de Incêndio": "prevencao_incendio",
}

# Contatos regionais para CTA segmentado
CONTATOS_REGIAO = {
    "Zona Sul":      {"nome": "Adriana Vinni",   "whatsapp": "(21) 99006-8755"},
    "Vila Isabel":   {"nome": "Adriana Vinni",   "whatsapp": "(21) 99006-8755"},
    "Grajaú":        {"nome": "Adriana Vinni",   "whatsapp": "(21) 99006-8755"},
    "Zona Norte":    {"nome": "Márcia Ferreira", "whatsapp": "(21) 98348-9117"},
    "Zona Sudoeste": {"nome": "",                "whatsapp": "(21) 9647-2458"},
    "Zona Oeste":    {"nome": "",                "whatsapp": "(21) 9647-2458"},
}

CRONOGRAMA = [
    {"horario": "08:00", "tipo": "reels",  "descricao": "Reels matinal"},
    {"horario": "12:00", "tipo": "post",   "descricao": "Post intermediário"},
    {"horario": "16:00", "tipo": "story",  "descricao": "Story da tarde"},
    {"horario": "20:00", "tipo": "post",   "descricao": "Post noturno"},
]

# ============================================================================
#  GOOGLE DRIVE — BUSCA DE IMAGEM
# ============================================================================
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive"]


def _autenticar_google_drive():
    creds = None
    if GOOGLE_TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(
            str(GOOGLE_TOKEN_PATH), SCOPES_DRIVE)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not GOOGLE_CREDENTIALS_PATH.exists():
                logger.error("Arquivo credentials.json não encontrado.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                str(GOOGLE_CREDENTIALS_PATH), SCOPES_DRIVE)
            creds = flow.run_local_server(port=0)
        with open(GOOGLE_TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
    return build("drive", "v3", credentials=creds)


def _buscar_subpasta(service, pasta_raiz_id: str, nome_subpasta: str) -> str | None:
    query = f"'{pasta_raiz_id}' in parents and name = '{nome_subpasta}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    arquivos = results.get("files", [])
    return arquivos[0]["id"] if arquivos else None


def _listar_imagens_na_pasta(service, pasta_id: str) -> list[dict]:
    query = f"'{pasta_id}' in parents and (mimeType='image/jpeg' or mimeType='image/png' or mimeType='image/webp') and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get("files", [])


def _baixar_imagem(service, file_id: str, destino: pathlib.Path) -> pathlib.Path:
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    with open(destino, "wb") as f:
        f.write(fh.getvalue())
    return destino


def buscar_imagem_drive(tema: str) -> pathlib.Path | None:
    if not GOOGLE_DRIVE_FOLDER_ID:
        return None
    service = _autenticar_google_drive()
    if not service:
        return None
    slug = TEMA_PARA_PASTA.get(tema, "")
    pasta_id = _buscar_subpasta(service, GOOGLE_DRIVE_FOLDER_ID, slug)
    if not pasta_id:
        return None
    imagens = _listar_imagens_na_pasta(service, pasta_id)
    if not imagens:
        return None
    escolhida = random.choice(imagens)
    extensao = escolhida["name"].rsplit(
        ".", 1)[-1] if "." in escolhida["name"] else "jpg"
    destino = TMP_DIR / f"drive_{slug}_{escolhida['id']}.{extensao}"
    if destino.exists():
        return destino
    return _baixar_imagem(service, escolhida["id"], destino)

# ============================================================================
#  GERAÇÃO DE IMAGEM POR IA (Vertex AI - Imagen 3)
# ============================================================================


def gerar_imagem_ia(prompt: str) -> pathlib.Path | None:
    """
    Usa o Imagen 3 do Vertex AI corporativo (Service Account Json) para gerar
    uma imagem sintética de alta qualidade, caso não tenha fotos da obra no dia.
    """
    print(f"\n[*] Solicitando imagem a Fabrica de Imagens (Imagen 3)...")
    print(f"    Prompt Base: '{prompt}'")

    # Prompt de engenharia corporativa infalível
    prompt_completo = (
        f"Professional corporate photography for an engineering and facility management company "
        f"named DL Solucoes Condominiais. "
        f"Context: {prompt}. "
        f"Focus highly on technical aspects requested: if security, show modern cameras/CCTV. "
        f"If electricity, show automation machines and clean panels. "
        f"If solar, strictly show Hybrid Photovoltaic Panels with Ongrid Battery systems. "
        f"Ultra-realistic, 4k resolution, cinematic lighting, modern technology focus, "
        f"clean aesthetic, no text or logos in the image."
    )

    caminho_imagem = os.path.join(TMP_DIR, "imagem_ia_temp.png")

    try:
        modelo = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

        imagens = modelo.generate_images(
            prompt=prompt_completo,
            number_of_images=1,
            aspect_ratio="1:1"
        )

        if imagens:
            # Converte a string do caminho do arquivo gerado pelo os.path para objeto Path
            caminho_final = pathlib.Path(caminho_imagem)
            imagens[0].save(location=str(caminho_final))
            print("    [!] A Imagem foi gerada e salva com extrema precisao pelo Imagen 3!")
            return caminho_final
        else:
             print("    [!] A IA nao retornou nenhuma imagem.")
             return None

    except Exception as e:
        print(f"    [X] Falha massiva ao gerar a imagem no Vertex: {e}")
        return None


# ============================================================================
#  FALLBACK: FOTO STOCK (Pexels - Gratuito)
# ============================================================================

_TEMA_PARA_BUSCA = {
    "Seguran\u00e7a Eletr\u00f4nica (CFTV, Interfonia)": "cctv security camera building",
    "El\u00e9trica e Energia Geral": "electrical panel condominium",
    "Energia Solar H\u00edbrida e Carports": "solar panel rooftop building",
    "Sistemas de Preven\u00e7\u00e3o de Inc\u00eandio": "fire alarm sprinkler building",
}


def buscar_imagem_stock(tema: str) -> pathlib.Path | None:
    """Busca foto real: Pexels (com key) ou Picsum (sempre funciona)."""
    query = _TEMA_PARA_BUSCA.get(tema, "modern condominium technology")
    slug = TEMA_PARA_PASTA.get(tema, "geral")
    cache = TMP_DIR / f"stock_{slug}.jpg"
    if cache.exists():
        logger.info("Usando imagem stock em cache: %s", cache.name)
        return cache
    try:
        pexels_key = os.getenv("PEXELS_API_KEY", "")
        if pexels_key:
            # Pexels com API key (fotos de alta qualidade tematicas)
            resp = requests.get(
                "https://api.pexels.com/v1/search",
                headers={"Authorization": pexels_key},
                params={"query": query, "per_page": 5,
                        "orientation": "square"},
                timeout=15,
            ).json()
            photos = resp.get("photos", [])
            if photos:
                foto = random.choice(photos)
                img_data = requests.get(
                    foto["src"]["large2x"], timeout=30).content
                with open(cache, "wb") as f:
                    f.write(img_data)
                logger.info("Imagem stock Pexels: %s", cache.name)
                return cache

        # Fallback garantido: Picsum (sempre funciona, foto real)
        resp = requests.get("https://picsum.photos/1080/1080",
                            timeout=20, allow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(cache, "wb") as f:
                f.write(resp.content)
            logger.info("Imagem stock Picsum: %s", cache.name)
            return cache
        return None
    except Exception as e:
        logger.error("Erro stock photo: %s", e)
        return None


# ============================================================================
#  REELS: CRIACAO DE VIDEO COM FFMPEG
# ============================================================================

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()


def criar_reel_video(
    imagem_path: pathlib.Path,
    copy_text: str,
    tema: str,
    duracao: int = 10,
) -> pathlib.Path | None:
    """Cria video Reel (MP4) a partir de imagem com efeito Ken Burns e texto."""
    slug = TEMA_PARA_PASTA.get(tema, "geral")
    video_path = TMP_DIR / \
        f"reel_{slug}_{datetime.date.today().isoformat()}.mp4"

    try:
        # 1. Prepara imagem base (1080x1080 pra feed quadrado ou 1080x1920 pra Reels)
        img = Image.open(imagem_path).convert("RGB")
        # Redimensiona para 1080x1920 (formato Reels vertical)
        img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
        # Cria canvas vertical 1080x1920 com fundo escuro
        canvas = Image.new("RGB", (1080, 1920), (15, 15, 25))
        # Coloca a imagem no topo
        canvas.paste(img, (0, 100))

        # 2. Adiciona texto do copy na parte inferior
        draw = ImageDraw.Draw(canvas)
        # Tenta usar fonte do sistema, senao usa padrao
        try:
            font = ImageFont.truetype("arial.ttf", 32)
            font_title = ImageFont.truetype("arialbd.ttf", 40)
        except OSError:
            font = ImageFont.load_default()
            font_title = font

        # Titulo: DL Solucoes
        draw.text((40, 1220), "DL Solucoes Condominiais",
                  fill=(0, 200, 255), font=font_title)

        # Copy (truncado para caber)
        linhas_copy = copy_text[:300].split("\n")
        y_pos = 1290
        for linha in linhas_copy[:6]:
            # Quebra linhas longas
            while len(linha) > 45:
                draw.text((40, y_pos), linha[:45],
                          fill=(230, 230, 230), font=font)
                y_pos += 40
                linha = linha[45:]
            draw.text((40, y_pos), linha, fill=(230, 230, 230), font=font)
            y_pos += 40
            if y_pos > 1850:
                break

        # CREA
        draw.text((40, 1870), "CREA-RJ: 2022106230",
                  fill=(120, 120, 120), font=font)

        # Salva frame base
        frame_path = TMP_DIR / f"_frame_{slug}.png"
        canvas.save(str(frame_path), quality=95)

        # 3. Usa ffmpeg para criar video com zoom suave (Ken Burns)
        # Zoom de 1.0 para 1.08 em {duracao} segundos
        cmd = [
            FFMPEG_EXE, "-y",
            "-loop", "1",
            "-i", str(frame_path),
            "-vf", f"zoompan=z='min(zoom+0.001,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={duracao*30}:s=1080x1920:fps=30",
            "-t", str(duracao),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-crf", "23",
            str(video_path),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            logger.error("ffmpeg stderr: %s", result.stderr[-500:])
            return None

        # Limpa frame temporario
        frame_path.unlink(missing_ok=True)

        logger.info("Reel criado: %s (%.1f MB)", video_path.name,
                    video_path.stat().st_size / 1024 / 1024)
        return video_path

    except Exception as e:
        logger.error("Erro ao criar Reel: %s", e)
        return None

# ============================================================================
#  CRIAÇÃO DE COPY E REVISÃO IMPLACÁVEL (O CÉREBRO)
# ============================================================================


def gerar_copy(tema: str, tipo_post: str, zona_alvo: str) -> str:
    if not gemini_client:
        logger.warning("Gemini client nao configurado. Usando copy padrao.")
        return f"Problemas com {tema}? Solicite uma Avaliacao Tecnica com a DL Solucoes. WhatsApp. CREA-RJ: 2022106230"

    # Busca contato regional para o CTA
    contato_info = ""
    for regiao, dados in CONTATOS_REGIAO.items():
        if regiao.lower() in zona_alvo.lower():
            nome = f" - {dados['nome']}" if dados['nome'] else ""
            contato_info = f"WhatsApp: {dados['whatsapp']}{nome}"
            break
    if not contato_info:
        contato_info = "WhatsApp: (21) 9647-2458"

    formatos = {
        "reels": "legenda curta e impactante para Reels (maximo 150 caracteres + hashtags)",
        "post": "legenda completa e persuasiva para Post no feed (3 paragrafos com CTA forte)",
        "story": "texto curto e direto para Story com CTA (maximo 100 caracteres + emoji)",
    }
    formato_instrucao = formatos.get(tipo_post, formatos["post"])

    system_prompt = dedent(f"""\
        Voce eh o Head de Vendas e Agente de Social Media da DL Solucoes Condominiais.
        O seu foco eh fechar contratos B2B de alto valor no Rio de Janeiro.

        REGRAS INEGOCIAVEIS E OBRIGATORIAS:
        1. PUBLICO: Chame a atencao de Sindicos e Administradoras de Condominios logo na primeira linha.
        2. LOCALIZACAO: Fale diretamente com condominios localizados {zona_alvo}.
        3. PALAVRA PROIBIDA: NUNCA use o termo "visita tecnica". Use SEMPRE "Avaliacao Tecnica".
        4. CTA OBRIGATORIO: Termine o texto ordenando uma acao. Inclua o contato: {contato_info}
        5. ASSINATURA: O texto DEVE terminar exatamente com a frase: "Responsabilidade Tecnica CREA-RJ: 2022106230".
        6. TOM: Profissional, solido, empresarial e focado na resolucao de problemas criticos.
    """)

    user_prompt = f"Crie uma {formato_instrucao} vendendo o servico de {tema}."

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{system_prompt}\n\n{user_prompt}",
        )
        return response.text.strip()
    except Exception as e:
        logger.error("Erro Gemini: %s", e)
        return f"Problemas com {tema}? Solicite uma Avaliacao Tecnica com a DL Solucoes. WhatsApp. CREA-RJ: 2022106230"


def revisor_implacavel(texto: str) -> tuple[bool, str]:
    """Auditoria de qualidade anti-falhas antes de postar."""
    txt_lower = texto.lower()

    if "visita técnica" in txt_lower or "visita tecnica" in txt_lower:
        return False, "Uso da palavra proibida 'visita técnica'."
    if "avaliação técnica" not in txt_lower and "avaliacao tecnica" not in txt_lower:
        return False, "Faltou exigir a 'Avaliação Técnica' no CTA."
    if "síndico" not in txt_lower and "sindico" not in txt_lower and "administradora" not in txt_lower:
        return False, "Não focou no público alvo (Síndicos/Administradoras)."
    if "crea-rj" not in txt_lower:
        return False, "Faltou a assinatura de Responsabilidade Técnica do CREA."

    return True, "Validado."

# ============================================================================
#  PUBLICAÇÃO OMNICHANNEL (INSTAGRAM + FACEBOOK)
# ============================================================================


def _upload_imagem_para_url(imagem_path: pathlib.Path) -> str | None:
    url = f"{META_GRAPH_URL}/{META_PAGE_ID}/photos"
    try:
        with open(imagem_path, "rb") as img_file:
            response = requests.post(url, files={"source": img_file}, data={
                                     "published": "false", "access_token": META_ACCESS_TOKEN}, timeout=120)
        data = response.json()
        if "id" in data:
            photo_url_resp = requests.get(f"{META_GRAPH_URL}/{data['id']}", params={
                                          "fields": "images", "access_token": META_ACCESS_TOKEN}, timeout=30).json()
            images = photo_url_resp.get("images", [])
            if images:
                return images[0]["source"]
        return None
    except Exception as e:
        logger.error("Erro no upload para url publica do FB: %s", e)
        return None


def publicar_no_instagram(media_url_or_path, caption: str, tipo: str = "post", is_video: bool = False) -> bool:
    media_url = f"{META_GRAPH_URL}/{INSTAGRAM_ACCOUNT_ID}/media"

    if is_video and tipo == "reels":
        # Publica como Reel (video)
        media_params = {
            "video_url": media_url_or_path,
            "caption": caption,
            "media_type": "REELS",
            "access_token": META_ACCESS_TOKEN,
        }
    else:
        media_params = {
            "image_url": media_url_or_path,
            "caption": caption,
            "access_token": META_ACCESS_TOKEN,
        }
        if tipo == "story":
            media_params["media_type"] = "STORIES"

    try:
        response = requests.post(
            media_url, data=media_params, timeout=60).json()
        if "id" not in response:
            logger.warning("IG media response: %s", response)
            return False

        # Video demora mais para processar
        wait_time = 30 if is_video else 5
        time.sleep(wait_time)

        pub_url = f"{META_GRAPH_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        pub_response = requests.post(
            pub_url,
            data={"creation_id": response["id"],
                  "access_token": META_ACCESS_TOKEN},
            timeout=60,
        ).json()
        return "id" in pub_response
    except Exception as e:
        logger.error("Erro publicar IG: %s", e)
        return False


def publicar_no_facebook(media_path: pathlib.Path, caption: str, is_video: bool = False) -> bool:
    if is_video:
        url = f"{META_GRAPH_URL}/{META_PAGE_ID}/videos"
        try:
            with open(media_path, "rb") as vid_file:
                response = requests.post(
                    url,
                    files={"source": vid_file},
                    data={"description": caption, "published": "true",
                          "access_token": META_ACCESS_TOKEN},
                    timeout=300,
                ).json()
            return "id" in response
        except Exception as e:
            logger.error("Erro publicar FB video: %s", e)
            return False
    else:
        url = f"{META_GRAPH_URL}/{META_PAGE_ID}/photos"
        try:
            with open(media_path, "rb") as img_file:
                response = requests.post(
                    url,
                    files={"source": img_file},
                    data={"message": caption, "published": "true",
                          "access_token": META_ACCESS_TOKEN},
                    timeout=120,
                ).json()
            return "id" in response or "post_id" in response
        except Exception as e:
            logger.error("Erro publicar FB foto: %s", e)
            return False

# ============================================================================
#  ORQUESTRAÇÃO E FEEDBACK LOOP
# ============================================================================


def salvar_plano_diario(tema: str, postagens: list[dict]):
    hoje = datetime.date.today()
    linhas = [
        f"# 📋 Plano Diário B2B — DL Soluções Condominiais",
        f"**Data:** {hoje.strftime('%d/%m/%Y')} | **Tema:** {tema}\n---",
        f"| # | Horário | Tipo | Status |",
        f"|---|---------|------|--------|"
    ]
    for i, p in enumerate(postagens, 1):
        linhas.append(
            f"| {i} | {p['horario']} | {p['tipo'].upper()} | {p.get('status', '⏳ Pendente')} |")

    caminho = TMP_DIR / "plano_diario.md"
    caminho.write_text("\n".join(linhas), encoding="utf-8")
    return caminho


def executar_postagem(tema: str, slot: dict) -> dict:
    tipo = slot["tipo"]
    zona_alvo = random.choice(ZONAS_RJ)
    logger.info("=" * 60)
    logger.info("Executando: %s -- Foco: %s (%s)",
                slot["horario"], zona_alvo, tema)

    # 1. Cadeia de fallback de imagem: Drive -> Gemini IA -> Stock photo
    imagem_local = buscar_imagem_drive(tema)
    if not imagem_local:
        logger.info("Drive vazio, tentando Gemini IA...")
        imagem_local = gerar_imagem_ia(tema)
    if not imagem_local:
        logger.info("Gemini IA falhou, tentando foto stock...")
        imagem_local = buscar_imagem_stock(tema)
    if not imagem_local:
        slot["status"] = "Falha (Sem imagem)"
        return slot

    logger.info("Imagem obtida: %s", imagem_local.name)

    # 2. Copy + Revisor Implacavel (Max 3 tentativas)
    max_tentativas = 3
    copy_final = ""
    for tentativa in range(1, max_tentativas + 1):
        copy_temp = gerar_copy(tema, tipo, zona_alvo)
        aprovado, motivo = revisor_implacavel(copy_temp)
        if aprovado:
            copy_final = copy_temp
            logger.info(
                "Copy Aprovada pelo Revisor (Tentativa %d).", tentativa)
            break
        else:
            logger.warning(
                "Revisor Barrou (Tentativa %d). Motivo: %s", tentativa, motivo)
            if tentativa == max_tentativas:
                copy_final = copy_temp

    logger.info("COPY:\n%s\n", copy_final)

    # 3. Se for Reels, criar video a partir da imagem
    is_video = False
    media_local = imagem_local
    if tipo == "reels":
        video_path = criar_reel_video(imagem_local, copy_final, tema)
        if video_path:
            media_local = video_path
            is_video = True
            logger.info("Reel em video criado com sucesso!")
        else:
            logger.warning("Falha ao criar video, publicando como imagem.")

    # 4. Disparo Omnichannel
    image_url = _upload_imagem_para_url(imagem_local)

    if is_video:
        # Quando é Reels (Video)
        pub_ig = publicar_no_instagram(
            media_local, copy_final, tipo="reels", is_video=True)
        # Atenção: Facebook Video Graph API usa 'source' com path local binário.
        pub_fb = publicar_no_facebook(media_local, copy_final, is_video=True)
    else:
        # Quando é Imagem Estática / Story
        pub_ig = publicar_no_instagram(
            image_url, copy_final, tipo=tipo, is_video=False) if image_url else False
        pub_fb = publicar_no_facebook(imagem_local, copy_final, is_video=False)

    if pub_ig and pub_fb:
        slot["status"] = "IG + FB"
    elif pub_ig:
        slot["status"] = "So IG"
    elif pub_fb:
        slot["status"] = "So FB"
    else:
        slot["status"] = "Falhou"

    return slot


def main():
    hoje = datetime.date.today()
    tema = _tema_do_dia(hoje)
    postagens = [dict(s) for s in CRONOGRAMA]

    if len(sys.argv) > 1 and sys.argv[1] == "--executar":
        for i, slot in enumerate(postagens):
            postagens[i] = executar_postagem(tema, slot)
            if i < len(postagens) - 1:
                logger.info(
                    "Aguardando 30s antes do proximo slot (anti-rate-limit)...")
                time.sleep(30)
    elif len(sys.argv) > 2 and sys.argv[1] == "--slot":
        slot_num = int(sys.argv[2])
        postagens[slot_num -
                  1] = executar_postagem(tema, postagens[slot_num - 1])
    else:
        logger.info("Modo: Planejamento. Use --slot N para rodar.")

    salvar_plano_diario(tema, postagens)

    print(f"\n{'=' * 40}\nRESUMO: {tema}\n{'=' * 40}")
    for i, p in enumerate(postagens, 1):
        print(
            f"[{i}] {p['horario']} | {p['tipo'].upper():5s} | {p.get('status', '⏳ Pendente')}")


if __name__ == "__main__":
    main()
