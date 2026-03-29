import os
import requests
from typing import Dict, Any

class AgenteCartografo:
    """
    Microsserviço leve (sem LLM pesada) dedicado exclusivamente à 
    Geolocalização, Distância e Cálculo de Custo de Deslocamento da DL Soluções.
    Isola a logística, impedindo que a 'Aninha' perca tempo calculando rotas.
    """
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        # Coordenadas fixas da DL Soluções Condominiais (Extraídas do iframe do cliente)
        self.origem_dl = "-22.9977654,-43.3806414"
        
    def calcular_viabilidade(self, endereco_lead: str) -> Dict[str, Any]:
        """
        Calcula o trajeto via Google Maps API e retorna a Matriz Operacional.
        """
        if not self.api_key:
            return {"status": "erro", "distancia_km": 0, "msg": "API_KEY do Google Ausente ou Inválida."}

        # Utilizamos a Distance Matrix por ser mais exata que a rota de ponta-a-ponta simples
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": self.origem_dl,
            "destinations": endereco_lead,
            "key": self.api_key,
            "language": "pt-BR"
        }
        
        try:
            resp = requests.get(url, params=params)
            data = resp.json()
            
            if data.get("status") == "OK":
                elemento = data["rows"][0]["elements"][0]
                
                if elemento.get("status") == "OK":
                    distancia_mts = elemento["distance"]["value"]
                    dist_km = round(distancia_mts / 1000, 1)
                    tempo_viagem = elemento["duration"]["text"]
                    
                    # -------------------------------------------------------------
                    # MATRIZ DE VIABILIDADE TÉCNICA E CUSTO DLSOLUCOES
                    # -------------------------------------------------------------
                    if dist_km <= 25.0:
                        status_viabilidade = "VERDE"
                        taxa_deslocamento = 0.0
                        aviso = f"Proximidade excelente ({dist_km}km). Viagem em {tempo_viagem}. Visita Técnica Gratuita autorizada."
                        
                    elif dist_km <= 60.0:
                        status_viabilidade = "AMARELO"
                        taxa_deslocamento = 180.0 # Sugestão de Custo Operacional (Pedágio + Gasolina)
                        aviso = f"Distância média ({dist_km}km). Viagem de {tempo_viagem}. Sugerir Taxa de Visita (R$180)."
                        
                    else:
                        status_viabilidade = "VERMELHO (FORA_DE_RAIO)"
                        taxa_deslocamento = 350.0
                        aviso = f"ALERTA: Escopo fora da região nativa ({dist_km}km - Aprox {tempo_viagem} de viagem). Repassar apenas projetos Premium ou com Taxa de Deslocamento alta."
                        
                    return {
                        "status": "sucesso",
                        "farol_viabilidade": status_viabilidade,
                        "distancia_km": dist_km,
                        "tempo_estimado": tempo_viagem,
                        "custo_sugerido_viagem": taxa_deslocamento,
                        "parecer_logistico": aviso
                    }
                else:
                    return {"status": "erro", "distancia_km": 0, "msg": "CEP / Endereço não mapeável."}
            else:
                return {"status": "erro", "distancia_km": 0, "msg": f"Google Api Error: {data.get('error_message', 'Desconhecido')}"}
                
        except Exception as e:
            return {"status": "erro", "distancia_km": 0, "msg": f"HTTP Falha: {str(e)}"}
