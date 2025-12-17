-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================
-- DIAGRAM STORAGE TABLE
-- Store diagram metadata with S3 references
-- ============================================================

CREATE TABLE IF NOT EXISTS diagrams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL,
    title TEXT NOT NULL,
    description TEXT,

    s3_key TEXT NOT NULL UNIQUE,
    diagram_type TEXT NOT NULL DEFAULT 'mermaid',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    created_by TEXT,
    tags TEXT[],

    CONSTRAINT fk_diagram_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_diagrams_project_id
    ON diagrams(project_id);

CREATE INDEX IF NOT EXISTS idx_diagrams_created_at
    ON diagrams(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_diagrams_s3_key
    ON diagrams(s3_key);

CREATE INDEX IF NOT EXISTS idx_diagrams_tags
    ON diagrams USING GIN(tags);

-- ============================================================
-- Auto-update updated_at trigger
-- ============================================================

CREATE OR REPLACE FUNCTION update_diagram_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER diagrams_updated_at
BEFORE UPDATE ON diagrams
FOR EACH ROW
EXECUTE FUNCTION update_diagram_timestamp();
