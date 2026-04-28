# n8n Rescue Protocol

This document contains the emergency CLI commands to extract workflows and reset the owner account for a Docker Compose-based n8n deployment.

## 1. Locate the container
From the directory containing your `docker-compose.yml` (likely `backend/n8n` based on the config):
```bash
docker-compose ps
```
Or universally to find the n8n container ID/name:
```bash
docker ps | grep n8n
```

## 2. EXPORT ALL WORKFLOWS (CRITICAL BACKUP)
Execute this command to dump all workflows from the n8n database into a JSON file safely inside the container, then copy it to your host machine. Assuming your container is named `n8n-n8n-1` or `n8n` (adjust `n8n` below to your container name from step 1 if different):

```bash
# Execute the export inside the container and output to stdout, redirecting to a file on your host machine
docker exec -it n8n n8n export:workflow --all > n8n_workflows_emergency_backup.json
```
*Verify the file size and content of `n8n_workflows_emergency_backup.json` before proceeding to ensure it's not empty.*

## 3. Reset the Owner Account
Once the backup is secured, reset the user management system. This will force n8n to ask you to set up a new Owner account upon next web UI access.

```bash
docker exec -it n8n n8n user-management:reset
```

After running this, restart the container to ensure clean state:
```bash
docker restart n8n
```

Then access your web interface (`https://n8n.dlsolucoescondominiais.com.br`) and register the new owner account immediately.
