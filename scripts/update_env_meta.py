import os

env_path = r'd:\AntiGravity\projeto_01\.env'
new_token = os.environ.get('META_PAGE_ACCESS_TOKEN_DL')
new_secret = "db2b2cbb91193147c82913d5dca5cb8f"

lines = []
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

token_found = False
secret_found = False

new_lines = []
for line in lines:
    if line.startswith('META_TOKEN='):
        new_lines.append(f'META_TOKEN={new_token}\n')
        token_found = True
    elif line.startswith('META_APP_SECRET='):
        new_lines.append(f'META_APP_SECRET={new_secret}\n')
        secret_found = True
    else:
        new_lines.append(line)

if not token_found:
    new_lines.append(f'META_TOKEN={new_token}\n')
if not secret_found:
    new_lines.append(f'META_APP_SECRET={new_secret}\n')

with open(env_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ .env updated successfully.")
