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

CREATE TABLE IF NOT EXISTS dl_nexus_execution_state (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id TEXT NOT NULL,
  step_name TEXT NOT NULL,
  status TEXT NOT NULL, -- 'pending', 'in_progress', 'completed', 'failed'
  input_hash TEXT, -- MD5 do input para detectar mudancas
  output_data JSONB,
  tokens_used INTEGER DEFAULT 0,
  execution_time_ms INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workflow_step ON dl_nexus_execution_state(workflow_id, step_name);
CREATE INDEX IF NOT EXISTS idx_input_hash ON dl_nexus_execution_state(input_hash);

CREATE TABLE IF NOT EXISTS dl_nexus_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_name TEXT NOT NULL,
  execution_id TEXT,
  metric_type TEXT NOT NULL,
  metric_value NUMERIC NOT NULL,
  unit TEXT,
  timestamp TIMESTAMP DEFAULT NOW(),
  tags JSONB
);

CREATE TABLE IF NOT EXISTS dl_dead_letter_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_workflow TEXT NOT NULL,
  execution_id TEXT,
  error_message TEXT NOT NULL,
  error_stack TEXT,
  input_payload JSONB,
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,
  created_at TIMESTAMP DEFAULT NOW(),
  resolved_at TIMESTAMP,
  resolution_notes TEXT
);

CREATE TABLE IF NOT EXISTS dl_feature_flags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  flag_name TEXT UNIQUE NOT NULL,
  enabled BOOLEAN DEFAULT false,
  description TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO dl_feature_flags (flag_name, enabled, description)
VALUES
  ('ENABLE_RAG', false, 'Ativa motor RAG global'),
  ('ENABLE_VIDEO', false, 'Ativa gerador de video para mkt'),
  ('ENABLE_LINKEDIN', false, 'Ativa publicacao automatica linkedin')
ON CONFLICT (flag_name) DO NOTHING;
