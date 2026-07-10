CREATE TABLE IF NOT EXISTS dl_nexus_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    active BOOLEAN DEFAULT FALSE,
    last_status VARCHAR(50),
    last_execution_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dl_nexus_agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id VARCHAR(255),
    action VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dl_nexus_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_name VARCHAR(255) NOT NULL,
    credential_type VARCHAR(50) NOT NULL,
    expiration_date TIMESTAMP WITH TIME ZONE,
    authorized_scopes JSONB,
    workflows_using JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dl_nexus_workflows_id ON dl_nexus_workflows(workflow_id);
CREATE INDEX IF NOT EXISTS idx_dl_nexus_agent_logs_workflow ON dl_nexus_agent_logs(workflow_id);
