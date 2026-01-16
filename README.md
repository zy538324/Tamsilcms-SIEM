# Tamsilcms SIEM (Low-Level Foundation)

## Project Overview
This repository delivers a low-level SIEM foundation built for secure ingestion, durable storage, and clear operator visibility. The architecture remains deliberately lean: a C# log shipper, a Node.js (TypeScript) ingestion API, PostgreSQL storage, and a modern dashboard for reading logs with filters and pagination.

## Architecture
```
[ Endpoint ]
   |
   | (JSON events over HTTPS)
   v
[ Ingestion API (Node.js / Fastify) ]
   |
   | (validated, normalised events)
   v
[ PostgreSQL ]
   |
   | (SQL queries)
   v
[ Dashboard (HTML/CSS/TypeScript) ]
```

## Components
- **Agent (C#/.NET 8)**: Reads local log files, batches events, and sends them securely with retry and spooling.
- **Backend (Fastify + TypeScript)**: Authenticates agents via API key, validates payloads, and writes logs to PostgreSQL.
- **Dashboard (HTML/CSS/TypeScript)**: Presents log stream and agent list with filtering and pagination.

## Local Development
1. Copy the environment template.
   ```bash
   cp .env.example .env
   ```
2. Start PostgreSQL.
   ```bash
   docker compose up -d postgres
   ```
3. Apply the schema.
   ```bash
   psql "$DATABASE_URL" -f db/schema.sql
   ```
4. Run the backend API.
   ```bash
   cd backend
   npm install
   npm run dev
   ```
5. Build and serve the dashboard.
   ```bash
   cd frontend
   npm install
   npm run build
   python -m http.server 8000
   ```

## Agent Setup
1. Export the agent environment variables (or set them in your service manager).
2. Run the agent:
   ```bash
   cd agent-csharp
   dotnet run
   ```

## Security Notes
- API keys are stored hashed (PBKDF2 + pepper) and never logged.
- All endpoints enforce payload size limits and schema validation.
- Use HTTPS in production and restrict database permissions to least privilege.

## Roadmap
- Alerting engine
- Enrichment pipeline
- Rule management and correlation

## Why this approach?
The stack prioritises strong foundations: secure ingestion, durable storage, and readable data. This ensures later features (alerting, correlation, intelligence feeds) can be added without reworking core data handling.
