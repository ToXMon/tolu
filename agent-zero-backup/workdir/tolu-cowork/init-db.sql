-- Tolu Cowork — Database Initialization
-- Creates tables for persistent project storage

BEGIN;

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    name VARCHAR(255) PRIMARY KEY,
    path TEXT NOT NULL,
    description TEXT,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_opened_at TIMESTAMPTZ DEFAULT NOW(),
    session_count INTEGER DEFAULT 0
);

-- Audit log table (persistent storage beyond JSONL)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    actor VARCHAR(255) NOT NULL,
    action VARCHAR(255) NOT NULL,
    resource TEXT NOT NULL,
    result VARCHAR(50) NOT NULL CHECK (result IN ('success', 'denied', 'error')),
    details JSONB DEFAULT '{}',
    sandbox_level VARCHAR(50),
    source_ip VARCHAR(45)
);

-- Sessions table (for Redis fallback / persistent sessions)
CREATE TABLE IF NOT EXISTS sessions (
    token_hash VARCHAR(128) PRIMARY KEY,
    device_id VARCHAR(255) NOT NULL,
    scope JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    last_rotated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scheduled tasks table
CREATE TABLE IF NOT EXISTS scheduled_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    cron VARCHAR(100) NOT NULL,
    prompt TEXT NOT NULL,
    project_name VARCHAR(255) REFERENCES projects(name),
    enabled BOOLEAN DEFAULT true,
    last_run TIMESTAMPTZ,
    next_run TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Device trust table
CREATE TABLE IF NOT EXISTS devices (
    device_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    fingerprint VARCHAR(255) NOT NULL,
    trust_level VARCHAR(50) DEFAULT 'untrusted' CHECK (trust_level IN ('untrusted', 'paired', 'trusted')),
    public_key TEXT,
    first_seen TIMESTAMPTZ DEFAULT NOW(),
    last_seen TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_actor ON audit_log (actor);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log (action);
CREATE INDEX IF NOT EXISTS idx_sessions_device ON sessions (device_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions (expires_at);
CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_enabled ON scheduled_tasks (enabled) WHERE enabled = true;
CREATE INDEX IF NOT EXISTS idx_devices_trust ON devices (trust_level);

COMMIT;
