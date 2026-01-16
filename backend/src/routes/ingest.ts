import { FastifyInstance, FastifyReply, FastifyRequest } from "fastify";

import { pool } from "../db.js";
import { verifyApiKey } from "../security.js";
import { ingestPayloadSchema } from "../types.js";

interface IngestRequest extends FastifyRequest {
  Headers: {
    "x-agent-key"?: string;
  };
}

export const registerIngestRoutes = async (app: FastifyInstance) => {
  app.post("/logs/ingest", async (request: IngestRequest, reply: FastifyReply) => {
    const apiKey = request.headers["x-agent-key"];
    if (!apiKey) {
      return reply.status(401).send({ error: "Missing API key" });
    }

    const parseResult = ingestPayloadSchema.safeParse(request.body);
    if (!parseResult.success) {
      return reply.status(400).send({ error: "Invalid payload", details: parseResult.error.flatten() });
    }

    const payload = parseResult.data;

    const mismatch = payload.events.find((event) => event.agent_id !== payload.agent_id);
    if (mismatch) {
      return reply.status(400).send({ error: "Agent mismatch" });
    }

    const agentResult = await pool.query(
      "SELECT id, api_key_hash FROM agents WHERE id = $1",
      [payload.agent_id]
    );

    const agent = agentResult.rows[0];
    if (!agent || !verifyApiKey(apiKey, agent.api_key_hash)) {
      return reply.status(403).send({ error: "Invalid credentials" });
    }

    const values: Array<string | number> = [];
    const placeholders: string[] = [];

    payload.events.forEach((event, index) => {
      const baseIndex = index * 7;
      placeholders.push(`($${baseIndex + 1}, $${baseIndex + 2}, $${baseIndex + 3}, $${baseIndex + 4}, $${baseIndex + 5}, $${baseIndex + 6}, $${baseIndex + 7})`);
      values.push(
        event.agent_id,
        event.log_source,
        event.event_time,
        event.event_level.toUpperCase(),
        event.event_id,
        event.message,
        new Date().toISOString()
      );
    });

    if (values.length > 0) {
      await pool.query(
        `INSERT INTO logs (agent_id, log_source, event_time, event_level, event_id, message, received_at)
         VALUES ${placeholders.join(", ")}`,
        values
      );
    }

    return reply.status(202).send({ status: "accepted", received: payload.events.length });
  });
};
