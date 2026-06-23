import json

# Mock Data Provided by Supabase Query Match
mock_files = [
    {
        "id": "item1",
        "file_id": "file123",
        "pasta_origem_id": "folder_A",
        "pasta_destino_id": "folder_B",
        "status": "aprovado_para_mover",
        "acao_aprovada": "mover",
        "precisa_revisao_humana": False
    },
    {
        "id": "item2",
        "file_id": "file456",
        "pasta_origem_id": "folder_A",
        "pasta_destino_id": "folder_A", # Bloqueado
        "status": "aprovado_para_mover",
        "acao_aprovada": "mover",
        "precisa_revisao_humana": False
    },
    {
        "id": "item3",
        "file_id": "file789",
        "pasta_origem_id": "folder_A",
        "pasta_destino_id": "folder_C",
        "status": "pendente", # Bloqueado
        "acao_aprovada": "mover",
        "precisa_revisao_humana": False
    }
]

def simulate_n8n_zelador_execution(files, dry_run=True):
    print(f"--- INICIANDO ZELADOR EXECUTOR (DRY_RUN={dry_run}) ---")
    resultados = {
        "analisados": 0,
        "movidos": 0,
        "dry_run": 0,
        "bloqueados": 0,
        "erros": 0
    }
    
    for item in files:
        resultados["analisados"] += 1
        print(f"\nItem: {item['id']}")
        bloqueado = False
        motivo = ""
        
        if item['pasta_origem_id'] == item['pasta_destino_id']:
            bloqueado = True
            motivo = "Origem igual destino"
        elif not item.get('file_id') or not item.get('pasta_origem_id') or not item.get('pasta_destino_id'):
            bloqueado = True
            motivo = "IDs ausentes"
        elif item.get('acao_aprovada') != 'mover':
            bloqueado = True
            motivo = "Acao diferente de mover"
        elif item.get('status') != 'aprovado_para_mover':
            bloqueado = True
            motivo = "Status invalido"
        elif item.get('precisa_revisao_humana'):
            bloqueado = True
            motivo = "Revisao humana pendente"
            
        if bloqueado:
            print(f"BLOQUEADO: {motivo}")
            resultados["bloqueados"] += 1
            # Update supabase to erro_movimentacao
            print("Supabase Update: status='erro_movimentacao'")
            continue
            
        if dry_run:
            print("DRY RUN: PATCH bloqueado com sucesso.")
            resultados["dry_run"] += 1
            print("Supabase Update: status='dry_run_movimento_validado'")
        else:
            print(f"PATCH /drive/v3/files/{item['file_id']}?addParents={item['pasta_destino_id']}&removeParents={item['pasta_origem_id']}")
            resultados["movidos"] += 1
            print("Supabase Update: status='movido'")
            
    print(f"\nResumo: {resultados}")

simulate_n8n_zelador_execution(mock_files, dry_run=True)
