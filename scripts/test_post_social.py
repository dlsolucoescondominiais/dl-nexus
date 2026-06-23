import argparse
import sys
import json
import time

def main():
    parser = argparse.ArgumentParser(description="Automação de Postagens DL Nexus V3")
    parser.add_argument("--platform", required=True, choices=["tiktok", "gmb"], help="Plataforma alvo")
    parser.add_argument("--text", required=True, help="Texto da postagem")
    parser.add_argument("--media", required=False, help="Caminho da mídia ou URL", default="")
    args = parser.parse_args()

    # Log de execução simulando conexão
    print(f"[INFO] Conectando à plataforma {args.platform.upper()}...", file=sys.stderr)
    time.sleep(1) # Simula delay de rede

    if args.platform == "tiktok":
        print(f"[INFO] Validando tokens do TikTok...", file=sys.stderr)
        # Mock de postagem no TikTok
        result = {
            "status": "success",
            "platform": "tiktok",
            "post_id": f"tt_{int(time.time())}",
            "message": "Postagem no TikTok realizada com sucesso via DL Nexus Automação (Mock)",
            "url": f"https://www.tiktok.com/@dl_solucoes/video/{int(time.time())}",
            "text_posted": args.text
        }
    elif args.platform == "gmb":
        print(f"[INFO] Validando credenciais do Google Business Profile...", file=sys.stderr)
        # Mock de postagem no GMB
        result = {
            "status": "success",
            "platform": "gmb",
            "post_id": f"gmb_{int(time.time())}",
            "message": "Postagem no Google Business Profile realizada com sucesso via DL Nexus Automação (Mock)",
            "url": f"https://business.google.com/posts/l/0123456789/{int(time.time())}",
            "text_posted": args.text
        }
    else:
        print(json.dumps({"status": "error", "message": "Plataforma inválida."}))
        sys.exit(1)

    print(f"[INFO] Postagem confirmada. ID: {result['post_id']}", file=sys.stderr)
    
    # Retorna o JSON limpo na saída padrão para o n8n
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
