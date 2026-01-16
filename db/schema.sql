CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS agents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  hostname TEXT NOT NULL,
  os_type TEXT NOT NULL,
  os_version TEXT NOT NULL,
  api_key_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS logs (
  id BIGSERIAL PRIMARY KEY,
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  log_source TEXT NOT NULL,
  event_time TIMESTAMP NOT NULL,
  received_at TIMESTAMP NOT NULL DEFAULT NOW(),
  event_level TEXT NOT NULL,
  event_id TEXT NOT NULL,
  message TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_logs_agent_id ON logs (agent_id);
CREATE INDEX IF NOT EXISTS idx_logs_event_time ON logs (event_time);
CREATE INDEX IF NOT EXISTS idx_logs_event_level ON logs (event_level);
