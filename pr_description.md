🔒 [Security Fix] Remove Hardcoded N8N API Keys

🎯 **What:** The vulnerability fixed
Hardcoded JSON Web Tokens (JWT) for the N8N API were present in `import_091_092_n8n.py` and `import_social_media_n8n.py`. These have been removed and replaced with environment variable loading.

⚠️ **Risk:** The potential impact if left unfixed
An attacker gaining access to the codebase would have immediate, unauthorized access to the production N8N API via the hardcoded JWT token, allowing them to manipulate workflows or access sensitive data.

🛡️ **Solution:** How the fix addresses the vulnerability
The hardcoded strings were removed. The scripts now fetch the token securely at runtime using `os.environ.get('N8N_API_KEY')`. This prevents credentials from being exposed in source control.
