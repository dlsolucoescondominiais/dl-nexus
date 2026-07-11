import subprocess

def check_workflow_status():
    try:
        result = subprocess.run(['n8n', 'workflow', 'list'], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print('Erros:', result.stderr)
    except Exception as e:
        print('Falha ao rodar comando n8n:', str(e))

check_workflow_status()
