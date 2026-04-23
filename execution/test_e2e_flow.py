#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================================
  test_e2e_flow.py — Simulador de Tiro Real (End-to-End) para DL Nexus
==========================================================================
Propósito: Validar a resiliência do Webhook Receptor (n8n), roteamento
da IA e salvamento no Supabase ANTES da produção oficial.
"""

import requests
import json
import time

# ============================================================================
# CONFIGURAÇÕES DE TESTE (Alvo: n8n hospedado na HostGator)
# ============================================================================
N8N_WEBHOOK_URL = "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-receptor"
# Substituir em produção pela chave real
API_KEY_TESTE = "TESTE-123-CHAVE-CADASTRADA-NO-N8N"

print("==========================================================")
print("🚀 INICIANDO TESTE END-TO-END (DL NEXUS / WHATSAPP)")
print("==========================================================")
print(f"🎯 Alvo: {N8N_WEBHOOK_URL}")

# ============================================================================
# PAYLOAD SIMULADO: META WHATSAPP (JSON EXATO DA API OFICIAL)
# ============================================================================
payload_mock = {
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "1234567890",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "5521990068755",
              "phone_number_id": "1234567890"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Síndico Roberto (Ed. Golden Blue)"
                },
                "wa_id": "5521999999999"
              }
            ],
            "messages": [
              {
                "from": "5521999999999",
                "id": "wamid.HBgLNTU1MjEyMjI2MzQyFQIAEhgUM0E0Qjg0NjVFMEMwRDExOThDQ0Q=",
                "timestamp": str(int(time.time())),
                "text": {
                  "body": "Bom dia, sou o síndico do Condomínio Golden Blue. Preciso de uma empresa séria para reformar nossa guarita com controle de acesso facial e consertar nosso painel elétrico principal. A conta de luz da bomba também está vindo absurda, acho que precisamos de Energia Solar nas áreas comuns. Podem agendar uma Avaliação Técnica urgente?"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}

# ============================================================================
# DISPARO DO MÍSSIL E ANÁLISE DO RESULTADO
# ============================================================================
headers = {
    "Content-Type": "application/json",
    "X-DL-API-KEY": API_KEY_TESTE  # HeaderAuth Blindado
}

print(f"\n📦 Payload montado: Síndico Roberto (Demanda: CFTV, Elétrica, Solar)")
print(f"📡 Disparando POST para o Webhook n8n...")

try:
    response = requests.post(
        N8N_WEBHOOK_URL,
        json=payload_mock,
        headers=headers,
        timeout=15
    )

    status_code = response.status_code
    print(f"\n==========================================================")

    if status_code == 200 or status_code == 201:
        print(f"✅ SUCESSO! [HTTP {status_code}]")
        print(f"   A Aninha (Triagem IA) recebeu a mensagem e repassou para o roteador.")
        print(f"   Próximo Passo: Verificar o Supabase se o Lead apareceu na tabela 'leads'.")
    elif status_code == 401 or status_code == 403:
        print(f"❌ BLOQUEADO! [HTTP {status_code}]")
        print(f"   A blindagem do n8n funcionou e recusou a credencial X-DL-API-KEY (ou não está configurada).")
    elif status_code == 404:
        print(f"❌ NÃO ENCONTRADO [HTTP {status_code}]")
        print(f"   O Webhook não está ativo ou a URL mudou na HostGator.")
    else:
        print(f"⚠️ RESULTADO INESPERADO [HTTP {status_code}]")
        print(f"   Resposta: {response.text}")

    print("==========================================================")

except requests.exceptions.ConnectionError:
    print(f"\n❌ ERRO DE CONEXÃO: Não foi possível alcançar o servidor HostGator.")
    print(f"   Verifique se o container do n8n está rodando (docker ps).")
except requests.exceptions.Timeout:
    print(f"\n❌ TIMEOUT: O servidor demorou mais de 15 segundos para responder.")
except Exception as e:
    print(f"\n❌ ERRO CRÍTICO NO SIMULADOR: {e}")
