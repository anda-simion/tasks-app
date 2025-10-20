-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Explicitly create the tasks_user role if it doesn't exist
DO
$do$
BEGIN
IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'tasks_user') THEN
CREATE ROLE tasks_user WITH LOGIN PASSWORD 'tasks_password';
END IF;
END
$do$;

-- Create enum type for task status
DO $$
BEGIN
IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'taskstatus') THEN
CREATE TYPE taskstatus AS ENUM ('not_done', 'done', 'deleted');
END IF;
END
$$;

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
text TEXT NOT NULL,
status taskstatus NOT NULL DEFAULT 'not_done',
created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Optional: trigger to update updated_at automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
NEW.updated_at = now();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON tasks;
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();