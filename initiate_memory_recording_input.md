# Learnings from n8n Workflow Deployment
- When deploying workflows dynamically to n8n via its API (`POST /workflows`), setting the workflow payload key `settings` to `{"saveExecutionProgress": True, "saveManualExecutions": True}` is sometimes strictly required by the n8n API, otherwise it may reject the payload with `request/body must have required property 'settings'`.
- Scripts containing hardcoded secrets used for API interactions must be deleted or scrubbed immediately after use before committing any git state to prevent repository leaks.
